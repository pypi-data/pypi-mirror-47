import os
import sys
import stat
import shutil
import importlib
import contextlib

import pytest

from textwrap import dedent

from setuptools import Distribution

from ..setup_helpers import get_package_info, register_commands
from ..commands import build_ext

from . import reset_setup_helpers, reset_distutils_log  # noqa
from . import run_setup, cleanup_import

ASTROPY_HELPERS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _extension_test_package(tmpdir, request, extension_type='c', include_numpy=False):
    """Creates a simple test package with an extension module."""

    test_pkg = tmpdir.mkdir('test_pkg')
    test_pkg.mkdir('apyhtest_eva').ensure('__init__.py')

    # TODO: It might be later worth making this particular test package into a
    # reusable fixture for other build_ext tests

    if extension_type in ('c', 'both'):
        # A minimal C extension for testing
        test_pkg.join('apyhtest_eva', 'unit01.c').write(dedent("""\
            #include <Python.h>
            #ifndef PY3K
            #if PY_MAJOR_VERSION >= 3
            #define PY3K 1
            #else
            #define PY3K 0
            #endif
            #endif

            #if PY3K
            static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "unit01",
                NULL,
                -1,
                NULL
            };
            PyMODINIT_FUNC
            PyInit_unit01(void) {
                return PyModule_Create(&moduledef);
            }
            #else
            PyMODINIT_FUNC
            initunit01(void) {
                Py_InitModule3("unit01", NULL, NULL);
            }
            #endif
        """))

    if extension_type in ('pyx', 'both'):
        # A minimal Cython extension for testing
        test_pkg.join('apyhtest_eva', 'unit02.pyx').write(dedent("""\
            print("Hello cruel angel.")
        """))

    if extension_type == 'c':
        extensions = ['unit01.c']
    elif extension_type == 'pyx':
        extensions = ['unit02.pyx']
    elif extension_type == 'both':
        extensions = ['unit01.c', 'unit02.pyx']

    include_dirs = ['numpy'] if include_numpy else []

    extensions_list = [
        "Extension('apyhtest_eva.{0}', [join('apyhtest_eva', '{1}')], include_dirs={2})".format(
            os.path.splitext(extension)[0], extension, include_dirs)
        for extension in extensions]

    test_pkg.join('apyhtest_eva', 'setup_package.py').write(dedent("""\
        from setuptools import Extension
        from os.path import join
        def get_extensions():
            return [{0}]
    """.format(', '.join(extensions_list))))

    test_pkg.join('setup.py').write(dedent("""\
        import sys
        from os.path import join
        from setuptools import setup
        sys.path.insert(0, r'{astropy_helpers_path}')
        from astropy_helpers.setup_helpers import register_commands
        from astropy_helpers.setup_helpers import get_package_info
        from astropy_helpers.version_helpers import generate_version_py

        if '--no-cython' in sys.argv:
            from astropy_helpers.commands import build_ext
            build_ext.should_build_with_cython = lambda *args: False
            sys.argv.remove('--no-cython')

        NAME = 'apyhtest_eva'
        VERSION = '0.1'
        RELEASE = True

        cmdclassd = register_commands(NAME, VERSION, RELEASE)
        generate_version_py(NAME, VERSION, RELEASE, False, False)
        package_info = get_package_info()

        setup(
            name=NAME,
            version=VERSION,
            cmdclass=cmdclassd,
            **package_info
        )
    """.format(astropy_helpers_path=ASTROPY_HELPERS_PATH)))

    if '' in sys.path:
        sys.path.remove('')

    sys.path.insert(0, '')

    def finalize():
        cleanup_import('apyhtest_eva')

    request.addfinalizer(finalize)

    return test_pkg


@pytest.fixture
def extension_test_package(tmpdir, request):
    return _extension_test_package(tmpdir, request, extension_type='both')


@pytest.fixture
def c_extension_test_package(tmpdir, request):
    # Check whether numpy is installed in the test environment
    has_numpy = bool(importlib.util.find_spec('numpy'))
    return _extension_test_package(tmpdir, request, extension_type='c',
                                   include_numpy=has_numpy)


@pytest.fixture
def pyx_extension_test_package(tmpdir, request):
    return _extension_test_package(tmpdir, request, extension_type='pyx')


def test_cython_autoextensions(tmpdir):
    """
    Regression test for https://github.com/astropy/astropy-helpers/pull/19

    Ensures that Cython extensions in sub-packages are discovered and built
    only once.
    """

    # Make a simple test package
    test_pkg = tmpdir.mkdir('test_pkg')
    test_pkg.mkdir('yoda').mkdir('luke')
    test_pkg.ensure('yoda', '__init__.py')
    test_pkg.ensure('yoda', 'luke', '__init__.py')
    test_pkg.join('yoda', 'luke', 'dagobah.pyx').write(
        """def testfunc(): pass""")

    # Required, currently, for get_package_info to work
    register_commands('yoda', '0.0', False, srcdir=str(test_pkg))
    package_info = get_package_info(str(test_pkg))

    assert len(package_info['ext_modules']) == 1
    assert package_info['ext_modules'][0].name == 'yoda.luke.dagobah'


def test_compiler_module(capsys, c_extension_test_package):
    """
    Test ensuring that the compiler module is built and installed for packages
    that have extension modules.
    """

    test_pkg = c_extension_test_package
    install_temp = test_pkg.mkdir('install_temp')

    with test_pkg.as_cwd():
        # This is one of the simplest ways to install just a package into a
        # test directory
        run_setup('setup.py',
                  ['install',
                   '--single-version-externally-managed',
                   '--install-lib={0}'.format(install_temp),
                   '--record={0}'.format(install_temp.join('record.txt'))])

        stdout, stderr = capsys.readouterr()
        assert "No git repository present at" in stderr

    with install_temp.as_cwd():
        import apyhtest_eva
        # Make sure we imported the apyhtest_eva package from the correct place
        dirname = os.path.abspath(os.path.dirname(apyhtest_eva.__file__))
        assert dirname == str(install_temp.join('apyhtest_eva'))

        import apyhtest_eva.compiler_version
        assert apyhtest_eva.compiler_version != 'unknown'


def test_no_cython_buildext(capsys, c_extension_test_package, monkeypatch):
    """
    Regression test for https://github.com/astropy/astropy-helpers/pull/35

    This tests the custom build_ext command installed by astropy_helpers when
    used with a project that has no Cython extensions (but does have one or
    more normal C extensions).
    """

    test_pkg = c_extension_test_package

    with test_pkg.as_cwd():

        run_setup('setup.py', ['build_ext', '--inplace', '--no-cython'])

        stdout, stderr = capsys.readouterr()
        assert "No git repository present at" in stderr

    sys.path.insert(0, str(test_pkg))

    try:
        import apyhtest_eva.unit01
        dirname = os.path.abspath(os.path.dirname(apyhtest_eva.unit01.__file__))
        assert dirname == str(test_pkg.join('apyhtest_eva'))
    finally:
        sys.path.remove(str(test_pkg))


def test_missing_cython_c_files(capsys, pyx_extension_test_package, monkeypatch):
    """
    Regression test for https://github.com/astropy/astropy-helpers/pull/181

    Test failure mode when building a package that has Cython modules, but
    where Cython is not installed and the generated C files are missing.
    """

    test_pkg = pyx_extension_test_package

    with test_pkg.as_cwd():

        with pytest.raises(SystemExit):
            run_setup('setup.py', ['build_ext', '--inplace', '--no-cython'])

        stdout, stderr = capsys.readouterr()
        assert "No git repository present at" in stderr

        msg = ('Could not find C/C++ file '
               '{0}.(c/cpp)'.format('apyhtest_eva/unit02'.replace('/', os.sep)))

        assert msg in stderr


@pytest.mark.parametrize('mode', ['cli', 'cli-w', 'deprecated', 'cli-l'])
def test_build_docs(capsys, tmpdir, mode):
    """
    Test for build_docs
    """

    test_pkg = tmpdir.mkdir('test_pkg')

    test_pkg.mkdir('mypackage')

    test_pkg.join('mypackage').join('__init__.py').write(dedent("""\
        def test_function():
            pass

        class A():
            pass

        class B(A):
            pass
    """))

    test_pkg.mkdir('docs')

    docs_dir = test_pkg.join('docs')
    docs_dir.join('conf.py').write(dedent("""\
        import warnings
        with warnings.catch_warnings():  # ignore matplotlib warning
            warnings.simplefilter("ignore")
            from sphinx_astropy.conf import *
        exclude_patterns.append('_templates')
        suppress_warnings = ['app.add_directive', 'app.add_node', 'app.add_role']
    """))

    docs_dir.join('index.rst').write(dedent("""\
        .. automodapi:: mypackage
           :no-inheritance-diagram:
    """))

    # For this test we try out the new way of calling register_commands without
    # arugments, instead getting the information from setup.cfg.
    test_pkg.join('setup.cfg').write(dedent("""
        [metadata]
        name = mypackage
        version = 0.1
    """))

    test_pkg.join('setup.py').write(dedent("""\
        import sys
        sys.path.insert(0, r'{astropy_helpers_path}')
        from astropy_helpers.setup_helpers import setup
        setup()
    """.format(astropy_helpers_path=ASTROPY_HELPERS_PATH)))

    with test_pkg.as_cwd():

        if mode == 'cli':
            run_setup('setup.py', ['build_docs'])
        elif mode == 'cli-w':
            run_setup('setup.py', ['build_docs', '-w'])
        elif mode == 'cli-l':
            run_setup('setup.py', ['build_docs', '-l'])
        elif mode == 'deprecated':
            run_setup('setup.py', ['build_sphinx'])
            stdout, stderr = capsys.readouterr()
            assert 'AstropyDeprecationWarning' in stderr

    assert os.path.exists(docs_dir.join('_build', 'html', 'index.html').strpath)


def test_command_hooks(tmpdir, capsys):
    """A basic test for pre- and post-command hooks."""

    test_pkg = tmpdir.mkdir('test_pkg')
    test_pkg.mkdir('_welltall_')
    test_pkg.join('_welltall_', '__init__.py').ensure()

    # Create a setup_package module with a couple of command hooks in it
    test_pkg.join('_welltall_', 'setup_package.py').write(dedent("""\
        def pre_build_hook(cmd_obj):
            print('Hello build!')

        def post_build_hook(cmd_obj):
            print('Goodbye build!')

    """))

    # A simple setup.py for the test package--running register_commands should
    # discover and enable the command hooks
    test_pkg.join('setup.py').write(dedent("""\
        import sys
        from os.path import join
        from setuptools import setup, Extension
        sys.path.insert(0, r'{astropy_helpers_path}')
        from astropy_helpers.setup_helpers import register_commands, get_package_info

        NAME = '_welltall_'
        VERSION = '0.1'
        RELEASE = True

        cmdclassd = register_commands(NAME, VERSION, RELEASE)

        setup(
            name=NAME,
            version=VERSION,
            cmdclass=cmdclassd
        )
    """.format(astropy_helpers_path=ASTROPY_HELPERS_PATH)))

    with test_pkg.as_cwd():
        try:
            run_setup('setup.py', ['build'])
        finally:
            cleanup_import('_welltall_')

    stdout, stderr = capsys.readouterr()
    want = dedent("""\
        running build
        running pre_hook from _welltall_.setup_package for build command
        Hello build!
        running post_hook from _welltall_.setup_package for build command
        Goodbye build!
    """).strip()

    assert want in stdout.replace('\r\n', '\n').replace('\r', '\n')


def test_invalid_package_exclusion(tmpdir, capsys):

    module_name = 'foobar'
    setup_header = dedent("""\
        import sys
        from os.path import join
        from setuptools import setup, Extension
        sys.path.insert(0, r'{astropy_helpers_path}')
        from astropy_helpers.setup_helpers import register_commands, \\
            get_package_info, add_exclude_packages

        NAME = {module_name!r}
        VERSION = '0.1'
        RELEASE = True

    """.format(module_name=module_name, astropy_helpers_path=ASTROPY_HELPERS_PATH))

    setup_footer = dedent("""\
        setup(
            name=NAME,
            version=VERSION,
            cmdclass=cmdclassd,
            **package_info
        )
    """)

    # Test error when using add_package_excludes out of order
    error_commands = dedent("""\
        cmdclassd = register_commands(NAME, VERSION, RELEASE)
        package_info = get_package_info()
        add_exclude_packages(['tests*'])

    """)

    error_pkg = tmpdir.mkdir('error_pkg')
    error_pkg.join('setup.py').write(
        setup_header + error_commands + setup_footer)

    with error_pkg.as_cwd():
        with pytest.raises(SystemExit):
            run_setup('setup.py', ['build'])

        stdout, stderr = capsys.readouterr()
        assert "RuntimeError" in stderr

    # Test warning when using deprecated exclude parameter
    warn_commands = dedent("""\
        cmdclassd = register_commands(NAME, VERSION, RELEASE)
        package_info = get_package_info(exclude=['test*'])

    """)

    warn_pkg = tmpdir.mkdir('warn_pkg')
    warn_pkg.join('setup.py').write(
        setup_header + warn_commands + setup_footer)

    with warn_pkg.as_cwd():
        run_setup('setup.py', ['build'])
        stdout, stderr = capsys.readouterr()
        assert 'AstropyDeprecationWarning' in stderr

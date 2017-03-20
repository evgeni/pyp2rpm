import pytest
import os

from flexmock import flexmock
from scripttest import TestFileEnvironment

from pyp2rpm.bin import Convertor, SclConvertor, main, convert_to_scl


tests_dir = os.path.split(os.path.abspath(__file__))[0]


class TestSpec(object):
    td_dir = '{0}/test_data/'.format(tests_dir)
    bin_dir = os.path.split(tests_dir)[0] + '/'
    exe = 'python {0}mybin.py'.format(bin_dir)

    def setup_method(self, method):
        self.env = TestFileEnvironment('{0}/test_output/'.format(tests_dir))

    @pytest.mark.parametrize(('package', 'options', 'expected'), [
        ('Jinja2', '-v2.8', 'python-Jinja2.spec'),
        ('Jinja2', '-v2.8 -b3', 'python-Jinja2_base.spec'),
        ('Jinja2', '-v2.8 -t epel7', 'python-Jinja2_epel7.spec'),
        ('Jinja2', '-v2.8 -t epel6', 'python-Jinja2_epel6.spec'),
        ('buildkit', '-v0.2.2 -b2', 'python-buildkit.spec'),
        ('StructArray', '-v0.1 -b2', 'python-StructArray.spec'),
        ('Sphinx', '-v1.5 -r python-sphinx', 'python-sphinx.spec'),
    ])
    @pytest.mark.webtest
    def test_spec(self, package, options, expected):
        with open(self.td_dir + expected) as fi:
            self.spec_content = fi.read()
        res = self.env.run('{0} {1} {2}'.format(self.exe, package, options),
                           expect_stderr=True)
        # changelog have to be cut from spec files
        assert set(res.stdout.split('\n')[1:-4]) == set(self.spec_content.split('\n')[1:-4])


class TestSrpm(object):
    td_dir = '{0}/test_data/'.format(tests_dir)
    bin_dir = os.path.split(tests_dir)[0] + '/'
    exe = 'python {0}mybin.py'.format(bin_dir)

    def setup_method(self, method):
        self.env = TestFileEnvironment('{0}/test_output/'.format(tests_dir))

    @pytest.mark.webtest
    def test_srpm(self):
        res = self.env.run('{0} Jinja2 --srpm'.format(self.exe), expect_stderr=True)
        assert res.returncode == 0


@pytest.mark.skipif(SclConvertor is None, reason="spec2scl not installed")
class TestSclIntegration(object):
    """
    """
    sphinx_spec = '{0}/test_data/python-sphinx.spec'.format(tests_dir)

    @classmethod
    def setup_class(cls):
        with open(cls.sphinx_spec, 'r') as spec:
            cls.test_spec = spec.read()

    def setup_method(self, method):
        self.default_options = {
            'no_meta_runtime_dep': False,
            'no_meta_buildtime_dep': False,
            'skip_functions': [''],
            'no_deps_convert': False,
            'list_file': None,
            'meta_spec': None
        }
        flexmock(Convertor).should_receive('__init__').and_return(None)
        flexmock(Convertor).should_receive('convert').and_return(self.test_spec)

    @pytest.mark.parametrize(('options', 'expected_options'), [
        (['--no-meta-runtime-dep'], {'no_meta_runtime_dep': True}),
        (['--no-meta-buildtime-dep'], {'no_meta_buildtime_dep': True}),
        (['--skip-functions=func1,func2'], {'skip_functions': ['func1', 'func2']}),
        (['--no-deps-convert'], {'no_deps_convert': True}),
        (['--list-file=file_name'], {'list_file': 'file_name'}),
    ])
    def test_scl_convertor_args_correctly_passed(self, options, expected_options, capsys):
        """Test that pyp2rpm command passes correct options to SCL convertor."""
        self.default_options.update(expected_options)
        flexmock(SclConvertor).should_receive('convert').and_return(self.test_spec)
        flexmock(SclConvertor).should_receive('__init__').with_args(
            spec=self.test_spec,
            options=self.default_options,
        ).once()

        with pytest.raises(SystemExit):
            main(args=['foo_package', '--sclize'] + options)
        out, err = capsys.readouterr()
        assert out == self.test_spec + '\n'

    @pytest.mark.parametrize(('options', 'omit_from_spec'), [
        ({'no_meta_runtime_dep': True}, '%{?scl:Requires: %{scl}-runtime}'),
        ({'no_meta_buildtime_dep': True}, '{?scl:BuildRequires: %{scl}-runtime}'),
        ({'skip_functions': 'handle_python_specific_commands'},
         '%{?scl:scl enable %{scl} - << \\EOF}\nset -e\nsphinx-build doc html\n%{?scl:EOF}'),
    ])
    def test_convert_to_scl_options(self, options, omit_from_spec):
        """Test integration with SCL options."""
        self.default_options.update({'skip_functions': ''})
        self.default_options.update(options)
        converted = convert_to_scl(self.test_spec, self.default_options)
        assert omit_from_spec not in converted

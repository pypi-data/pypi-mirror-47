# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises

from _sadm.configure import plugins
from _sadm.env.settings import Settings
from _sadm.errors import EnvError, AssetNotFoundError

def test_configure(testing_env):
	e = testing_env()
	e.session.start()
	plugins.configure(e)
	assert isinstance(e.settings, Settings)

def test_file_not_found(testing_env):
	e = testing_env()
	with raises(AssetNotFoundError):
		plugins.configure(e, cfgfile = 'nofile.ini')

def test_cfg_invalid_name(testing_env):
	e = testing_env()
	with raises(EnvError, match = 'invalid config name \'fake\''):
		plugins.configure(e, cfgfile = 'testing/config-invalid-name.ini')

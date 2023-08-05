# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from os import path
from pytest import raises

from _sadm import cfg
from _sadm.errors import Error

def test_cfg():
	assert cfg._DEFAULT['name'] == ''
	assert cfg._DEFAULT['profile'] == 'default'
	assert cfg._DEFAULT['env'] == 'default'
	c = cfg.new()
	assert isinstance(c, ConfigParser)
	assert c.name() == 'sadmtest'
	assert c.filename().endswith(path.join('tdata', 'sadm.cfg'))
	assert len(c.defaults()) == 5
	assert c.get('default', 'name') == 'sadmtest'
	assert c.get('default', 'profile') == 'testing'
	assert c.get('default', 'env') == 'testing'
	assert c.get('default', 'dir') == '.'
	assert c.listPlugins('testing') == ['sadm', 'os', 'testing']
	assert len(c.sections()) == 2
	assert c.has_section('testing')
	assert c.get('testing', 'dir') == './tdata'
	assert c.get('testing', 'env.testing') == 'testing/config.ini'
	assert sorted(c.listProfiles()) == ['envsetup', 'testing']
	assert sorted(c.listEnvs('testing')) == ['testing', 'testing.nodir']

def test_profile_error():
	c = cfg.new()
	with raises(Error, match = 'ProfileError: config profile noprofile not found'):
		c.listEnvs('noprofile')

def test_default_plugins():
	assert tuple(sorted(cfg._enablePlugins)) == ('os', 'os.user', 'sadm', 'sadmenv')

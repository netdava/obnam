# Copyright (C) 2009  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import socket

import obnamlib


class App(object):

    '''Main program for backup program.'''
    
    def __init__(self):
        self.hooks = obnamlib.HookManager()
        
        self.config = obnamlib.Configuration([])
        self.config.new_string(['log'], 'name of log file (%default)')
        self.config['log'] = 'obnam.log'
        self.config.new_string(['store'], 'name of backup store')
        self.config.new_string(['hostname'], 'name of host (%default)')
        self.config['hostname'] = self.deduce_hostname()

        self.pm = obnamlib.PluginManager()
        self.pm.locations = [self.plugins_dir()]
        self.pm.plugin_arguments = (self,)
        
        self.interp = obnamlib.Interpreter()
        self.register_command = self.interp.register

        self.hooks.new('plugins-loaded')
        self.hooks.new('shutdown')
        
    def deduce_hostname(self):
        return socket.gethostname()
        
    def plugins_dir(self):
        return os.path.join(os.path.dirname(obnamlib.__file__), 'plugins')

    def setup_logging(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(self.config['log'])
        handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        
    def run(self):
        self.pm.load_plugins()
        self.pm.enable_plugins()
        self.hooks.call('plugins-loaded')
        self.config.load()
        self.setup_logging()
        if self.config.args:
            self.interp.execute(self.config.args[0], self.config.args[1:])
        else:
            raise obnamlib.AppException('Usage error: '
                                        'must give operation on command line')
        self.hooks.call('shutdown')

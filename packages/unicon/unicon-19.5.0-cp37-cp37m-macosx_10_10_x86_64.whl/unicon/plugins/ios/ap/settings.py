__copyright__ = "# Copyright (c) 2016 by cisco Systems, Inc. All rights reserved."
__author__ = "Giacomo Trifilo <gtrifilo@cisco.com>"

from unicon.plugins.generic.settings import GenericSettings


class ApSettings(GenericSettings):
    def __init__(self):
        super().__init__()

        self.HA_INIT_EXEC_COMMANDS = [
            'debug capwap console cli',
            'terminal length 0',
            'terminal width 0',
            'show version'
        ]

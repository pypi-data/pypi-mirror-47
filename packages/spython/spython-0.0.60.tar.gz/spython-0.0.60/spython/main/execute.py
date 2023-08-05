
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
from spython.utils import stream_command
import os
import sys


def execute(self, 
            image = None, 
            command = None,
            app = None,
            writable = False,
            contain = False,
            bind = None,
            stream = False,
            nv = False,
            return_result=False):

    ''' execute: send a command to a container
    
        Parameters
        ==========

        image: full path to singularity image
        command: command to send to container
        app: if not None, execute a command in context of an app
        writable: This option makes the file system accessible as read/write
        contain: This option disables the automatic sharing of writable
                 filesystems on your host
        bind: list or single string of bind paths.
             This option allows you to map directories on your host system to
             directories within your container using bind mounts
        nv: if True, load Nvidia Drivers in runtime (default False)
        return_result: if True, return entire json object with return code
                       and message result (default is False)
    '''
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('exec')

    # nv option leverages any GPU cards
    if nv is True:
        cmd += ['--nv']
    
    # If the image is given as a list, it's probably the command
    if isinstance(image, list):
        command = image
        image = None

    if command is not None:
        
        # No image provided, default to use the client's loaded image
        if image is None:
            image = self._get_uri()
            self.quiet = True

        # If an instance is provided, grab it's name
        if isinstance(image, self.instance):
            image = image.get_uri()

        # Does the user want to use bind paths option?
        if bind is not None:
            cmd += self._generate_bind_list(bind)

        # Does the user want to run an app?
        if app is not None:
            cmd = cmd + ['--app', app]

        sudo = False
        if writable is True:
            sudo = True

        if not isinstance(command, list):
            command = command.split(' ')

        cmd = cmd + [image] + command
 
        if stream is False:
            return self._run_command(cmd,
                                     sudo=sudo,
                                     return_result=return_result)
        return stream_command(cmd, sudo=sudo)

    bot.error('Please include a command (list) to execute.')

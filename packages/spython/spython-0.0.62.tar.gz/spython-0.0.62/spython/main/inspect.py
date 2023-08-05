
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json as jsonp

from spython.utils import ( 
    check_install, 
    run_command
)

def inspect(self, image=None, json=True, app=None, quiet=True):
    '''inspect will show labels, defile, runscript, and tests for an image
    
       Parameters
       ==========
       image: path of image to inspect
       json: print json instead of raw text (default True)
       quiet: Don't print result to the screen (default True)
       app: if defined, return help in context of an app

    '''
    check_install()

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    cmd = self._init_command('inspect')
    if app is not None:
        cmd = cmd + ['--app', app]

    options = ['e','d','l','r','hf','t']

    # After Singularity 3.0, helpfile was changed to H from

    if "version 3" in self.version():
        options = ['e','d','l','r','H','t']

    for x in options:
        cmd.append('-%s' % x)

    if json is True:
        cmd.append('--json')

    cmd.append(image)
    result = run_command(cmd, quiet=False)

    if result['return_code'] == 0:
        result = jsonp.loads(result['message'][0])

        # Unify output to singularity 3 format
        if "data" in result:
            result = result['data']

        # Fix up labels
        result = parse_labels(result)

        if not quiet:
            print(jsonp.dumps(result, indent=4))

    return result


def parse_labels(result):
    '''fix up the labels, meaning parse to json if needed, and return
       original updated object

       Parameters
       ==========
       result: the json object to parse from inspect
    '''

    labels = result['attributes'].get('labels') or {}
    try:
        labels = jsonp.loads(labels)
    except:
        pass

    result['attributes']['labels'] = labels

    return result

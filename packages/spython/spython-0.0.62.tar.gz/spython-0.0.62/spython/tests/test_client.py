#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
from spython.main import Client
import unittest
import tempfile
import shutil
import os


print("########################################################### test_client")

class TestClient(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.cli = Client
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        #shutil.rmtree(self.tmpdir)
        print('not')
    def test_commands(self):

        print('Testing client.build command')
        container = "%s/container.sif" %(self.tmpdir)

        print("...Case 1: Build from docker uri")
        created_container = self.cli.build('docker://busybox:1.30.1', 
                                           image=container,
                                           sudo=False)
        self.assertEqual(created_container, container)
        self.assertTrue(os.path.exists(created_container))
        os.remove(container)

        print('Testing client.export command')
        sandbox = "busybox:1.30.sandbox"
        created_sandbox = self.cli.export('docker://busybox:1.30.1')
        self.assertEqual(created_sandbox, sandbox)
        self.assertTrue(os.path.exists(created_sandbox))
        shutil.rmtree(created_sandbox)

        print("Testing client.pull command")
        print("...Case 1: Testing naming pull by image name")
        image = self.cli.pull("shub://vsoch/singularity-images", 
                              pull_folder=self.tmpdir)
        self.assertTrue(os.path.exists(image))
        self.assertTrue('singularity-images' in image)
        print(image)

        print('Testing client.run command')
        result = self.cli.run(image)
        print(result)
        self.assertTrue('You say please, but all I see is pizza..' in result)
        os.remove(image)

        print("...Case 2: Testing docker pull")
        container = self.cli.pull("docker://busybox:1.30.1",
                                   pull_folder=self.tmpdir)
        self.assertTrue("busybox:1.30.1" in container)

        print(container)
        self.assertTrue(os.path.exists(container))

        print('Testing client.execute command')
        result = self.cli.execute(container,'ls /')
        print(result)
        self.assertTrue('tmp\nusr\nvar' in result)

        print('Testing client.execute command with return code')
        result = self.cli.execute(container,'ls /', return_result=True)
        print(result)
        self.assertTrue('tmp\nusr\nvar' in result['message'])
        self.assertEqual(result['return_code'], 0)

        print("Testing client.inspect command")
        result = self.cli.inspect(container)
        self.assertEqual(result['type'], 'container')
        self.assertTrue('attributes' in result)

        os.remove(container)


if __name__ == '__main__':
    unittest.main()

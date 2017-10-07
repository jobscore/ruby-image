#!/usr/bin/env python
import os
import sys
import subprocess


def packer_args(option):
    args = [
        "packer",
        "build",
        option,
        "packer.json"
    ]
    return args


branch = os.getenv('TRAVIS_BRANCH', '')

if branch == 'master':
    os.environ['RELEASE_VER'] = "latest"
    args = packer_args("-except=testing")
elif branch == 'develop':
    os.environ['RELEASE_VER'] = "beta"
    args = packer_args("-except=testing")
elif 'release/' in branch:
    os.environ['RELEASE_VER'] = branch.replace('release/', '')
    args = packer_args("-except=testing")
else:
    args = packer_args("-only=testing")
    os.environ['RELEASE_VER'] = "alpha"

print("Packer cmd: " + " ".join(args))
print("Version: {}".format(os.environ['RELEASE_VER']))

cmd = subprocess.Popen(args)
cmd.wait()
sys.exit(cmd.returncode)

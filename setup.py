#!/usr/bin/env python
from setuptools import setup
import contextlib
import imp
import os
import re
import subprocess

DATA_ROOTS = []
PROJECT = 'enlil'
VERSION_FILE = 'enlil/version.py'

def _get_output_or_none(args):
    try:
        return subprocess.check_output(args).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def _get_git_description():
    return _get_output_or_none(['git', 'describe'])

def _get_git_branches_for_this_commit():
    branches = _get_output_or_none(['git', 'branch', '-r', '--contains', 'HEAD'])
    split = branches.split('\n') if branches else []
    return [branch.strip() for branch in split]

def _is_on_releasable_branch(branches):
    return any(['origin/master' == branch or branch.startswith('origin/hotfix') for branch in branches])

def _git_to_version(git):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git)
    if not match:
        version = git
    else:
        version = "{tag}.post0.dev{offset}".format(**match.groupdict())
    print("Calculated {} version '{}' from git description '{}'".format(PROJECT, version, git))
    return version

@contextlib.contextmanager
def write_version():
    git_description = _get_git_description()
    git_branches = _get_git_branches_for_this_commit()
    version = _git_to_version(git_description) if git_description else None
    if git_branches and not _is_on_releasable_branch(git_branches):
        print("Forcing version to 0.0.1 because this commit is on branches {} and not a whitelisted branch".format(git_branches))
        version = '0.0.1'
    if version:
        with open(VERSION_FILE, 'r') as version_file:
            old_contents = version_file.read()
        with open(VERSION_FILE, 'w') as version_file:
            version_file.write('VERSION = "{}"\n'.format(version))
    yield
    if version:
        with open(VERSION_FILE, 'w') as version_file:
            version_file.write(old_contents)

def get_version():
    basedir = os.path.abspath(os.path.dirname(__file__))
    version = imp.load_source('version', os.path.join(basedir, PROJECT, 'version.py'))
    return version.VERSION

def get_data_files():
    data_files = []
    for data_root in DATA_ROOTS:
        for root, _, files in os.walk(data_root):
            data_files.append((os.path.join(PROJECT, root), [os.path.join(root, f) for f in files]))
    return data_files


def main():
    with write_version():
        setup(
            name                 = "enlil",
            version              = get_version(),
            description          = "A wiki that uses markdown",
            url                  = "https://github.com/EliRibble/enlil",
            long_description     = "A wiki that uses markdown and is awesome",
            author               = "Eli Ribble",
            author_email         = "junk@theribbles.org",
            install_requires     = [
                'flask==0.10.1',
            ],
            extras_require       = {
                'develop'        : [
                    'coverage==3.7.1',
                    'pylint==1.4.3',
                    'pytest-cov==1.8.1',
                    'pytest-flask==0.8.1',
                    'pytest-mock==0.7.0',
                    'pytest==2.6.4',
                ],
            },
            packages             = [
                "enlil",
                "enlil.api",
            ],
            package_data         = {
                "enlil"          : ["enlil/*"],
                "enlil.api"      : ["enlil/api/*"],
            },
            data_files           = get_data_files(),
            scripts              = ['bin/enlil'],
            include_package_data = True,
        )


if __name__ == "__main__":
    main()

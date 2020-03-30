#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CHAOSS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Venu Vardhan Reddy Tekula <venuvardhanreddytekula8@gmail.com>
#


from github import Github, BadCredentialsException
from subprocess import call
import os

token = "xxxx"
g = Github(token)
try:
    user = g.get_user()
    print("The PAT is working. You are " + user.login + ".\n")
except BadCredentialsException:
    print("Please check your PAT. Exiting.\n")
    exit()

CHECK_REMOTES_CMD = ['git', 'remote', '-v']
CHECKOUT_MASTER_CMD = ['git', 'checkout', 'master']
FETCH_UPSTREAM_CMD = ['git', 'fetch', 'upstream']
REBASE_UPSTREAM_CMD = ['git', 'rebase', 'upstream/master']

current_path = os.getcwd()
print("Current path: " + current_path)

required_path = os.path.join(current_path, "sources")

print("Moving into the `sources` folder.\n")
os.chdir(required_path)

repos = [f.path for f in os.scandir(os.getcwd()) if f.is_dir()]

for repo in repos:
    os.chdir(repo)
    try:
        print("\n## " + repo.split("/")[-1])
        origin = "https://" + user.login + ":" + token + "@github.com/" + user.login + "/" + repo.split("/")[-1]
        PUSH_TO_UPSTREAM_CMD[2] = origin

        print("\n>>> Checking remotes")
        call(CHECK_REMOTES_CMD)
        print("\n>>> Change to master branch")
        call(CHECKOUT_MASTER_CMD)
        print("\n>>> Fetching upstream")
        call(FETCH_UPSTREAM_CMD)
        print("\n>>> Rebasing master")
        call(REBASE_UPSTREAM_CMD)
    except Exception as e:
        print(e)
        exit()

print("\nDone! 🎉")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CHAOSS
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
import git.repo.base as grb
import os

token = "xxxx"
g = Github(token)
try:
    user = g.get_user()
    print("The PAT is working. You are " + user.login + ".\n")
except BadCredentialsException:
    print("Please check your PAT. Exiting.\n")
    exit()

current_path = os.getcwd()
required_path = os.path.join(current_path, "sources")

print("Creating the folder `sources`.")
try:
    os.mkdir(required_path)
except FileExistsError:
    print("The folder with name `sources` already exists. Moving into the existing folder.")
    pass

os.chdir(required_path)

repos = ["chaoss/grimoirelab-sirmordred", "chaoss/grimoirelab-elk", "chaoss/grimoirelab-kingarthur",
         "chaoss/grimoirelab-graal", "chaoss/grimoirelab-perceval", "chaoss/grimoirelab-perceval-mozilla",
         "chaoss/grimoirelab-perceval-opnfv", "chaoss/grimoirelab-perceval-puppet",
         "Bitergia/grimoirelab-perceval-finos", "chaoss/grimoirelab-sortinghat", "chaoss/grimoirelab-sigils",
         "chaoss/grimoirelab-kidash", "chaoss/grimoirelab-toolkit", "chaoss/grimoirelab-cereslib",
         "chaoss/grimoirelab-manuscripts"]

for item in repos:
    repo_url = item.split("/")
    print("\n" + repo_url[0] + "/" + repo_url[1])
    org = g.get_organization(repo_url[0])
    repo = org.get_repo(repo_url[1])
    print("forking the repository " + repo.name + " to " + user.login)
    my_fork = user.create_fork(repo)  # ignores if already forked
    try:
        print("cloning the repository " + user.login + "/" + repo.name)
        local_repo = grb.Repo.clone_from("https://github.com/" + user.login + "/" + repo.name + ".git",
                                         os.getcwd() + "/" + repo.name, branch="master")
        print("adding the `upstream` remote.")
        grb.Repo.create_remote(local_repo, "upstream",
                               "https://github.com/" + repo_url[0] + "/" + repo.name + ".git")
    except grb.GitCommandError:
        print(str(repo.name) + " already exists and is not empty. Not cloning.")
        pass

print("\nDone! 🎉")

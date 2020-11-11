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


import logging
import os
import os.path
import sys

import argparse
from argparse import RawTextHelpFormatter

from subprocess import call

import git.repo.base as grb
from github import Github, BadCredentialsException, GithubException

REPOS = [
    "chaoss/grimoirelab-sirmordred",
    "chaoss/grimoirelab-elk",
    "chaoss/grimoirelab-kingarthur",
    "chaoss/grimoirelab-graal",
    "chaoss/grimoirelab-perceval",
    "chaoss/grimoirelab-perceval-mozilla",
    "chaoss/grimoirelab-perceval-opnfv",
    "chaoss/grimoirelab-perceval-puppet",
    "chaoss/grimoirelab-perceval-weblate",
    "Bitergia/grimoirelab-perceval-finos",
    "chaoss/grimoirelab-sortinghat",
    "chaoss/grimoirelab-sigils",
    "chaoss/grimoirelab-kidash",
    "chaoss/grimoirelab-toolkit",
    "chaoss/grimoirelab-cereslib",
    "chaoss/grimoirelab-manuscripts"
]

GITHUB_URL = "https://github.com/"

CHECK_REMOTES_CMD = ['git', 'remote', '-v']
CHECKOUT_MASTER_CMD = ['git', 'checkout', 'master']
FETCH_UPSTREAM_CMD = ['git', 'fetch', 'upstream']
REBASE_UPSTREAM_CMD = ['git', 'rebase', 'upstream/master']

LOG_FORMAT = "[%(asctime)s] - %(message)s"
DEBUG_LOG_FORMAT = "[%(asctime)s - %(name)s - %(levelname)s] - %(message)s"


def configure_logging(debug):
    """
    Configure logging.
    This function sets basic attributes for logging.
    :param debug: set the debug mode
    """
    if not debug:
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT)
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format=DEBUG_LOG_FORMAT)


def parse_args():
    """
    Setup command line argument parsing with argparse.
    """
    parser = argparse.ArgumentParser(
        description="glab-dev-env-setup script argument parser",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("-t", "--token",
                        required=True,
                        help="GitHub API Token\n\n")

    parser.add_argument("-s", "--source",
                        default="sources",
                        help="folder of the dev env\n\n")

    parser.add_argument("-d", "--debug",
                        action='store_true',
                        help="set debug mode for logging\n\n")

    parser.add_argument("-u", "--update",
                        action='store_true',
                        help="update the forks.\n\n")

    parser.add_argument("-c", "--create",
                        action='store_true',
                        help="create the repositories.\n\n")

    return parser.parse_args()


def check_token(token):
    """
    Verify token.
    This function checks if the token is valid.

    :param token: github personal access token
    :returns g: GitHub auth object
    """
    logging.info("checking the access token")

    g = Github(token)
    try:
        user = g.get_user()
        logging.info("access token is working, " + user.login)
        return g
    except BadCredentialsException as e:
        logging.error("invalid token: " + str(e))
        exit()
    except Exception as e:
        logging.error("exiting: " + str(e))
        exit()


def move_into_folder(folder):
    """
    Change the directory.
    This function changes the working directory.
    :param folder: required folder name
    """
    req_path = os.path.join(os.getcwd(), folder)
    if os.path.isdir(req_path):
        logging.info("moving into " + req_path)
    else:
        logging.info("folder not existing, creating new " + req_path)
        os.mkdir(req_path)
    os.chdir(req_path)


def fork(user, repo):
    """
    Fork the repository.
    :param user: user
    :param repo: repository
    """
    try:
        logging.info("forking the repository " + repo.name + " to " + user.login)
        user.create_fork(repo)
    except GithubException as e:
        logging.error("forking aborted.")
        logging.error("please select the appropriate scope (`repo`) for the token: " + str(e))
        exit()


def clone_upstream(user, org, repo):
    """
    Clone and set upstream for the repository.
    :param user: user
    :param org: organization
    :param repo: repository
    """
    try:
        logging.info("cloning the forked repository " + repo.name)
        local_repo = grb.Repo.clone_from(GITHUB_URL + user.login + "/" + repo.name + ".git",
                                         "{0}/{1}".format(os.getcwd(), repo.name), branch="master")
        logging.info("adding the `upstream` remote")
        grb.Repo.create_remote(local_repo, "upstream", GITHUB_URL + org.login + "/" + repo.name + ".git")

    except grb.GitCommandError:
        logging.info("folder already exists and is not empty, cloning aborted")
        pass


def check_remote():
    """
    Check the remote of the repository.
    """
    logging.info("checking remotes")
    call(CHECK_REMOTES_CMD)


def sync():
    """
    Update the forks.
    This function fetched the upstream remote and
    updates the master branch of the repository.
    """
    try:
        logging.info("fetching upstream")
        call(FETCH_UPSTREAM_CMD)
        logging.info("changing branch to master")
        call(CHECKOUT_MASTER_CMD)
        logging.info("rebasing")
        call(REBASE_UPSTREAM_CMD)
    except Exception as e:
        logging.error(str(e))
        exit()


def update(source):
    """
    Updates the forks.
    This function iterates through the repositories and
    updates them to the latest fork.

    :param source: dev env folder
    """
    logging.info("updating the forks")
    curr_path = os.getcwd()
    for item in REPOS:
        move_into_folder(curr_path + "/" + source)
        org, repo = item.split("/")
        move_into_folder(repo)
        sync()


def create(g, source):
    """
    Creates the folder with all 15 repositories.
    This function iterates through the repositories and
    fork, clone and sets the upstream in each of the
    repository.

    :param g: GitHub auth object
    :param source: dev env folder
    """
    logging.info("setting up the repositories")
    curr_path = os.getcwd()
    user = g.get_user()
    for item in REPOS:
        move_into_folder(curr_path + "/" + source)
        org, repo = item.split("/")
        org = g.get_organization(org)
        repo = org.get_repo(repo)
        fork(user, repo)
        clone_upstream(user, org, repo)
        move_into_folder(repo.name)
        check_remote()


def main():
    """
    A script for automating the process the setting up the development
    environment for GrimoireLab.


    The script can be run via the command line:
        $ python3 glab-dev-env-setup.py -c -t xxxx

    Examples:
    --------

    * Create a folder `sources` with all the 15 GrimoireLab
    components forked, cloned and setting their upstream link
    using the GitHub API token xxxx:
        $ python3 glab-dev-env-setup.py --create --token xxxx --source sources

    * Update the existing forks present in the `sources` folder
    with the latest changes using the GitHub API token xxxx:
        $ python3 glab-dev-env-setup.py --update --token xxxx --source sources
    """
    args = parse_args()

    token = str(args.token)
    source = str(args.source) if args.source else "sources"

    configure_logging(args.debug)

    g = check_token(token)

    if args.create:
        create(g, source)
    elif args.update:
        update(source)
    else:
        logging.error("select any method, --create or --update")

    return


if __name__ == '__main__':
    try:
        main()
        logging.info("done!")
    except KeyboardInterrupt:
        sys.stderr.write("\n\nReceived Ctrl-C or other break signal. Exiting.\n")
        sys.exit(0)

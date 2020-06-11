# grimoirelab-scripts

automation scripts for maintaining GrimoireLab.

## tools

### [generate-es-index-schema](generate-es-index-schema.py)

#### Usage

You can use the script from the command line
```
$ python3 generate-es-index-schema.py index_name -m client
```

Replace `index_name` with the required index name and check if you have varied credentials for connecting to Elasticsearch if you are using the client method.

#### Examples:

* Create a schema file `git.csv` of the index `git-enriched` using the dump menthod:
```
$ curl -XGET -k "https://admin:admin@localhost:9200/git-enriched/" > mapping
$ python3 generate-es-index-schema.py git-enriched -m dump -f git.csv
```

* You can use `--help`, if you need more details.
```
$ python3 generate-es-index-schema.py --help
```

## setup

### [glab-dev-env-setup](glab-dev-env-setup.py)

A combined version of the above two scripts.

While setting up the developer environment of the GrimoireLab, one step is to fork all the GrimoireLab components, clone them to a target local folder (e.g., sources) and each local repo should have two `remotes`: `origin` points to the forked repo, while `upstream` points to the parent repo.

Reference: [Cloning the repositories](https://github.com/chaoss/grimoirelab-sirmordred/blob/master/Getting-Started.md#cloning-the-repositories-)

This script automates the whole process.

To use these script, you need to install the PyGitHub and GitPython modules in the virtualenvironment (or the machine).
```
$ python3 -m pip install PyGitHub GitPython
```

#### Usage

You can use the script from the command line
```
$ python3 glab-dev-env-setup.py -c -t xxxx
```

Replace the `xxxx` with the GitHub API Token, you can get one from here [Personal Access Tokens | GitHub](https://github.com/settings/tokens/new). Make sure you have minimum **repo** access level.

#### Examples

* Create a folder `sources` with all the 15 GrimoireLab components forked, cloned and setting their upstream link using the GitHub API token xxxx: 
```
$ python3 glab-dev-env-setup.py --create --token xxxx --source sources
```
 
* Update the existing forks present in the `sources` folder with the latest changes using the GitHub API token xxxx: 
```
$ python3 glab-dev-env-setup.py --update --token xxxx --source sources
```

* You can use `--help`, if you need more details.
```
$ python3 glab-dev-env-setup.py --help
```

Reference: https://gist.github.com/vchrombie/4403193198cd79e7ee0079259311f6e8

#### [download-sources.sh](download-sources.sh)

For [setting up the dev-environment in PyCharm](https://github.com/chaoss/grimoirelab-sirmordred#setting-up-a-pycharm-dev-environment), we need to fork, clone and add upstream to each project. A shell script to automate this process.

Python version of the same script, [glab-fork-clone-upstream.py](glab-fork-clone-upstream.py)

#### [sync-local-upstream.sh](sync-local-upstream.sh)

From time to time, we need to update the forks. A shell script to automate this process.

Python version of the same script, [glab-sync-local-upstream.py](glab-sync-local-upstream.py)

References:
- https://gist.github.com/vchrombie/18cc5f36fe5c934067addf44a487ead9
- https://gist.github.com/vchrombie/5593ea202e7f85d0478d2c1532ca2a9b

## mariadb

### [mariadb-script.sh](mariadb-script.sh)

A shell script to install maria-db.

### [dbscript.sh](dbscript.sh)

A shell script to create the test databases in mariadb for elk tests.

---

If you have any suggestion/improvements, please raise an issue or submit a PR to the scripts.

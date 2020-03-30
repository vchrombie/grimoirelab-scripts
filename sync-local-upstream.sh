#!/usr/bin/env bash

cd sources/

repos=(
      elk
      sirmordred
      kingarthur
      graal
      perceval
      perceval-mozilla
      perceval-opnfv
      perceval-puppet
      perceval-finos
      sortinghat
      sigils
      kidash
      toolkit
      cereslib
      manuscripts
      )

for i in ${!repos[@]}
do
	echo -e `expr $i + 1` "\n>>> opening repo"
	cd grimoirelab-"${repos[i]}"
	git checkout master
	echo -e "\n>>> checking remote"
	git remote -v
	echo -e "\n>>> checking for changes in upstream"
	git fetch upstream
	echo -e "\n>>> merging changes with master"
	git rebase upstream/master
	echo -e "\n>>> git push"
	git push https://vchrombie:plmoknijb88%40@github.com/vchrombie/grimoirelab-"${repos[i]}"
	git pull
	echo
	cd ..
done

ls

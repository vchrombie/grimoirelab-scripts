#!/usr/bin/env bash

mkdir sources
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
      sortinghat
      sigils
      kidash
      toolkit
      )

for i in ${!repos[@]}
do
	echo -e `expr $i + 1` "\n>>> cloning ${repos[i]}"
	git clone https://github.com/vchrombie/grimoirelab-"${repos[i]}"
	echo -e "\n>>> adding remote"
	cd grimoirelab-"${repos[i]}"
	git remote -v
	git remote add upstream https://github.com/chaoss/grimoirelab-"${repos[i]}"
	echo -e "\n>>> remote added"
	git remote -v
	echo
	cd ..
done

echo -e `expr 14 + 1` "\n>>> cloning perceval-finos"
git clone https://github.com/vchrombie/grimoirelab-perceval-finos
echo -e "\n>>> adding remote"
cd grimoirelab-perceval-finos
git remote -v
git remote add upstream https://github.com/Bitergia/grimoirelab-perceval-finos
echo -e "\n>>> remote added"
git remote -v
echo
cd ..

ls

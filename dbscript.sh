mysql -u root -p -e "create database test_sh"
mysql -u root -p -e "create database test_projects"
mysql -u root -p test_projects < sources/grimoirelab-elk/tests/test_projects.sql


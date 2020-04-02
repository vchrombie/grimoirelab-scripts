sudo apt --purge remove mariadb-server
sudo apt --purge remove mysql
sudo apt autoremove
sudo apt autoclean
sudo apt update
sudo apt install mariadb-server
mysql -V
echo -e "\n\nchecking status\npress q to quit\n\n"
sudo systemctl status mariadb
sudo mysql_secure_installation

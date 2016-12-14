# Kill previous instances
sudo pkill -f httpd
sudo pkill -f run.py
sudo pkill -f flaskr.py
sudo pkill -f python
sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/app_server_nginx.conf
sudo rm /etc/nginx/sites-available/api_server_nginx.conf

sudo cp ~/cs207project/conf/app_server_nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/app_server_nginx.conf /etc/nginx/sites-enabled/app_server_nginx.conf

sudo service nginx restart

printf "\nMoving Repos Assets to www...\n"

# Recreate  /home/www
sudo rm -r /home/www
sudo mkdir /home/www

sudo rm /home/www/cs207project -r
# Need to import the whole project
sudo cp ~/cs207project /home/www/ -r

printf "\nStarting Application Servers...\n"

cd ~/cs207project/cs207project/tsrbtreedb
sudo nohup python3 socket_server.py &
#echo "Socket Server Started"

cd ~/cs207project/cs207project/flask

sudo  nohup python3 run.py &
#echo "REST API Server Started"

sudo mkdir /home/www/DB

# Permissions needed to be given, if not write/delete of files cannot be done
sudo chmod 777 -R /home/www
#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static

# Install nginx if it is not already installed
if ! which nginx > /dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo chown -R ubuntu:ubuntu /data/

# Create fake HTML file
echo "<html><head><title>Test Page</title></head><body>This is a test page.</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update nginx configuration
sudo sed -i '/listen 80 default_server;/a location /hbnb_static {\nalias /data/web_static/current/;\n}' /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart

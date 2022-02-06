#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static. It must:
# Install Nginx if it not already installed
# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/shared/ if it doesn’t already exist
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
# Use alias inside your Nginx configuration
# Tip
# Your program should always exit successfully. Don’t forget to run your script on both of your web servers.
sudo apt-get update && sudo apt-get install -y nginx
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared/
printf "\
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu /data/ && chgrp -R ubuntu /data/
sudo sed -i "/listen 80 default_server;/a \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default
sudo service nginx restart

# run all commands with sudo in beginning for permission issues
sudo apt-get update
sudo apt-get install docker.io
sudo apt-get install docker-compose

sudo docker build -t like_comments_i3 .
sudo docker run like_comments_i3
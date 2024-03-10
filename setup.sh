# run all commands with sudo in beginning for permission issues
sudo apt-get update
sudo apt-get install docker.io
sudo apt-get install docker-compose

sudo git clone https://github.com/Sahilvohra58/Insta_engagement_bot.git
cd Insta_engagement_bot
sudo docker-compose up -d

# sudo docker build -t like_comments_i3 .
# sudo docker run like_comments_i3
# sudo rm -rf Insta_engagement_bot
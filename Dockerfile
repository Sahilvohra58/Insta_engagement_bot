# https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py-alpine/3.10-alpine-selenium/Dockerfile
# https://www.youtube.com/watch?v=H0kQL_KHt3o
# https://www.youtube.com/watch?v=mz32F3R0AkU
# docker build -t northamerica-northeast2-docker.pkg.dev/ai-video-editor/like-comments-repo/like_comments_demo:latest .
# docker run northamerica-northeast2-docker.pkg.dev/ai-video-editor/like-comments-repo/like_comments_demo:latest
# docker push northamerica-northeast2-docker.pkg.dev/ai-video-editor/like-comments-repo/like_comments_demo:latest
# docker rm -v $(docker ps --filter status=exited -q)
# docker rmi -f $(docker images -aq)

# Push code to artifact registry - create a cloud run job (not service) - schedule the run with cloud scheduler with cron "1 8,9,10,11,16,17,18,21,22,23 * * *"

FROM python:3.10

WORKDIR /app
COPY . /app

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium==4.9.1
RUN pip install webdriver_manager==4.0.0

CMD [ "/bin/bash" ]
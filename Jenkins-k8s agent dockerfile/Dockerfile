FROM jenkins/inbound-agent:latest

USER root

# install packages
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install sudo curl bash jq python3 python3-pip \
    && apt-get install sshpass \
    && apt-get install -y zip

# Installing aws cli (Official)
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install -i /usr/local/aws-cli -b /usr/local/bin
RUN aws --version

# install AWS CLI using pip -- Didn't work
# RUN set +x \
#   && pip3 install awscli --upgrade

RUN apt-get update && apt-get install -y apt-transport-https \
       ca-certificates curl gnupg2 \
       software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

RUN echo "yes" | echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
# Installing docker
RUN apt-get -y update && apt-get install -y docker-ce-cli

# Adding kubectl 
RUN apt-get install -y apt-transport-https ca-certificates curl
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
RUN echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# RUN apt-get -y update && apt-get install -y python3-boto3
# # Updating the apt repos
# RUN apt-get update  -qq 
# RUN apt-get -y update && apt-get install openjdk-11-jdk -y

# Installing kubectl
RUN apt-get update
RUN apt-get install -y kubectl


RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - &&\
    apt install nodejs -y
RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4 -y
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN apt-get update -y
# RUN apt-get install mysql-client  -y
# RUN apt-get -y update && apt-get install openjdk-11-jdk -y

# Install mongodb cli
RUN sudo apt-get install gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN sudo apt-get update
RUN sudo apt-get install -y mongocli
RUN sudo apt-get install gnupg curl
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
--dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN sudo apt-get update
RUN sudo apt-get install -y mongodb-org
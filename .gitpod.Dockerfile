FROM gitpod/workspace-full-vnc

USER root
# installing firefox
RUN apt-get update && apt install -y firefox 

RUN echo $(firefox -v|more)

# installing pip3 
RUN apt-get install -y python3-pip 
RUN apt install -y curl

# installing wget
RUN apt-get install -y curl unzip wget


# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app
COPY . .

# set ENV for python ascii
ENV PYTHONIOENCODING=utf8

# installing pip3 packages
RUN pip3 install scrapy
RUN pip3 install selenium
RUN pip3 install boto3
RUN pip3 install pandas
# RUN pip3 install scrapy-selenium
RUN pip3 install scrapy-selenium

# Then install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin
RUN geckodriver --version

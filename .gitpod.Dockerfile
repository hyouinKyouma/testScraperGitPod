FROM gitpod/workspace-full

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
RUN apt-get update && apt install -y firefox 
RUN echo $(firefox -v|more)

# installing pip3 packages
RUN pip3 install scrapy
RUN pip3 install boto3
RUN pip3 install pandas
# RUN pip3 install scrapy-selenium
RUN pip3 install scrapy-selenium

# Then install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin
RUN geckodriver --version

# run spider
CMD ["scrapy", "crawl", "arekere"]
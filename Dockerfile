FROM selenium/standalone-chrome:latest

WORKDIR /home/pixieapp

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python3", "./bot.py"]
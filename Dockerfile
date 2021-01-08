FROM python:3.7

RUN mkdir -p /usr/src/flaskServer
COPY . /usr/src/flaskServer
WORKDIR /usr/src/flaskServer

RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /usr/src/flaskServer/requirements.txt

RUN apt update
RUN apt install -y libgl1-mesa-glx

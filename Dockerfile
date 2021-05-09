FROM python:3.7

WORKDIR /usr/src/flaskServer

COPY . /usr/src/flaskServer

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /usr/src/flaskServer/requirements.txt

CMD ["/bin/bash", "-c", "/usr/src/flaskProxy/launch_service.sh"]
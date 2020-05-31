FROM python:3.7

RUN mkdir -p /usr/src/flaskServer
WORKDIR /usr/src/flaskServer
COPY requirements.txt /usr/src/flaskServer
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /usr/src/Proxy_Server/requirements.txt
COPY . /usr/src/flaskServer

CMD ["gunicorn", "-c", "/usr/src/flaskServer/gunicorn.py", "manager:app"]

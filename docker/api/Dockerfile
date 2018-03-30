FROM python:3.6

RUN apt-get update && pip install -U pip

RUN mkdir -p /etc/pyse2018/ /source/

COPY requirements/base.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /source
COPY docker-config.ini /etc/pyse2018/pyse2018.ini

ENTRYPOINT /source/entrypoint-api.sh
EXPOSE 80

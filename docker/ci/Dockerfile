FROM python:3.6

RUN mkdir -p /etc/pyse2018/ /source/

COPY requirements/ /requirements/
RUN pip install -r /requirements/dev.txt

COPY . /source
COPY docker-config.ini /etc/pyse2018/pyse2018.ini

ENTRYPOINT /source/entrypoint-ci.sh

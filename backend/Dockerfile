#cotainer 실행시 옵션 추가: --platform linux/amd64 

FROM --platform=linux/amd64 ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
 dpkg --purge --force-depends ca-certificates-java && \
 apt-get install ca-certificates-java -y && \
 apt-get install software-properties-common -y && \
 add-apt-repository ppa:deadsnakes/ppa -y && \
 apt-get -y install tzdata && \
 apt-get install python3.8 -y && \
 apt-get install python3-pip -y && \
 apt-get install openjdk-8-jdk -y && \
 apt-get install curl gcc -y && \
 apt-get install wget -y && \
 apt-get install git -y && \
 apt-get install automake -y && \
 apt-get install autoconf -y && \
 apt-get install autotools-dev -y

RUN curl -L https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash

RUN cd /tmp && \
  wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz && \
  tar xvf mecab-0.996-ko-0.9.2.tar.gz && \
  cd /tmp/mecab-0.996-ko-0.9.2 && \
  ./configure && \
  make check && \
  make install

RUN apt-get install libffi-dev -y

RUN pip3 install gunicorn

COPY ./requirements.txt /backend/requirements.txt

RUN pip3 install -r /backend/requirements.txt

COPY ./ /backend/

CMD ["bash", "-c", "cd /backend && python3 manage.py migrate && gunicorn -w 3 --bind 0:2102 backend.wsgi"]
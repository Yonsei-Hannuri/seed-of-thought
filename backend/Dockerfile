#cotainer 실행시 옵션 추가: --platform linux/amd64 

# debian bullseye 버전, python이 설치된 base 이미지
FROM --platform=linux/amd64 python:3.8-slim-bullseye

# 빌드시 사용자 입력을 요구하는 것을 방지하는 설정
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y

RUN apt-get install build-essential -y
RUN apt-get install libpoppler-cpp-dev -y
RUN apt-get install pkg-config -y
RUN apt-get install python3-dev -y 

# install python packages
COPY ./requirements.txt /backend/requirements.txt
RUN pip3 install -r /backend/requirements.txt

COPY ./ /backend/

CMD ["bash", "-c", "cd /backend && python3 manage.py migrate && gunicorn --timeout 120 -w 1 --bind 0:2102 backend.wsgi"]
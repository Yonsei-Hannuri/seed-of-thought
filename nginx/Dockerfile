FROM nginx:latest

#/hannuri 볼륨을 host랑 공유하게 하면 된다. for uploadedfile and serving frontend
VOLUME /hannuri

RUN apt-get update && \
  apt-get-repository ppa:certbot/certbot && \
  apt-get install -y python3-certbot-nginx && \
  certbot --nginx -d hannuri.xyz -d www.hannuri.xyz -d pag.hannuri.xyz


#RUN certbot --authenticator webroot -w /usr/share/nginx/html --installer nginx -d hannuri.xyz --email jnh03336@gmail.com 

EXPOSE 80
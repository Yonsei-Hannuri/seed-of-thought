cd /deploy

sudo docker stop hannuri-api || true
sudo docker rm hannuri-api || true
sudo docker image rm hannuri-api || true
sudo docker load -i hannuri-api.tar
sudo docker run -d --platform linux/amd64 -p 2999:2102 -v /home/hannuri/log:/backend/log -v /home/hannuri/db:/backend/db --network hannuri-net --name hannuri-api hannuri-api
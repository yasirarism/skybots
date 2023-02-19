### If you are trying to lazy which you should not! (Deploying to Heroku)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/newkanekibot/skybots)

#### Build And Run The Docker Image Using Official Docker Commands

- Start Docker daemon (SKIP if already running):
```
sudo dockerd
```
- Build Docker image:
```
sudo docker build . -t skybot
```
- Run the image:
```
sudo docker run skybot
```
- To stop the running image:
```
sudo docker ps
```
```
sudo docker stop id
```

----

#### Build And Run The Docker Image Using docker-compose

```
sudo apt install docker-compose
```
- Build and run Docker image or to view current running image:
```
sudo docker-compose up
```
- After editing files with nano for example (nano start.sh):
```
sudo docker-compose up --build
```
- To stop the running image:
```
sudo docker-compose stop
```
- To run the image:
```
sudo docker-compose start
```

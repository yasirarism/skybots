FROM ubuntu:22.10

ENV PYTHONWARNINGS="ignore"
ENV DEBIAN_FRONTEND="noninteractive" TZ="Asia/Jakarta"
RUN apt upgrade -y
RUN apt update -y
RUN apt-get install python3 python3-pip python3-lxml git tzdata wget curl ffmpeg -y

COPY . .
RUN pip3 install -r requirements.txt
# Set CMD Bot
CMD ["python3", "main.py"]

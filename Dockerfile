FROM ubuntu:16.04

MAINTAINER Tiyn tiyn@martenkante.eu

RUN apt-get update

RUN apt-get upgrade -y

RUN apt-get install python3 python3-pip -y

COPY src /blog

WORKDIR /blog

RUN pip3 install -r requirements.txt

VOLUME /blog/templates/entry

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

FROM ubuntu

MAINTAINER Tiyn tiyn@martenkante.eu

RUN apt-get update

RUN apt-get install python3 python3-pip git -y

RUN git clone https://github.com/tiyn/flaskblog /blog

WORKDIR /blog/src

RUN pip3 install -r requirements.txt

VOLUME /blog/src/templates/entry

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

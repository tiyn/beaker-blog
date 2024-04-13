FROM python:3

MAINTAINER tiyn tiyn@mail-mk.eu

COPY src /blog

WORKDIR /blog

RUN pip3 install -r requirements.txt

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

VOLUME /blog/templates/entry

VOLUME /blog/static/graphics

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

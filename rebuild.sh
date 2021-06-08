#!/bin/sh
docker stop beaker-blog
docker rm beaker-blog
docker build . -t tiyn/beaker-blog
docker run --name beaker-blog \
    --restart unless-stopped \
    -p "5000:5000" \
    -e FLASK_ENV=development \
    -d tiyn/beaker-blog

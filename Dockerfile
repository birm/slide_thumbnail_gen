FROM ubuntu:trusty

RUN apt-get update

RUN apt-get install -y openslide-tools
RUN apt-get install -y python-openslide

RUN mkdir -p /var/src
COPY . /var/src

WORKDIR /var/src

CMD while true; do sleep 1000; done

#CMD python Thumbnails.py demo/manifest.csv

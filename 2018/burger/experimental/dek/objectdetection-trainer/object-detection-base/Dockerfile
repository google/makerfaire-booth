FROM tensorflow/tensorflow:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    git


RUN mkdir -p /opt
RUN git clone https://github.com/dakoner/models-1.git --branch softplacementdevlogging --single-branch /opt/tensorflow_models && cd /opt/tensorflow_models && git checkout 3cd7919a14c21419d1518d8151684af6948d2767
FROM tensorflow/tensorflow@sha256:bfadad8f2c80424d8d6059d3b8cd6947bf23111dc786fc33db72b56b632a1f28

RUN apt-get update && apt-get install -y --no-install-recommends \
    git 


RUN mkdir -p /opt
RUN git clone https://github.com/dakoner/models-1.git --branch softplacementdevlogging --single-branch /opt/tensorflow_models && cd /opt/tensorflow_models && git checkout 3cd7919a14c21419d1518d8151684af6948d2767
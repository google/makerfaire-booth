FROM object-detection-base-gpu

RUN apt-get install -y --no-install-recommends \
    python-tk

COPY scripts/eval.sh /opt
ENTRYPOINT ["/opt/eval.sh"]

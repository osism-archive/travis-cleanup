FROM python:3.7-alpine

COPY requirements.txt /requirements.txt
COPY src/main.py /usr/local/bin/travis-cleanup

RUN apk add --no-cache --virtual .build-deps \
      build-base \
      libffi-dev \
      openssl-dev \
      python3-dev \
    && apk add --no-cache tini \
    && pip install -r requirements.txt \
    && chmod +x /usr/local/bin/travis-cleanup \
    && echo "*/30 * * * * travis-cleanup" > /etc/crontabs/root \
    && rm /requirements.txt \
    && apk del .build-deps

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/sbin/crond", "-f", "-d", "8"]

FROM ruby:3.0-alpine

ARG VERSION=0.8.2

RUN apk add --no-cache build-base sqlite-libs sqlite-dev && \
    gem install mailcatcher -v $VERSION && \
    apk del --rdepends --purge build-base sqlite-dev

EXPOSE 1025 80

ENTRYPOINT ["mailcatcher", "--foreground"]
CMD ["--ip", "0.0.0.0", "--http-port", "80"]
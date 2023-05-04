FROM lscr.io/linuxserver/firefox:latest

RUN python3 -m ensurepip --default-pip
RUN python3 -m pip install requests
RUN chown -R abc:users /config

COPY ./tools /tools
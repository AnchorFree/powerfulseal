FROM python:3

COPY . /code
WORKDIR /code
RUN python3 setup.py install
RUN python3 setup.py install_lib

ENTRYPOINT ["/usr/local/bin/powerfulseal"]

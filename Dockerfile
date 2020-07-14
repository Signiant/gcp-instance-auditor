FROM python:3.8-slim

RUN pip install google-api-python-client

RUN mkdir /src

COPY audit.py /src/

WORKDIR /src

ENTRYPOINT ["python","/src/audit.py"]

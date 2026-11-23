FROM alpine:latest
LABEL maintainer "Stephan Richter <stephan.richter@uni-jena.de>"
RUN apk add bash python3 py3-fastapi py3-yaml uvicorn
WORKDIR /opt/crc/Backend
EXPOSE 8000
CMD python server.py
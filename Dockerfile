FROM docker.io/alpine:latest
LABEL maintainer "Stephan Richter <stephan.richter@uni-jena.de>"
RUN apk add bash npm python3 py3-fastapi py3-pymysql py3-pip py3-yaml uvicorn
EXPOSE 8000
COPY <<EOF /launch
#!/bin/bash
cd /opt/crc/Frontend
npm install
npm run dev -- --host 2>&1 >/dev/null &
cd /opt/crc/Backend
python server.py
EOF
RUN chmod +x /launch
CMD /launch
EXPOSE 5173 8000
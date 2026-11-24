FROM docker.io/alpine:latest
LABEL maintainer "Stephan Richter <stephan.richter@uni-jena.de>"
RUN apk add bash npm python3 py3-fastapi py3-pymysql py3-pip py3-yaml uvicorn
EXPOSE 8000
RUN echo '#!/bin/bash' > /launch \
 && echo 'cd /opt/crc/Frontend' >> /launch \
 && echo 'npm install' >> /launch \
 && echo 'npm run dev -- --host 2>&1 >/dev/null &' >> /launch \
 && echo 'cd /opt/crc/Backend' >> /launch \
 && echo 'python server.py' >> /launch
RUN chmod +x /launch
CMD /launch
EXPOSE 5173 8000
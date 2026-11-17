FROM alpine:3.22
LABEL Maintainer "Stephan Richter"
RUN apk add bash npm
ADD script /opt
CMD /bin/bash

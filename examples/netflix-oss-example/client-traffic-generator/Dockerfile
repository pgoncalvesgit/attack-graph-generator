#
# Dockerfile for Service C
#

FROM java:8

MAINTAINER Oreste Luci

# Install netcat
RUN apt-get update && apt-get install -y netcat

VOLUME /tmp

WORKDIR /client-traffic-generator

# Not working so changed for something else.
# ADD target/client-traffic-generator.jar client-traffic-generator.jar
ARG JAR_FILE
ADD ${JAR_FILE} client_traffic_generator.jar

RUN bash -c 'touch /client-traffic-generator.jar'

ADD run.sh run.sh
RUN chmod 744 run.sh

CMD ["./run.sh","client-traffic-generator.jar"]

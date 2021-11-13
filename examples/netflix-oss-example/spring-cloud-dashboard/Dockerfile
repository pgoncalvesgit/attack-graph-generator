#
# Dockerfile for Turbine
#

FROM java:8

MAINTAINER Oreste Luci

# Install netcat
RUN apt-get update && apt-get install -y netcat

VOLUME /tmp

WORKDIR /spring-cloud-dashboard

# Not working so changed for something else.
# ADD target/spring-cloud-dashboard.jar spring-cloud-dashboard.jar
ARG JAR_FILE
ADD ${JAR_FILE} spring-cloud-dashboard.jar

RUN bash -c 'touch /spring-cloud-dashboard.jar'

ADD run.sh run.sh
RUN chmod 744 run.sh

EXPOSE 8086
CMD "./run.sh"

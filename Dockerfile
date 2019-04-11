FROM ubuntu:18.04
MAINTAINER Kemele M. Endris <keme686@gmail.com>

USER root

# Python 3.6 and Java 8 installation
RUN apt-get update && \
    apt-get install -y --no-install-recommends nano wget git curl less && \
    apt-get install -y --no-install-recommends python3.6 python3-pip python3-setuptools && \
    pip3 install --upgrade pip && \
    apt-get install -y --no-install-recommends openjdk-8-jdk openjdk-8-jre-headless && \
    apt-get clean

RUN mkdir /KG-Testbed
WORKDIR  /KG-Testbed

COPY . /KG-Testbed

RUN cd /KG-Testbed/tools && \
    wget https://github.com/RMLio/rmlmapper-java/releases/download/v4.3.3/rmlmapper-4.3.3-r92.jar && \
    mv rmlmapper-4.3.3-r92.jar rmlmapper.jar && \
    cd ..
RUN cd /KG-Testbed/tools && \
   wget https://github.com/SDM-TIB/TIB-RDFizer/archive/v0.1.zip && \
   unzip v0.1.zip && \
   mv TIB-RDFizer-0.1 rdfizer-master &&  cd rdfizer-master/rdfizer && \
   pip3 install -r requirements.txt && \
   cd /KG-Testbed

CMD ["/KG-Testbed/reproduce.sh"]

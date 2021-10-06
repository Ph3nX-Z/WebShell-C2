FROM ubuntu

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt -yq upgrade

RUN mkdir /home/webshell-C2/
COPY ./ /home/webshell-C2/
WORKDIR /home/webshell-C2/

RUN apt-get -yq install python3
RUN apt-get -yq install python3-pip
RUN pip3 install flask


EXPOSE 80
CMD ["python3","server.py","&"]

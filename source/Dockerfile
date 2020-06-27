FROM ubuntu

RUN apt-get update
RUN apt-get install python -y
RUN apt-get install spin -y
RUN apt-get install gcc -y
RUN apt-get install python3-venv python3-pip -y

RUN pip3 install numpy
RUN pip3 install sklearn
RUN pip3 install pandas

COPY . /opt/source-code

ENTRYPOINT cd /opt/source-code ; cat readme ; bash
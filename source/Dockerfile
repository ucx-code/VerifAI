FROM ubuntu

RUN apt-get update
RUN apt-get install python -y
RUN apt-get install spin -y
RUN apt-get install gcc -y
RUN apt-get install python3-venv python3-pip -y

RUN pip3 install numpy
RUN pip3 install sklearn
RUN pip3 install pandas

COPY ./source /opt/source-code
RUN chmod u+x /opt/source-code/examples-for-explaining-approach/run.bash
RUN rm /opt/source-code/Dockerfile

ENTRYPOINT cd /opt/source-code ; cat readme ; bash
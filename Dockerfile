# Instructions copied from - https://hub.docker.com/_/python/
FROM python:3-onbuild

#RUN apt-get update
#RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev gfortran
#RUN pip install --upgrade pip
#RUN pip install numpy==1.14.3
#RUN pip install scipy==1.1.0

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./gfi_1.py"]

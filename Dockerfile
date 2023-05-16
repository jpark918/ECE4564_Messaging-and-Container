##Deriving the latest base image
#FROM python:latest
#
#ADD ServerP3.py .
#ADD ServerKeys.py .
#ADD ClientKeys.py .
#COPY ./requirements.txt /C:/Users/Jihoon/Downloads/ECE_4564_NetAppDes/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /C:/Users/Jihoon/Downloads/ECE_4564_NetAppDes/requirements.txt
#CMD ["python", "./ServerP3.py"]
#----
#Deriving the latest base image
FROM python:latest

ADD ClientP3.py .
ADD ClientKeys.py .
#WORKDIR /code

#COPY ./requirements.txt /code/requirements.txt
COPY ./requirements.txt /C:/Users/Jihoon/Downloads/ECE_4564_NetAppDes/requirements.txt

#RUN python3 -m pip install -r /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /C:/Users/Jihoon/Downloads/ECE_4564_NetAppDes/requirements.txt
#RUN pip install -r requirements.txt

#COPY ./ECE_4564_NetAppDes /code/ECE_4564_NetAppDes

CMD ["python", "./ClientP3.py"]
#-------------------------------------------
#pip freeze > requirements.txt (will create a txt with all imports inside it)
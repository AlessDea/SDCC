# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
RUN pip install grpcio
RUN pip install google-api-python-client
RUN pip install mysql-connector-python-rf
RUN pip install pika
RUN pip install pybreaker

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["groupmanager.py"]

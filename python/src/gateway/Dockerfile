# select base image
FROM python:3.10-slim-bullseye

# install updates without additinal packages
RUN apt-get update \
	&& apt-get install -y --no-install-recommends --no-install-suggests \
	build-essential \
	&& pip install --no-cache-dir --upgrade pip

# create app directory	
WORKDIR /app
# install requirements first
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
# copy everything to the app directory
COPY . /app

# make port 8080 available to inter-container communication
EXPOSE 8080

# run server
CMD ["python3", "server.py"]

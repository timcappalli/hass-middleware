FROM python:3.8-slim-buster

LABEL maintainer="@timcappalli"
LABEL version="2020.07.09"

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . /app

CMD [ "python", "app.py" ]
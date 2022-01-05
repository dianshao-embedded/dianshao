# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /app/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
COPY ./src/requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# copy project
COPY ./src .

# CMD will run when this dockerfile is running
CMD ["sh", "-c", "python manage.py migrate;"]

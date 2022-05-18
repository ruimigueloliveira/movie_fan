
FROM python:3.8-alpine


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add gcc python3-dev musl-dev

RUN mkdir /app

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY ./src/   /app

CMD ["python", "manage.py", "runserver" ,"0.0.0.0:8080"]
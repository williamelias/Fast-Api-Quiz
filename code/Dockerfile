FROM python:3.10-slim-bullseye

WORKDIR /code

RUN apt-get update && apt-get install make

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade  -r /code/requirements.txt 

COPY ./app /code/app
COPY ./entrypoint.sh /code

# ENTRYPOINT [ "entrypoint.sh" ]

EXPOSE 8082

CMD [ "uvicorn", "app.main:app","--host","0.0.0.0", "--port", "8082", "--reload" ]
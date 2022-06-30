FROM python:3

WORKDIR /code/app

EXPOSE 8000

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY .env /code/app/.env

CMD ["python", "main.py"]
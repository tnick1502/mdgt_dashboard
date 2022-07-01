FROM python:3.9

WORKDIR /code

EXPOSE 80

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --user --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code

COPY ./.env /code/.env

CMD ["python", "bot.py"]
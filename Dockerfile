FROM python:3

WORKDIR /code/app

EXPOSE 8001

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["python", "main.py"]
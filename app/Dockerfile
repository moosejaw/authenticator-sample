FROM python:3.8.5-slim
WORKDIR /usr/src/app

COPY ./*.py ./
COPY ./modules/ ./modules/
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

CMD gunicorn -w $NUM_WORKERS -b 0.0.0.0:$WEBAPP_PORT wsgi:app --preload
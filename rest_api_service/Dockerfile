FROM python:3

WORKDIR /usr/src/app

COPY ./rest_api_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./rest_api_service .
COPY ./entity_classes ./entity_classes
COPY ./shared_utils ./shared_utils
COPY  config.yml .
COPY ./files ./files

CMD ["python", "./app.py"]
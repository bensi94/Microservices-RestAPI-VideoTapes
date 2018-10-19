FROM python:3

WORKDIR /usr/src/app

COPY ./database_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./database_service ./database_service
COPY ./entity_classes ./entity_classes
COPY ./shared_utils ./shared_utils
COPY  config.yml .
COPY ./files ./files
RUN chmod +x ./database_service/run-nameko.sh

CMD ["./database_service/run-nameko.sh"]
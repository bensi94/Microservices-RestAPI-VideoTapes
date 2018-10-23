FROM python:3

WORKDIR /usr/src/app

COPY ./tests/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./tests .
COPY ./database_service ./database_service
COPY ./shared_utils ./shared_utils
COPY ./entity_classes ./entity_classes
COPY  config.yml .
COPY ./files ./files
RUN chmod +x run-tests.sh

CMD ["./run-tests.sh"]
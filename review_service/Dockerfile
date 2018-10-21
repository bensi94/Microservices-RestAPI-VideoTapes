FROM python:3

WORKDIR /usr/src/app

COPY ./review_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./review_service ./review_service
COPY ./entity_classes ./entity_classes
COPY ./shared_utils ./shared_utils
COPY  config.yml .
COPY ./files ./files
RUN chmod +x ./shared_utils/run-nameko.sh

CMD ["./shared_utils/run-nameko.sh"]
#!/bin/bash

# Check if rabbit is up and running before starting the service.

RABBIT_URL="http://${RABBIT_USER:-guest}:${RABBIT_PASSWORD:-guest}@${RABBIT_HOST:-localhost}:${RABBIT_MANAGEMENT_PORT:-15672}/api/vhosts"

is_ready() {
    eval "curl -I ${RABBIT_URL}"
}

i=0
while ! is_ready; do
    i=`expr $i + 1`
    if [ $i -ge 10 ]; then
        echo "$(date) - rabbit still not ready, giving up"
        exit 1
    fi
    echo "$(date) - waiting for rabbit to be ready"
    sleep 3
done

# Run Service

<<<<<<< HEAD
py.test --disable-pytest-warnings -v  -s ./
=======
py.test --disable-pytest-warnings -v  -s ./test_tape.py
>>>>>>> 32aa3400ca45068ad7a3dbdb5a9b8f91303bb19a

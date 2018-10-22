import os
CONFIG = {'AMQP_URI': 'amqp://' +
          os.environ['RABBIT_USER'] + ':' + os.environ['RABBIT_PASSWORD'] + '@' + os.environ['RABBIT_HOST']}


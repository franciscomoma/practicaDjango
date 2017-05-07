# -*- coding: utf-8 -*-
import pika
from django.conf import settings


def publish(exchange, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.AMQP_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, type='fanout')
    channel.basic_publish(exchange=exchange, routing_key='', body=body)

    connection.close()

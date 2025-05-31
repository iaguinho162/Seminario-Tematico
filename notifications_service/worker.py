import pika

def callback(ch, method, properties, body):
    print(f" [x] Notificação recebida: {body.decode()}")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()

channel.queue_declare(queue='order_notifications')

channel.basic_consume(
    queue='order_notifications',
    on_message_callback=callback,
    auto_ack=True
)

print(' [*] Aguardando notificações. CTRL+C para sair')
channel.start_consuming()

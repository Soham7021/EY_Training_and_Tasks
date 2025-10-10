import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='student_tasks')

task = {
    'student_id':101,
    'action': 'Generate_Certificate',
    'email': 'rahul@example.com'
}

channel.basic_publish(exchange='', routing_key='student_tasks', body=json.dumps(task))

print("task sent to ", task)
connection.close()
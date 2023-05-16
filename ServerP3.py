
import pika
import ClientKeys
from cryptography.fernet import Fernet
import pyttsx3
import wolframalpha
import ServerKeys
import pickle

def on_message_received(ch, method, properties, body):
    print("starting server")
    db = pickle.loads(body[10:])

    key = ClientKeys.Encryptionkey
    fernet = Fernet(db[1])
    # decrypt the encrypted string with the
    # Fernet instance of the key,
    # that was used for encrypting the string
    # encoded byte string is returned by decrypt method,
    # so decode it to string with decode methods
    decMessage = fernet.decrypt(db[2]).decode()

    print("decrypted string: ", decMessage)

    engine = pyttsx3.init()

    # We can use file extension as mp3 and wav, both will work
    engine.say(decMessage)
    engine.save_to_file(decMessage, 'speech.wav')

    # Wait until above command is not finished.
    engine.runAndWait()

    question = decMessage

    # App id obtained by the above steps
    app_id = ServerKeys.wolf_id

    # Instance of wolf ram alpha
    # client class
    client = wolframalpha.Client(app_id)

    # Stores the response from
    # wolf ram alpha
    res = client.query(question)

    # Includes only text from the response
    answer = next(res.results).text

    print(answer)
    encMessage = fernet.encrypt(answer.encode())
    db2 = {1: encMessage, 2: db[3]}
    # db = (key, encMessage, result)
    msg = pickle.dumps(db2)
    msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
    response = msg

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         properties.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='letterbox')
channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)
print("Starting Consuming")

channel.start_consuming()
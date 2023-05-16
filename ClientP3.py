import pika
import time
import subprocess
import tweepy
from cryptography.fernet import Fernet
import wolframalpha
import json
from os.path import join, dirname
import ClientKeys
import pyttsx3
import sys
import hashlib
import pickle
import time

repeat = 1
tweetindex = 0;
avgtwt = 0;
processtwt = 0;
start_time = 0;
avgtime = []

n = len(sys.argv) # needs to be 7 exact arguments
valid_cmd = False
if n == 7 or n == 1:
    valid_cmd = True
print(n)
bearer_token = ClientKeys.twitterbearer
screen_name = ClientKeys.twitterName

client = tweepy.Client(bearer_token)

twitterid = client.get_user(username=screen_name)
#print(type(twitterid))  # to confirm the type of object
#print(f"The Twitter ID is {twitterid.data.id}.")

# Get User's Tweets

# This endpoint/method returns Tweets composed by a single user, specified by
# the requested user ID

while (repeat == 1):

    user_id = twitterid.data.id

    response = client.get_users_tweets(user_id, max_results=20)

    try:
        tweetobj = response.data[tweetindex]
        tweetobj = tweetobj.text
        start_time = time.time()
    except:
        print("no more new tweets")

    #store all tweets in array
    #data = []
    #for i in range(0, len(tweetobj)):
        #data.append(response.data[i].text)

    brek = []
    for i in range(0, len(tweetobj)):
        if tweetobj[i] == '"':
            brek.append(i)
    if len(brek) != 2:
        print("You messed up the format ex: #ECE4564T18 “How old is the moon?”")

    brek[0] = brek[0] + 1
    hold = tweetobj[brek[0]:brek[1]]
    tweetobj = hold

    # By default, only the ID and text fields of each Tweet will be returned
    #for tweet in response.data:
     #   print(tweet.id)
      #  print(tweet.text)
    # By default, the 10 most recent Tweets will be returned
    # You can retrieve up to 100 Tweets by specifying max_results
    response = client.get_users_tweets(user_id, max_results=100)

    key = ClientKeys.Encryptionkey

    # Instance the Fernet class with the key

    fernet = Fernet(key)

    # then use the Fernet class instance
    # to encrypt the string, the string must
    # be encoded to byte string before encryption
    encMessage = fernet.encrypt(tweetobj.encode())
    decMessage = fernet.decrypt(encMessage).decode()

    result = hashlib.md5(encMessage)
    #print("The hexadecimal equivalent of hash is : ", end ="")
    #print(result.hexdigest())

    print("original string: ", tweetobj)
    #print("encrypted string: ", encMessage)
    db = {1:key, 2: encMessage, 3:result.digest()}
    #db = (key, encMessage, result)
    msg = pickle.dumps(db)
    msg = bytes(f"{len(msg):<{10}}", 'utf-8')+msg
    #print(msg)


    import pika
    import uuid
    class FibonacciRpcClient(object):

        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))

            self.channel = self.connection.channel()
            result = self.channel.queue_declare(queue='', exclusive=True)
            self.callback_queue = result.method.queue

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True)

            self.response = None
            self.corr_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = body

        def call(self, n):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='',
                routing_key='letterbox',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body = n)
            self.connection.process_data_events(time_limit=None)
            return self.response


    fibonacci_rpc = FibonacciRpcClient()

    #print(" [x] Requesting fib(30)")
    data = fibonacci_rpc.call(msg)

    db = pickle.loads(data[10:])
    decMessage = fernet.decrypt(db[1]).decode()
    #print(db)
    print("decrypted string: ", decMessage)
    hold = time.time() - start_time
    print("time to process tweet: ", hold)
    avgtime.append(hold)
    #engine = pyttsx3.init()

    # We can use file extension as mp3 and wav, both will work
    #engine.say(decMessage)
    #engine.save_to_file(decMessage, 'speech.wav')

    # Wait until above command is not finished.
    #engine.runAndWait()
    #print("Try again?: 1 for yes, 2 for no")
    answer = input('Try again?: 1 for yes, 2 for no \n')
    if (answer == '1'):
        repeat = 1
        tweetindex = tweetindex + 1
    else:
        repeat = 0

    if (tweetindex >= 20):
        performance = input('Print avg/min/max latency?: 1 for yes, 2 for no \n')
        if(performance == '1'):
            avgfinal = 0
            mintime = 0
            maxtime = 0
            firsttime = 0
            for i in avgtime:
                avgfinal = avgfinal + i
                if firsttime == 0: #intially store the first time as both min/max
                    mintime = i
                    maxtime = i
                    firsttime = 1
                if i < mintime: #check if smaller time exists
                    mintime = i
                if i > maxtime: #check if longer time exists
                    maxtime = i
            avgfinal = avgfinal/len(avgtime)
            print("avg latency: ", avgfinal)
            print("min latency: ", mintime)
            print("max latency: ", maxtime)

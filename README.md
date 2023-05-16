Specification: 
Project 3 is an extension to Project 2, which is a text-based question and answer system.
Questions to your Q&A system comes from Twitter Tweets and got answered by
WolframAlpha’s computational knowledge engine. The question and resulting answer are
“spoken” using IBM Watson’s text-to-speech (TTS) translation API.
The system uses two machines following the client/server model discussed in class. The
server is iterative and connection-oriented. Communication among client and server is handled
via stream-oriented sockets.
Updated Workflow
• The non-stopping client program captures a Twitter status object (Tweet) containing the
question text in a streaming mode.
• The client builds and sends a question “payload” to the server via gRPC or MQ.
• The server unpacks the payload, speaks the question, and sends the question to the
WolframAlpha engine and receives the answer.
• The server builds and sends an answer “payload” back to the client.
• The client unpacks the payload, speaks the answer, and displays the answer on the monitor.
• Two clients and one server are running in docker containers
• Clients and server run in different machines (while two clients can stay in the same
machine)
• Each client pulls at least 20 tweets, and records latency to process each tweet

Additional Information:
RabbitMQ is a message broker based on the AMQP protocol.
An exchange receives messsages from producers and pushes them to queues.

A Docker container is a standard unit of software that packages up code and all its dependencies
    * Allows applications to run quickly and reliably from one computing resource to another (migration!)
A docker container image isa lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libs, and settings.
    * It becomes containers at runtime
    * In the case of Docker containers = images become containers when they run on Docker Engine.

For our implementation, RabbitMQ has been used to send our question "payload" to the server

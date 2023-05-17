Specification: 
Project 3 is an extension to Project 2, which is a text-based question and answer system.
Questions to your Q&A system comes from Twitter Tweets and got answered by
WolframAlpha’s computational knowledge engine. The question and resulting answer are
“spoken” using IBM Watson’s text-to-speech (TTS) translation API.
The system uses two machines following the client/server model discussed in class. The
server is iterative and connection-oriented. Communication among client and server is handled
via stream-oriented sockets.

Updated Workflow
<br>
• The non-stopping client program captures a Twitter status object (Tweet) containing the
question text in a streaming mode. </br>
<br>
• The client builds and sends a question “payload” to the server via gRPC or MQ. </br>
<br>
• The server unpacks the payload, speaks the question, and sends the question to the
WolframAlpha engine and receives the answer. </br>
<br>
• The server builds and sends an answer “payload” back to the client. </br>
<br>
• The client unpacks the payload, speaks the answer, and displays the answer on the monitor. </br>
<br>
• Two clients and one server are running in docker containers </br>
<br>
• Clients and server run in different machines (while two clients can stay in the same
machine) </br>
<br>
• Each client pulls at least 20 tweets, and records latency to process each tweet </br>

<br> Additional Information: </br>
RabbitMQ is a message broker based on the AMQP protocol.
An exchange receives messsages from producers and pushes them to queues.

<br>
A Docker container is a standard unit of software that packages up code and all its dependencies </br>
    • Allows applications to run quickly and reliably from one computing resource to another (migration!) 
<br> A docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libs, and settings. </br>
    • It becomes containers at runtime 
    <br>
    • In the case of Docker containers = images become containers when they run on Docker Engine. </br>
<br>
For our implementation, RabbitMQ has been used to send our question "payload" to the server </br>

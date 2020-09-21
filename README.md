# DS Lab 6

**Student: Dmitry Podpryatov**

**Group: DS-02**

## Thread approach

Server is based on the code from [this repository](https://gist.github.com/gordinmitya/349f4abdc6b16dc163fa39b55544fd34).
Code has been added to the run method.

Client is based on the code from [this site](https://realpython.com/python-sockets/#echo-client) and 
from [question](https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python) on stack overflow.

## Usage

Server
```
python3 server.py
```

Client
```
python3 client.py <file> <host|ip> <port>
python3 client.py meme.jpg localhost 8800
```

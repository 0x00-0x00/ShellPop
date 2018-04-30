# ShellPop
## About
    Pop shells like a master
    Shell pop is all about popping shells. With this tools you can
    generate easy and sofisticated reverse or bind shell commands
    to help you during penetration tests.
    Don't wast more time with .txt files storing your Reverse shells!

-----
## Installation
```bash
root@kali# python setup.py install
```

## Module Index
* [List] (#shell-list)
* [Basics] (#basics)
* [Encoders] (#encoders)
* [Protocols] (#protocols)
* [Credits] (#credits)


-----
### __Shells List__
#### *List of shells*
You can list all available shellpop shells using the --list option.


#### *Command line example*
```bash
user@desktop$ shellpop --list
```

![ShellsList](img/list-section.JPG?raw=true)


### __Basics__
-----
#### *Shell Types*
There is two types of payloads in this program: Bind or Reverse.

-----
##### 1. Reverse shell
Reverse shells use your attacker machine to serve as the "server". In this type of payload, you need both --host and --port pointing back to your machine. A handler must be set.

-----
##### Bind shell
Bind shells use the remote host to serve the connection. In this type of payload, all you need is the --port option with a valid port number.


#### Command line examples
##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443
![Screenshot](img/photo9.JPG?raw=true)

##### Generating a Powershell TCP bind shell over port 1337
![Screenshot](img/photo13.JPG?raw=true)

-----
### __Encoders__
Encoders are special options that you can use while generating shellpop payloads.

There are, currently, three encoding methods that can be applied singularly, or concurrently, and they are:

1. XOR encoding

 Uses a random numeric key (1-255) to obfuscate the payload and add a decryption stub to decrypt it.

2. Base64 encoding
 Simple base64 encoding in payload data and add a decryption stub to decrypt it.

3. URL encoding

 Simple URL encode over the final payload.


#### *Command line examples*
##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 but using URL-encoding, suitable to use over HTTP protocol.
![Screenshot](img/photo10.jpg?raw=true)

##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 but encode it to base64 and set-up a wrapper to decode it. This helps when quotes are troublesome.
![Screenshot](img/photo11.jpg?raw=true)

##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 URL-encoded and encoded to base64 ... Yes, you know the drill!
![Screenshot](img/photo12.jpg?raw=true)

##### Generating a Powershell bind shell over port 1337 encoded in base64
![Screenshot](img/photo14.JPG?raw=true)

#### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 using --xor encoding.
![Screenshot](img/xor-encoding-example.JPG?raw=true)

#### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 using ALL methods of encoding!
![Screenshot](img/encoding-all-example.JPG?raw=true)

### __Protocols__
Currently there is support of two protocols to land your shells:

1. TCP
2. UDP

#### *Command line examples*
##### TCP is blocked but UDP is not? Let there be shell!
![Screenshot](img/photo15.jpg?raw=true)

### __Credits__

This code is authored by Andre Marques (@zc00l) and this project's contributors.

It is made open to public the moment it was released in this github.

Any damage caused by this tool don't make any contributor, including the author, of responsibility.

-----
Current contributors:
+ zc00l
+ touhidshaikh
+ lowfuel

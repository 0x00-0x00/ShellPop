# ShellPop
## About

Shellpop is all about popping shells. With this tool you can
generate easy and sophisticated reverse or bind shell commands
to help you during penetration tests.

Don't waste more time with .txt files storing your Reverse shells!
-----
## Installation
Python 2.7 is required. 

3.0+ version will not work.

**Required Dependencies Install**
```bash
root@kali# apt-get install python-argcomplete metasploit-framework -y
```
```bash
root@kali# pip install -r requirements.txt
```
**Setup Install**
```bash
root@kali# python setup.py install
```

**PS**: After installation, tab auto-complete will only work after restarting the terminal.

## Index
* [Help](#help-section)
* [List](#shells-list)
* [Basics](#basics)
* [Obfuscation](#obfuscation)
* [Encoders](#encoders)
* [Handlers](#handlers)
* [Meterpreter Shells](#meterpreter-shells-new)
* [Stagers](#stagers)
* [Protocols](#protocols)
* [Credits](#credits)
* [Team Members](#team-members)
* [Contributors](#contributors)

-----
### __Help Section__
To quickly list all available options of this tools, use --help.

#### *Command line examples*
```bash
root@kali# shellpop --help
```

![Screenshot](img/img-shell-help.JPG?raw=true)


-----
### __Shells List__
#### *List of shells*
You can list all available shellpop shells using the --list option.


#### *Command line example*
```bash
root@kali# shellpop --list
```

![ShellsList](img/img-shell-list.JPG?raw=true)

##### Auto-Complete [NEW]

Now shellpop has auto-complete feature. To use it, you need to forget about --number and (--reverse or --bind), just stick to --payload argument. Like the image below:

![Autocomplete](img/img-shell-autocomplete.JPG?raw=true)

### __Basics__
-----
#### *Copying it to clipboard*
Dont waste time. This tool is all about NOT wasting time. So you can use `--clip` option to all your generated payloads and get them automagically copied to your clipboard.

#### *Shell Types*
There is two types of payloads in this program: Bind or Reverse.

-----
##### 1. Reverse shell
Reverse shells use your attacker machine to serve as the "server". In this type of payload, you need both --host and --port pointing back to your machine. A handler must be set.

-----
##### 2. Bind shell
Bind shells use the remote host to serve the connection. In this type of payload, all you need is the --port option with a valid port number.


#### Command line examples
##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443
![Screenshot](img/img-shell-example-01.JPG?raw=true)

##### Generating a Powershell TCP bind shell over port 1337
![Screenshot](img/img-shell-example-02.JPG?raw=true)

---
### __Obfuscation__
There are currently two main methods of obfuscation available for your generated payloads:

1. *Variable renaming obfuscation*

__Replaces all variables in payload with randomly named ones. Applied to every payload automatically.__

![Screenshot](img/img-random-variables.JPG?raw=true)

2. *IPfuscation*

__Obfuscate the IP addresse and port used by the payload__

Coined by @vysecurity, IPfuscation is simply leveraging the little known fact that IP addresses can be converted to decimal, octal, and hexadecimal numbers, or a combination of all three, and still be used.

Port obfuscation is accomplished by replacing the port number with a mathematical expression that evaluates to the port number.

![Screenshot](img/img-ipfuscation-example.JPG?raw=true)

Here the IP address in the generated payload is a combination of different number bases. The first part in normal decimal notation, the second and third parts are 2 and 3 converted to octal with random zeros as padding, and the fourth part is 4 in hex, with some zeros as padding also. The selection of bases to use in each part of the IP address is randomized, as well as the number of zeros used as padding to hex and octal numbers.

The port is obfuscated by replacing 443 with an expression that evaluates to 443. This expression is generated randomly as well.

---
#### Size Concerns
Although IPfuscation is optional, random variable obfuscation is now automatically enforced on all payloads. If the size of the payload is a real concern, you can pass the `--obfuscate-small` option to have the payload be minimally increased in size by obfuscation. The variable names, IP address and port number will be significantly shorter when used with this option.

![Screenshot](img/img-small-obfuscation.JPG?raw=true)

-----
### __Encoders__
Encoders are special options that you can use while generating shellpop payloads.

There are, currently, three encoding methods that can be applied singularly, or concurrently, and they are:

1. *XOR encoding*

 __Uses a random numeric key (1-255) to obfuscate the payload and add a decryption stub to decrypt it.__

2. *Base64 encoding*

 __Simple base64 encoding in payload data and add a decryption stub to decrypt it.__

3. *URL encoding*

 __Simple URL encode over the final payload.__


#### *Command line examples*
##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 but using URL-encoding, suitable to use over HTTP protocol.
![Screenshot](img/img-shell-example-03.JPG?raw=true)

##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 but encode it to base64 and set-up a wrapper to decode it. This helps when quotes are troublesome.
![Screenshot](img/img-shell-example-04.JPG?raw=true)

##### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 URL-encoded and encoded to base64 ... Yes, you know the drill!
![Screenshot](img/img-shell-example-05.JPG?raw=true)

##### Generating a Powershell bind shell over port 1337 encoded in base64
![Screenshot](img/img-shell-example-06.JPG?raw=true)

#### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 using --xor encoding.
![Screenshot](img/img-shell-example-07.JPG?raw=true)

#### Generating a Python TCP reverse shell to IP 1.2.3.4 at port 443 using ALL methods of encoding!
![Screenshot](img/img-shell-example-08.JPG?raw=true)

-----
### __Handlers__
Handler is a mechanism to "handle" the act of serving a socket to receive the incoming connection or to connect itself to a server endpoint in a way to establish your shell.

Currently there is support of the following TCP handlers:
1. TCP PTY Handlers
2. TCP Meta-Handlers [NEW]

This means every TCP shell can have appended to their command-line argument the `--handler` option. Removing the necessity of the operator to spawn the handler (probably ncat or nc) by himself.

![Screenshot](img/handler.gif?raw=true)

### __Meterpreter Shells__ [NEW]
This feature was widely asked by people who used this tool. Now it is technically possible to upgrade all shellpop shells to meterpreter, as since 0.3.6, handler uses by default the Metasploit Framework to land shells.

![Meterpreter](img/handler-meterpreter.gif?raw=true)

-----
### __Stagers__
Stager is a mechanism of serving your payload in STAGES. Sometimes payload complexity or size can get troublesome. In such cases, you can craft a small payload which in turn can request and execute the bigger one.

Currently there is support of the following Stagers protocols:
1. HTTP


#### HTTP Stagers
ShellPop has the following set of HTTP stagers to fit in any scenario you would want:
1. Linux Stagers (Python, Perl, Wget and cURL)
2. Windows Stagers (Powershell, CertUtil, BitsAdmin and Cscript)

To use HTTP staging, append to your command line `--stager http` and, optionally, if you want to specify the HTTP server port, the `--http-port` flag will put your port number in front of the pre-defined ones.

![Screenshot](img/stager.gif?raw=true)

-----
### __Protocols__
Currently there is support of two protocols to land your shells:

1. TCP
2. UDP
3. ICMP (Nishang ICMP shell)

#### *Command line examples*
##### TCP is blocked but UDP is not? Let there be shell!
![Screenshot](img/img-shell-example-09.JPG?raw=true)

-----
### __Credits__

This code is authored by Andre Marques (@zc00l) and this project's contributors.

It is made open to public the moment it was released in this github.

Any damage caused by this tool don't make any contributor, including the author, of responsibility.

-----
### __Team Members__
+ Andre Marques ([zc00l](https://github.com/0x00-0x00))
+ Touhid M.Shaikh ([touhidshaikh](https://github.com/touhidshaikh))
+ Rοbеrt Εѕрі ([lowfuel](https://github.com/SouAquele))
-----
### __Contributors__
We really appreciate all Contributors.

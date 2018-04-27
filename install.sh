#!/bin/bash
# Installation script for ShellPop
# Written by zc00l

if [ $(id -u) != "0" ]; then
    echo "[!] Only root can install over /opt folder.";
    exit 1;
fi
if [ ! -d /opt/shellpop ]; then
    echo "Creating /opt/shellpop folder ...";
    mkdir -v /opt/shellpop;
else
    echo "Old installation detected. Flushing ....";
    rm /opt/shellpop/*.py
    if [ -f /opt/shellpop/shellpop ]; then
    	rm /opt/shellpop/shellpop
    fi
fi

echo "Installing components ...";
cp *.py shellpop /opt/shellpop; chmod +x /opt/shellpop/shellpop; ln -s /opt/shellpop/shellpop /usr/local/bin/shellpop

error=0;
components=("reverse.py" "shellpop" "bind.py");
for c in ${components[@]}; do
	if [ ! -f /opt/shellpop/${c} ]; then
		echo "[!] Could not find component in shellpop folder: ${c}"
		error=$((error+1));
	fi
done

if [ $error -eq 0 ]; then
	echo "[+] Everything went fine!";
	shellpop --list
fi



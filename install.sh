#!/bin/bash
if [ $(id -u) != "0" ]; then
    echo "Only root can install over /opt folder.";
    exit 1;
fi
if [ ! -d /opt/shellpop ]; then
    mkdir /opt/shellpop;
fi
cp shellpop /opt/shellpop; chmod +x /opt/shellpop/shellpop; ln -s /opt/shellpop/shellpop /usr/local/bin/shellpop

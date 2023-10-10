#!/bin/bash
source ~/Mini_Proyectos/bot_telegram/secret_bot_telegram
#TOKEN=""
#ID_USER=""
MESSAGE="No se ha pasado ningún mensaje"
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
if [ -n "$1" ]; then
	MESSAGE=$1
fi

curl -s -X POST $URL -d chat_id=$ID_USER -d text="$MESSAGE"

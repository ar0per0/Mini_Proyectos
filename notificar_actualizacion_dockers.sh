#!/bin/bash

#Lista dockers comprobar 2 setmanas
list2s=("vaultwarden/server" "jc21/nginx-proxy-manager")
#Excluir de la lista a comprobar (separar con | ex --> prova1|prova2)
all_exclude="ubuntu_ok|kasmweb/ubuntu-jammy-dind:1.13.0|octoprint/octoprint"


FILE_LOG="notificar_actualizacion_dockers.log"
message=""

count_image_docker(){
	local number=$(docker images | grep "$1" | wc -l)
	echo $number
}

docker_pull(){
	echo "docker pull $1"
	if [ $? != 0 ]; then
		message="$message
		          - Error comprobar $1."
		return 1 #false
	else
		return 0 #true
	fi
}

check_docker(){
	local name_docker=$(echo "$1" | cut -d':' -f1)
	local count_image=$(count_image_docker "$name_docker")
	if [ "$count_image" -gt 1 ]; then
		message="$message
		          - El $1 ya estaba pendiente."
		if $(docker_pull "$1"); then
			local count_image_pending_pull=$(count_image_docker "$name_docker")
			if [ "$count_image_pending_pull" -gt 2 ]; then
				local rm_image=$(docker images | grep "$name_docker" | awk 'NR==2 {print $3}')
				echo "docker image rm $rm_image"
			fi
		fi
	else
		if $(docker_pull "$1"); then
			local count_image_pull=$(count_image_docker "$name_docker")
			if [ "$count_image_pull" -gt 1 ]; then
				message="$message
				          - El $1 se puede actualizar."
			fi
		fi
	fi
}

check_size_disk(){
	local size=$(df --total | tail -n 1 | awk '{print $5}' | grep -oE '[0-9]+')
	echo "$size"
}



#### Listas a comprobar
if [ "$1" == "list2s" ]; then
	echo "$(date +%d/%m/%y) lanzado list2s" >> $FILE_LOG
	for item in "${list2s[@]}"; do
		check_docker $item
	done

elif [ "$1" == "all" ]; then
	echo "$(date +%d/%m/%y) lanzado all" >> $FILE_LOG
	all_dockers=$(docker images | awk 'NR > 1 {print $1 ":" $2}' | grep -v -E "$all_exclude" | sort | uniq)
	for line in $all_dockers; do
		if [ "$(check_size_disk)" -gt 90 ]; then
			message="$message
			          - Omitido $1 Disco duro > 90%"
		else
			check_docker $line
		fi
	done
fi

#### Notificar a telegram
if [ "$message" != "" ]; then
	echo "$(date +%d/%m/%y) mensaje: $message" >> $FILE_LOG
	message="🛠 Dockers actualizar:$message"
	~/Mini_Proyectos/bot_telegram/bot_telegram_message.sh "$message"
fi

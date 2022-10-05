
############ Help function ###########
Help(){
	echo "Usage: ./run.sh -p [HOST PORT] -c [CONTAINER PORT] -n [NAME]"
	echo "-p for the HOST PORT"
	echo "-c for the CONTAINER PORT"
	echo "-n for the container NAME"
}


while getopts p:c:n:h: flag
do
    case "${flag}" in
        p) host_port=${OPTARG};;
        c) container_port=${OPTARG};;
        n) container_name=${OPTARG};;
	h) Help
	exit;;
	\?) # Invalid option
         echo "Error: Invalid option"
         exit;;

    esac
done

if [[ -z $1  ||  -z $2 || -z $3 ]]
then
        echo "ERROR: -p, -c  and -n are mandatory arguments.";
        echo "Usage: $0 -p [HOST PORT] -c [CONTAINER PORT] -n [NAME]"
        echo "Try '$0 -h' for more information"
        exit 1;
fi

echo ${host_port}
echo ${container_port}
echo ${container_name}

docker build -t ${container_name} .
id=$(docker run -dp ${host_port}:${container_port} --name ${container_name} ${container_name})

docker network connect net1 ${id} --alias login

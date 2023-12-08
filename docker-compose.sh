# get env file path from arguments
env_file_path=$1

# function to show help menu
show_help() {
    echo "Usage: $0 <env_file_path>"
    echo "Example: ./docker-compose.sh .env"
}

# exit if env file path is not provided
if [ -z "$env_file_path" ]; then
    echo "\n\t* must provide env file path *\n"
    show_help
    exit 1
fi

# env file equal -h show help
if [ "$env_file_path" = "-h" ]; then
    show_help
    exit 0
fi

# exit if env file does not exit
if [ ! -f "$env_file_path" ]; then
    echo "env file does not exist"
    exit 1
fi

# set env - even though the docker-compose command takes the env file path as an argument,
# set the env variables here so that they override any provided by an IDE like VSCode
export $(cat $env_file_path | xargs)

docker-compose --env-file $env_file_path up -d

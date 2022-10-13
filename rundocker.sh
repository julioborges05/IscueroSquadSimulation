DEFAULT_DOCKER_IMAGE="squerosqad"
DEFAULT_CONTAINER_NAME="squerosqadcontainer"

WORK_DIR=`pwd`
CONTAINER_WORK_DIR=$WORK_DIR

CONTAINER_NAME=$DEFAULT_CONTAINER_NAME
DOCKER_IMAGE=$DEFAULT_DOCKER_IMAGE

# Executando o docker
docker run  -it \
            --rm \
            --name=$CONTAINER_NAME \
            --net=host \
            --privileged \
            --workdir="${CONTAINER_WORK_DIR}" \
            --volume="/dev:/dev" \
            --volume="${WORK_DIR}:${CONTAINER_WORK_DIR}" \
            $HOME/.Xauthority:/root/.Xauthority \
            $DOCKER_IMAGE

docker container rm $CONTAINER_NAME -f

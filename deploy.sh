IMAGE="evergiven.ury.york.ac.uk:5042/noticeboard"
CONTAINER="noticeboard"
PROJECTDIR="/opt/noticeboard"
LOGDIR="/mnt/logs/"
PORT=5042
DATE=$(date +%s)

docker build -t $IMAGE:$DATE .
docker push $IMAGE:$DATE
docker service update --image $IMAGE:$DATE noticeboard
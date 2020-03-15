#!/bin/bash
# Run producer or consumer containers

docker run -itd --name $1 --cap-add=NET_ADMIN --network kfk4_testNet4 --mount type=bind,source=/storage/hanwu/apps/4deliveryTest,target=/home/apps/deliveryTest kfk4_node:v2

#!/bin/bash

# $1 is the number of partitions, $2 is the number of replicas, $3 is the name

/home/apps/kafka/bin/kafka-topics.sh --list --bootstrap-server 172.29.0.3:9092,172.29.0.4:9092,172.29.0.2:9092

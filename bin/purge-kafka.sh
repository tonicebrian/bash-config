#!/bin/bash

if [ -z "$1" ]; then
    echo "Plese provide topic to purge...."
    exit 1
fi

KAFKA_FOLDER=$HOME/software/kafka
echo "Setting message retention to 500ms"
$KAFKA_FOLDER/bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name $1 --alter --add-config retention.ms=500

echo "Waiting for the purge to happen" && sleep 1

echo "Set retention to 10 minutes"
$KAFKA_FOLDER/bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name $1 --alter --add-config retention.ms=600000


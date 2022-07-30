#!/bin/bash
d=$(date +%Y-%m-%d)

if [ "$1" == hotitems ]; then
    echo "Run hotitem scrapy"
    scrapy crawl vgg-hotitems -O data/${d}.json
    exit 0
fi

if [ "$1" == games ]; then
    echo "Run games scrapy"
    scrapy crawl vgg-games -O data/${d}.json
    exit 0
fi

echo "missing an agv"
exit 1 
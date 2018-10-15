#!/usr/bin/env bash

rm ./snapshot/getAppListSnapshot.zip

cd ./env_steam/lib/python3.6/site-packages
zip -r9 ../../../../snapshot/getAppListSnapshot.zip .
cd ../../../../
zip -g ./snapshot/getAppListSnapshot.zip getAppList.py utils.py settings.yml

aws lambda update-function-code \
--function-name getAppList \
--zip-file fileb://snapshot/getAppListSnapshot.zip \
--profile adminuser

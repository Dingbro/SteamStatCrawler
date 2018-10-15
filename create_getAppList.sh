#!/usr/bin/env bash

rm ./snapshot/getAppListSnapshot.zip
aws lambda delete-function --function-name getAppList

cd ./env_steam/lib/python3.6/site-packages
zip -r9 ../../../../snapshot/getAppListSnapshot.zip .
cd ../../../../
zip -g ./snapshot/getAppListSnapshot.zip getAppList.py utils.py settings.yml

aws lambda create-function \
--region ap-southeast-1 \
--function-name getAppList \
--zip-file fileb://snapshot/getAppListSnapshot.zip \
--role arn:aws:iam::915999582461:role/role_lambda \
--handler getAppList.getAppList_handler \
--runtime python3.6 \
--profile adminuser \
--handler getAppList.getAppList_handler \
--runtime python3.6 \
--timeout 60 \
--memory-size 256

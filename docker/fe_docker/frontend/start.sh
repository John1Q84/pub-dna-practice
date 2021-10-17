#!/bin/sh
echo 'get temporary token for metedata'
TOKEN=`curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
echo ''

echo '>> Get Region ....'
REGION=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep region | cut -d \" -f 4`
echo $REGION && echo ''

cat configs.json.tpl | sed "s/REGION_CODE/$REGION/g" > configs.json


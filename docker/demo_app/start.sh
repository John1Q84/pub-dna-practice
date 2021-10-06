#!/bin/sh
export region=`curl 169.254.169.254/latest/meta-data/hostname | cut -f 2 -d '.'`

cat configs.json.tpl | sed -i "s/REGION_CODE/'$region'/g" > configs.json
source v_demo_app/bin/activate
pip3 install -r requirements.txt

python3 app.py

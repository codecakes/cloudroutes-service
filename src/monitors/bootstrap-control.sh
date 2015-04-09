#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"

echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Installing Cloudroutes Common Package Support"
pip install -e git+https://github.com/codecakes/cloudroutes_common_pkg.git@master#egg=cloudroutes_common_pkg
echo "-------------------------------------------------"

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/control.yml.example /config/config.yml
sed -i "s/redis_ip$/$REDIS_PORT_6379_TCP_ADDR/" /config/config.yml
sed -i "s/3679/$REDIS_PORT_6379_TCP_PORT/" /config/config.yml
sed -i "s/5879/$MONITORBROKER_PORT_5879_TCP_PORT/" /config/config.yml
sed -i "s/broker_host$/$MONITORBROKER_PORT_5879_TCP_ADDR/" /config/config.yml
sed -i "s/5878/$MONITORBROKER_PORT_5878_TCP_PORT/" /config/config.yml
sed -i "s/interval/$MONITORINTERVAL/" /config/config.yml
sed -i "s/300/$SLEEPTIMER/" /config/config.yml

echo "[BOOTSTRAP] Starting control.py for $MONITORINTERVAL"
echo "-------------------------------------------------"
python /code/control.py /config/config.yml

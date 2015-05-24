#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Installing Cloudroutes Common Package Support"
echo "-------------------------------------------------"
pip install git+https://github.com/codecakes/cloudroutes_common_pkg.git@master

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/broker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml

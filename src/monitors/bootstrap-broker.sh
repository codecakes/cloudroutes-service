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
cp /code/config/broker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml

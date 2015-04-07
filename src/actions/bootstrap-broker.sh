#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Pip Installing common helper files:"
pip install -U git+https://github.com/codecakes/cloudroutes_common_pkg.git@master
echo "-------------------------------------------------"

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/actionBroker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml

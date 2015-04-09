#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/broker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml

echo "[BOOTSTRAP] Installing Cloudroutes Common Package Support"
python /code/add2pth.py
echo "-------------------------------------------------"

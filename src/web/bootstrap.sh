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
cp /code/instance/web.cfg.example /config/web.cfg
sed -i "s/28015/$DB_PORT_28015_TCP_PORT/" /config/web.cfg
sed -i "s/localhost/$DB_PORT_28015_TCP_ADDR/" /config/web.cfg

echo "[BOOTSTRAP] Starting web.py"
echo "-------------------------------------------------"
python /code/web.py /config/web.cfg

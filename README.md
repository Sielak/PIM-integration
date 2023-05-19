# Overview
### Description
This project is used to integrate Jeeves and In River (PIM).  
It use [FastAPI](https://fastapi.tiangolo.com/).
From Jeeves DB it uses `q_hl_dp_data` to store integration logs from and to PIM.

### Process description
**Jeeves to PIM**
1. Jeeves Trigger (insert small amount of data to `q_hl_dp_data`)
2. Job `PIM2.0` have 1 steps (PIM send product) every with two actions  
2.1 Generate JSON based on data in `q_hl_dp_data` and save it in that table (Text7)  
2.2 Send HTTP request to FastAPI with this JSON from `q_hl_dp_data`  
4. Result is saved in this same row in `q_hl_dp_data` (column ResultXML and/or Message)  

**PIM to Jeeves**  
1. HTTP request is triggered (wso2 webhook)
2. FastApi fetch data from PIM and saves it in `q_hl_dp_data`
3. The appropriate procedure is run on the database side to update jeeves
4. Result of such update is logged in `q_hl_dp_data` (column EI / Message)


### Dependencies
SQL DB
```
jobs:
    PIM2.0
procedures:
    q_hl_pim2_transfer_toPIM
    q_hl_pim_GetProductFromPim
    q_hl_PIM_Picture_Synce_SDL
sql user with access to:
    q_hl_dp_writedata (procedure)
    q_hl_pim_GetProductFromPim (procedure)
```

WSO2
```
Endpoint for PIM visible from outside of HL network passing request internally:
https://esb-endpoint-703.hl-display.com/services/PIM_2_PythonAPI_PROD
```
# Structure
`main.py` --> Main file with API endpoints  
`gunicorn.py` --> File used for running FastAPI on prod using Gunicorn  
`config/` --> folder for configuration file  
`lib/` --> folder for classes used in API  
`models/` --> folder for pydantic models  

# Contributing
### Configure project
```bash
git clone git@gitlab.hl-display.com:root/pim-python.git
python -m venv venv  # put proper version of python (3.8 or higher)
source /venv/bin/activate
pip install -r requirements.txt
# Change data (if needed) in config/config.json
python main.py
```
### Debug
```python
logger.warning("Text for debug")
```
# Deployment
## Already configured machine
1. edit config file (if needed)
```bash
nano /home/ubuntu/.config/pim_integration/config_prod.json
```
2. Run Jenkins job `PIM2.0/Deploy_prod_pim2`
## New machine
1. Add new service to systemd
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
```bash
# gunicorn.service
# For running Gunicorn based application with a config file - TutLinks.com
#
# This file is referenced from official repo of TutLinks.com
# https://github.com/windson/fastapi/blob/fastapi-postgresql-caddy-ubuntu-deploy/gunicorn.service
#
[Unit]
Description=pim_integration on Gunicorn Web Server as Unit Service Systemd
After=network.target
[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/pim_integration
Environment="PATH=/home/ubuntu/virtual_environments/venv_pim/bin"
ExecStart=/home/ubuntu/virtual_environments/venv_pim/bin/gunicorn --config /opt/pim_integration/gunicorn.py main:app
[Install]
WantedBy=multi-user.target

```
```bash
sudo systemctl daemon-reload
```
2. edit config file
```bash
nano /home/ubuntu/.config/pim_integration/config_prod.json
```
3. Run Jenkins job `PIM2.0/Deploy_prod_pim2`
# Rigs monitor
## Description
Python monitor to check the status of your rigs and solves multiple problems. Currently works with Nicehash and Minerstat.
You can set the solutions that you want for a specific problem:
Example: if vram is high, restarts the mining program. If that doesn't work, the rig is restarted. If it still doesn't work an issue is opened and an email is sent to a Human.
The main idea is to avoid human intervention if possible

## Prerequisites:
Python 3.10 (I didn't test it with previous versions, but it may work)

## Instalation
1) Clone the repo
2) Move conf.json.example.nicehash or conf.json.example.minerstat to conf.json
3) Edit that file with your settings 
4) run "sudo bash ./run.sh"

Alternatively you could run "nohup sudo bash ./run.sh &" to detach the process of the terminal (Useful if you run it in a cloud server)

In the conf.json you need to complete the data of your rigs, your access keys and user, and "API pass" of Gmail. Don't share your conf.json.
More details in the documentation section

The run.sh installs the requirements, add the script folder to PYTHONPATH, run python3 Main/server.py and run python3 Main/main.py
The Main/server.py use your port 80 to expose some useful endpoints:
localhost/ = dashboard (current status of your rigs)
localhost/log = tail of the log, it updates automatically, just need to keep the windows open
localhost/full = resume of everything that happened to your rigs. (Screenshots below)
localhost/daily = daily resume
localhost/weekly = weekly resume
localhost/monthly = monthly resume
localhost/yearly = yearly resume


## Documentación

Gmail api pass= https://www.techgeekbuzz.com/blog/how-to-use-gmail-api-in-python-to-send-mail/

### Nicehash

Nicehash org_id, key and secret= https://www.nicehash.com/blog/post/nicehash-api-integration-with-google-spreadsheets-guide#api
Nicehash api docs: https://www.nicehash.com/docs/rest

### Minerstat

Minerstat API Token https://api.minerstat.com/docs-private
Minerstat Access Key: the key to access to Minerstat dashboard

Private API https://api.minerstat.com/docs-private
Public API https://api.minerstat.com/docs-public

## Screenshots
![image](https://user-images.githubusercontent.com/3521741/185759335-679d6b3e-6d18-40f1-8484-b31d28f9f3e0.png)
![image](https://user-images.githubusercontent.com/3521741/185759398-19376004-8bcb-4dbf-8316-13624abdea36.png)
![image](https://user-images.githubusercontent.com/3521741/185759411-b2cce75b-4b25-4490-b135-adeeabf16e9b.png)
![image](https://user-images.githubusercontent.com/3521741/185759418-dbec0fcd-2dc6-4200-a7ee-1554d3eba946.png)
![image](https://user-images.githubusercontent.com/3521741/185759437-dcdcd17a-fc65-40ab-814d-1c811328aa12.png)

## Contact me
if you have any doubt or comment send an email to matiasegea@gmail.com



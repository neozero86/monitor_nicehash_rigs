# Rigs monitor
## Description
Python monitor to check status of rigs. Currently working with Nicehash and Minerstat.

## Prerequisites:
Python 3.10 (I didn't test it with previous versions, but it could work)

## Instalation
1) Clone the repo
2) Move conf.json.example.nicehash or conf.json.example.minerstat to conf.json
3) Edit that file with your settings 
4) run "sudo bash ./run.sh"

Alternatively you could run "nohup sudo bash ./run.sh &" to detach the process of the terminal (Useful if you run it in some cloud server)

In the conf.json you need to complete the data of your rigs, your access keys and user and "API pass" of Gmail. Don't share your conf.json.
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

## Contact me
if you have any doubt or comment send an email to matiasegea@gmail.com



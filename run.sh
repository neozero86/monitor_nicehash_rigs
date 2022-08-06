PWD=`pwd`
if [[ ${PYTHONPATH} != *"${PWD}"* ]];then
	export PYTHONPATH="${PYTHONPATH}:${PWD}"
fi
python3 Main/main.py

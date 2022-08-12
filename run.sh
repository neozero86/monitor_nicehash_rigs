python3 -m pip install -r requirements.txt

function cleanup {
  echo "killing report process id: "$report_pid
  kill -9 $report_pid
}

trap cleanup EXIT

PWD=`pwd`
if [[ ${PYTHONPATH} != *"${PWD}"* ]];then
	export PYTHONPATH="${PYTHONPATH}:${PWD}"
fi
nohup python3 Main/server.py &
export report_pid=$(echo $!)
python3 Main/main.py 

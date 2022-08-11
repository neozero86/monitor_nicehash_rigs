python3 -m pip install -r requirements.txt

function cleanup {
  echo "killing report process id: "$report_pid
  kill -9 $report_pid
  echo "killing log process id: "$log_pid
  kill -9 $log_pid
}

trap cleanup EXIT

PWD=`pwd`
if [[ ${PYTHONPATH} != *"${PWD}"* ]];then
	export PYTHONPATH="${PYTHONPATH}:${PWD}"
fi
nohup python3 Main/report/show_report.py &
export report_pid=$(echo $!)
nohup frontail logs/out.log --ui-highlight &
export log_pid=$(echo $!)
python3 Main/main.py 

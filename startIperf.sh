echo $1
iperf3 -c "$1" -t "$2" -u -b "$3"
# tmux new-session -d -s iperf 'python iperf.py $1'
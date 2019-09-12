echo $1
iperf3 -c "$1" -t 10
# tmux new-session -d -s iperf 'python iperf.py $1'
#/bin/bash
#-------------------------------
#	Author: LSK
#	Filename: control.sh
#	Datetime: 2018-7-6
#   Description: control wechat
#-------------------------------
workPath=$(cd $(dirname $0 )/; pwd)
bin=$workPath/wechat-socket.py
pidFile=$workPath/logs/wechat.pid
logFile=$workPath/logs/wechat.log
function check_pid() {
    if [ -f $pidFile ];then
        pid=`cat $pidFile`
        if [ -n $pid ];then
            running=`ps -p $pid | grep -v "PID TTY" | wc -l`
            return $running
        fi
    fi
    return 0
}
function start() {
    check_pid
    running=$?
    if [ $running -gt 0 ];then
        echo -n "The Wechat Interface is running already,pid="
        cat $pidFile
        return 1
    fi
    nohup /usr/bin/python $bin >> $logFile 2>&1 &
    echo $! > $pidFile
    echo "The Wechat Interface start to run,pid=$!"
}
function stop(){
    check_pid
    running=$?
    if [ $running -gt 0 ];then
        kill $pid
        echo "The Wechat Interface stoped..."
    else
        echo "The Wechat Interface not running"
    fi
}
function restart() {
    stop
    sleep 1
    start
}
function status(){
    check_pid
    running=$?
    if [ $running -gt 0 ];then
        echo -n "The Wechat Interface is running.PID="
        cat $pidFile
    else
        echo "The Wechat Interface is stopped"
    fi
}
function help(){
    echo "$0 start|stop|restart|status"
}
function pid() {
    cat $pidFile
}
if [ "$1" == "" ];then
    help
elif [ "$1" == "stop" ];then
    stop
elif [ $1 == "start" ];then
    start
elif [ $1 == "restart" ];then
    restart
elif [ $1 == "status" ];then
    status
elif [ $1 == "pid" ];then
    pid
else
    help
fi

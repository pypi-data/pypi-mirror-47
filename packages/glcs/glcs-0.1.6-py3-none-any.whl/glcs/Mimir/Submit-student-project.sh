#!/bin/bash
username=""
pass=""
email=""
directory=""
pid=""
dir=0
while getopts "u:p:e:d:i:" opt;
do
  case $opt in
    u )
    username="$OPTARG"
    echo "$username"
    ;;
    p )
    pass="$OPTARG"
    echo "$pass"
    ;;
    e )
    email="$OPTARG"
    echo "$email"
    ;;
    d )
    dir=1
    directory="$OPTARG"
    echo "$directory"
    ;;
    i )
    pid="$OPTARG"
    echo "$pid"
    ;;
  esac
done
if [ $dir -eq 0 ];
then
  directory="temp"
  echo "$directory"
fi
mimir login -e "$username" -p "$pass"
mimir project submit --path $directory --project-id $pid --on-behalf-of "$email"
mimir logout
rm -rf $directory

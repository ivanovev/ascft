#!/bin/bash

if [ $# == 0 ]; then
    echo "wrong # of args"
    exit 1
fi

path=`pwd`
name=`basename $path`
tgz_file="/tmp/${name}.tgz"
smb="/mnt/smb4"

tgz()
{
    tar --exclude-vcs --exclude=*.swp -cvzf $tgz_file ascft.py ascft.bat freeze.bat
}

try2copy()
{
    n=`mount | grep $smb | wc -l`
    btgz=`basename $tgz_file`
    if (($n == 1)); then
        cp $tgz_file $smb/start/$btgz
    fi
}

case $1 in
'tgz')  tgz
        try2copy
        ;;
*)      echo 'invalid option'
        ;;
esac


#!/bin/bash
echo Checking packages

python3 -m pip install -r requirements.txt

echo Running ToundBotV2

if [ "$OSTYPE" == "msys" ]
then
	echo python
	python3 ToundBotV2.py > logfile.txt 2>&1
	
elif [ "$OSTYPE" == "linux" ]
then
	echo python3
	python3 ToundBotV2.py > logfile.txt 2>&1
fi

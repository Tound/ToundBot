#!/bin/bash
echo Checking packages

python -m pip install -r requirements.txt

echo Running ToundBotV2

if [ "$OSTYPE" == "msys" ]
then
	echo python
	python ToundBotV2.py > logfile.txt 2>&1
	
elif [ "$OSTYPE" == "linux" ]
then
	echo python3
	python3 ToundBotV2.py > logfile.txt 2>&1
fi

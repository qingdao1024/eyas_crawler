#!/bin/sh
while [ ! -f /vagrant_data/break.flag ]; do
	  python test14.py >> log.log
done

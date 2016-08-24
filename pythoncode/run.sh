#!/bin/sh
while [ ! -f /vagrant_data/break.flag ]; do
	  python clawer-v-1-1-1.py >> log.log
done

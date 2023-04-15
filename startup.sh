#!/usr/bin/env bash
sudo /usr/sbin/crond -s
/opt/app-root/app/case_poller.py &
sleep 10
/opt/app-root/app/exporter.py

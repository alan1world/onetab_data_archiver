#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

# IS_RUNNING = True

def mariadb_is_running():
    
    status_mariadb = subprocess.run(['systemctl', 'status', 'mysqld'], stdout=subprocess.PIPE, encoding="utf-8")
    if "Active: active" in status_mariadb.stdout:
        return "Mariadb is running"
    else:
        return "Mariadb is not running"
        
def mariadb_start():
    
    service_mariadb = subprocess.run(['systemctl', 'start', 'mysqld'], stdout=subprocess.PIPE, encoding="utf-8")
    if service_mariadb.returncode == 0:
        print("Mariadb successfully started")
    else:
        print("Failed to start Mariadb")

def mariadb_stop():
    
    service_mariadb = subprocess.run(['systemctl', 'stop', 'mysqld'], stdout=subprocess.PIPE, encoding="utf-8")
    if service_mariadb.returncode == 0:
        print("Mariadb successfully stopped")
    else:
        print("Failed to stop Mariadb")

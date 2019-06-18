#! /usr/bin/env python
# -*- coding: utf-8 -*-

import mariadbcontrol, mysql.connector as mariadb, keyring, getpass
from collections import namedtuple

def run_mariadb():
    
    if "Mariadb is not running" in mariadbcontrol.mariadb_is_running():
        mariadbcontrol.mariadb_start()
        print("Mariadb has been started")
        return "stop"
    else:
        print("Mariadb was already running")
        return "leave"

        
def mariadb_connect(db='links', usr='alan', psswd='', dbase='link_store'):
    
    mariadb_connection = mariadb.connect(user=usr, password=psswd, database=dbase)
    cursor = mariadb_connection.cursor()
    stmt = "CREATE TABLE IF NOT EXISTS"
    stmt += db
    stmt += " (link_id bigint NOT NULL AUTO_INCREMENT, "
    stmt += "raw_link TEXT, "
    stmt += "title TEXT, "
    stmt += "link TEXT, "
    stmt += "source TEXT, "
    stmt += "importdate TEXT, "
    stmt += "CONSTRAINT link_id_pk PRIMARY KEY (link_id)"
    stmt += ") ENGINE = 'Aria' TRANSACTIONAL = 1;"
    cursor.execute(stmt)
    mariadb_connection.commit()
    cursor.close()
    mariadb_connection.close()

def mariadb_insert(lite_cur, db='links', usr='alan', psswd='', dbase='link_store', compatibility_order = False):
    
    mariadb_connection = mariadb.connect(user=usr, password=psswd, database=dbase)
    cursor = mariadb_connection.cursor()
    stmt = "INSERT INTO "
    stmt += db
    if compatibility_order == True:
        stmt += " (raw_link, title, link, source, importdate) VALUES (%s, %s, %s, %s, %s)"
    else:
        stmt += " (raw_link, source, importdate, title, link) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(stmt, lite_cur)
    mariadb_connection.commit()
    cursor.close()
    mariadb_connection.close()

def mariadb_limiter(lite_cur, db='links', usr='alan', psswd='', dbase='link_store'):
    
    x = 0
    y = 0
    while y <= len(mds):
        y += 12000
        if y > len(mds):
            y = len(mds)
            mariadb_insert(mds[x:], db, usr, psswd, dbase)
            break
        else:
            mariadb_insert(mds[x:y], db, usr, psswd, dbase)
            x = y

def key_implement(dbase = 'link_store', usr = 'alan'):
    
    if keyring.get_password(dbase, usr) == None:
        usr_pass = getpass.getpass(prompt="Mysql password:")
        keyring.set_password(dbase, usr, usr_pass)
        print("Password set")
        return usr_pass
    else:
        print("Password found")
        return keyring.get_password(dbase, usr)
    
if __name__ == "__main__":
    
    usr = 'alan'
    dbase = 'link_store'
    db='links'
    psswd = key_implement(dbase = dbase, usr = usr)
    
    Linker = namedtuple('Linker', ['raw_link', 'browser', 'date', 'title', 'link'])
    link_collection = []
    link_collection.append(Linker('[test](test)','chrome','2018-04-02','test','test'))
    link_collection.append(Linker('[test](test)','firefox','2018-04-02','test','test'))
    
    mariadb_state = run_mariadb()
    mariadb_insert(lite_cur=link_collection, db=db, usr=usr, psswd=psswd, dbase=dbase)
    
    
    if mariadb_state == "stop":
        mariadbcontrol.mariadb_stop()

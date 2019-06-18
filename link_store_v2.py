#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, sys, configparser, os, tarfile, tempfile, shutil
# removed: argparse, dataset, re, datetime, mistune
# packages:
import backup_csv, backup_html, backup_hugo, backup_xml, create_namedtuple, backup_db, backup_mariadb, mariadbcontrol
# Mistune is the markdown converter
# Dataset for lazy database creation
from PyQt5.QtWidgets import (QDialog, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QPlainTextEdit, QLineEdit, QLabel)
    
class GatherText(QDialog):
        
    def __init__(self):
        super().__init__()
        # self.output = {'Content':'', 'Browser':'', 'Modifier':'', 'Date':''}
        self.initUI()
    
    def initUI(self):
        
        chromeButton = QPushButton("Chrome")
        firefoxButton = QPushButton("Firefox")
        keepButton = QPushButton("Keep")
        self.plainTextEdit = QPlainTextEdit()
        self.lineEdit = QLineEdit()
        lineLabel = QLabel("Modifier")
        self.lineEdit2 = QLineEdit()
        lineLabel2 = QLabel("Date")
        
        # Create the space for the browser buttons
        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(chromeButton)
        hbox.addWidget(firefoxButton)
        hbox.addWidget(keepButton)
        
        # Create the space for the modifier text and date change
        hbox2 = QHBoxLayout()
        hbox2.addWidget(lineLabel)
        hbox2.addWidget(self.lineEdit)
        hbox2.addWidget(lineLabel2)
        hbox2.addWidget(self.lineEdit2)
        
        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.plainTextEdit)
        
        self.setLayout(vbox)
        chromeButton.clicked.connect(self.setOutputChrome)
        firefoxButton.clicked.connect(self.setOutputFirefox)
        keepButton.clicked.connect(self.setOutputKeep)
        self.lineEdit2.setText(time.strftime("%Y-%m-%d"))
        
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Link Store')
        self.show()

    def setOutputChrome(self):
        self.setOutput(self.plainTextEdit.toPlainText(), 'chrome', self.lineEdit.text(), self.lineEdit2.text())

    def setOutputFirefox(self):
        self.setOutput(self.plainTextEdit.toPlainText(), 'firefox', self.lineEdit.text(), self.lineEdit2.text())

    def setOutputKeep(self):
        fix_this_text = self.plainTextEdit.toPlainText()
        fixed_test = fix_this_text.replace("\n\nhttp", "|http").replace("\n\n","\n")
        self.setOutput(fixed_test, 'keep', self.lineEdit.text(), self.lineEdit2.text())

    def build_markdown(self, contents, location, strBrowser, strDate, strModifier):
        
        file_name = location + strBrowser + '-' +  strDate + strModifier + '.md'
        backup_hugo.create_namedtuple(contents, browser=strBrowser, hdate=strDate, location = file_name, modifier = strModifier)
        
    def build_html(self, contents, location, strBrowser, strDate, strModifier):
        
        file_name = location + strBrowser + '-' +  strDate + strModifier + '.html'
        backup_html.create_html(contents, browser=strBrowser, hdate=strDate, location = file_name, modifier = strModifier)
        
    def build_xml(self, contents, location, strBrowser, strDate, strModifier):
        
        file_name = location + strBrowser + '-' +  strDate + strModifier + '.xml'
        backup_xml.create_xml(contents, output_name=file_name)
        
    def build_csv(self, contents, location, strBrowser, strDate, strModifier):
        
        file_name = location + strBrowser + '-' +  strDate + strModifier + '.csv'
        backup_csv.create_csv(contents, output_name=file_name)
        
    def build_db(self, contents, location, strBrowser, strDate, strModifier):
        
        file_name = location + strDate + '.db'
        backup_db.create_db(content=contents, source=strBrowser, output_name=file_name)
    
    def build_mariadb(self, contents, usr, dbase, db):
        
        mariadb_state = backup_mariadb.run_mariadb()
        psswd = backup_mariadb.key_implement(dbase = dbase, usr = usr)
        backup_mariadb.mariadb_insert(lite_cur=contents, db=db, usr=usr, psswd=psswd, dbase=dbase)
        if mariadb_state == "stop":
            mariadbcontrol.mariadb_stop()
        
    def setOutput(self, strContent, strBrowser, strModifier, strDate):
       
        contents = create_namedtuple.create_namedtuple(strContent.split('\n'),strDate,mybrowser=strBrowser)
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        #config.read('debug.ini')
        
        config_zip = config.getboolean("Outputs", "zip")
        
        if config.getboolean("Outputs", "zip"):
            with tempfile.TemporaryDirectory() as tmpdirname: 
                self.build_markdown(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                self.build_html(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                self.build_xml(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                self.build_csv(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                
                try:
                    with tarfile.open(name=config.get("Locations", "db") +  strDate + strModifier + '.tar.gz',mode='r') as gtar:
                        gtar.extractall(path=tmpdirname + '/')
                except IOError:
                    pass
                self.build_db(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                with tarfile.open(name=config.get("Locations", "db") +  strDate + strModifier + '.tar.gz',mode='w:gz') as gtar:
                    for x in os.listdir(tmpdirname):
                        gtar.add(tmpdirname + '/' + x, x)
        
        if config.getboolean("Outputs", "markdown"):
            self.build_markdown(contents, config.get("Locations", "hugo"), strBrowser, strDate, strModifier)
        
        if config.getboolean("Outputs", "html"):
            self.build_html(contents, config.get("Locations", "html"), strBrowser, strDate, strModifier)
            
        if config.getboolean("Outputs", "xml"):
            self.build_xml(contents, config.get("Locations", "db"), strBrowser, strDate, strModifier)
            
        if config.getboolean("Outputs", "csv"):
            self.build_csv(contents, config.get("Locations", "db"), strBrowser, strDate, strModifier)
        
        if config.getboolean("Outputs", "sqlite"):
            with tempfile.TemporaryDirectory() as tmpdirname:
            # self.build_db(contents, config.get("Locations", "db"), strBrowser, strDate, strModifier)
                self.build_db(contents, tmpdirname+'/', strBrowser, strDate, strModifier)
                for x in os.listdir(tmpdirname):
                    print(x)
                    shutil.copy(tmpdirname + '/' + x, os.getcwd())
        
        if config.getboolean("Outputs", "mariadb"):
            db_config = config['Database']
            self.build_mariadb(contents, db_config['user'], db_config['schema'], db_config['table'])
        
        self.accept()
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = GatherText()
    # ex.exec_()
    # print('Content: \t' + ex.output['Content'] +
    #       '\nBrowser: \t' + ex.output['Browser'] +
    #       '\nDate: \t\t' + ex.output['Date'])
    # exit()
    sys.exit(app.exec_())

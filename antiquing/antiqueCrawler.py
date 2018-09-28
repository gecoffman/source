#!/usr/bin/python

import sys
sys.path.insert(0, '/home/ekarg/src/')

import datetime 
from dateutil import parser

import requests

import pandas
from database import getSession
from antiqueTable import antiqueTableManager
from lib.emailHelper import sendMail 
import time
from passwords.antiqueWebsite import password, emails

def main():
	cred = { 'StoreID' : password['store'], 'DealerNo' : password['username'], 'Password' : password['password'] } 	
	page  = requests.post( 'https://www.mall-info.com/default.asp', data=cred  ) 
	
	tableManager = antiqueTableManager( cred )
	
	hasUpdated = False
	while( not hasUpdated  ):
		updatedDate = tableManager.getLastDateUpdate()

	
		if updatedDate == datetime.date.today():
		
			subject = 'Sales updated for %s' % str( updatedDate )
			currentTotal = tableManager.getCurrentTotal()
        		msg = 'Go check! The current total is %s' % currentTotal
			
			#sendMail( emails[0], subject, msg )	
			#sendMail( emails[1], subject, msg )
			sess = getSession()
			df = tableManager.getSalesHistoryTable()
			print df.head()
			sess.write_frame( 'GC32','History_'+ str( updatedDate ),  df )
			hasUpdated = True
		else:
			time.sleep( 5 * 60 ) 		


if __name__ == '__main__':
	main()

import sys

sys.path.insert( 0, 'home/ekarg' )
import requests
import pandas
from bs4 import BeautifulSoup
from dateutil import parser



class antiqueTableManager( object ):


	def __init__( self, cred ):
		self.cred = cred 


	def getCurrentTotalTable( self ):
		''' Get the initial table when you log in that contains the last date/time updated'''
		page  = requests.post( 'https://www.mall-info.com/default.asp', data=self.cred  )
	        		
        	df = pandas.read_html( page.content )[1]

        	df.index = df[0]
        	df = df.T
        	df.columns = [ 'StoreNo', 'MallName', 'Updated', 'DealerNo', 'DealerName', 'CurrentCheck', 'Company', 'Email' ]
        	df = df.drop(0)
 
        	
		return df 

	def getLastDateUpdate( self ):
		''' Determine that last date updated ''' 
		df = self.getCurrentTotalTable()
		updated = df[ 'Updated' ].iloc[0]
                updatedDate = parser.parse( updated ).date()
		return updatedDate

	def getCurrentTotal( self ):
		''' Determine current total ''' 
		df = self.getCurrentTotalTable()
                currentTotal = df[ 'CurrentCheck' ].iloc[0]
		return currentTotal

		
	def getSalesHistoryTable( self ):
	       ''' Return data frame of the sales history '''
               page  = requests.post( 'https://www.mall-info.com/default.asp', data=self.cred  )	
	       soup = BeautifulSoup( page.content, 'html.parser' )
	       href = soup.select_one("a[href*=History]" )['href']
	       page  = requests.post( 'https://www.mall-info.com/' + href, data=self.cred  )      
	       df = pandas.read_html( page.content )[1]
	       return df

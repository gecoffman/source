import os.path
import pickle

_FILES_HOME = os.path.expanduser( '~/mall_data/' )

''' use this module by doing

from database import getSession

sess = getSession()

all_data = ses.read_all()

'''

class SessionBase( object ):

    def __init__( self, handle = None ):
        self.handle = handle

    def list_dealers( self ):
        ''' list all the dealers in the db '''
        raise NotImplementedError( 'list dealers not implemented in base class' )

    def list_frames( self, dealer ):
	''' list all the frame in the db for the passed dealer '''
        raise NotImplementedError( 'list frames not implemented in base class' )

    def read_frame( self, dealer, frame_name ):
        ''' read the given frame name for the given dealer from the db '''
        raise NotImplementedError( 'read frame not implemented in base class' )

    def read_all( self ):
        ''' read all the data, return as a dict keyed by dealer, of dicts keyed by
        frame name, values are dataframes '''

        all_data = { }
        all_dealers = self.list_dealers()
        for dealer in all_dealers:
            all_data[ dealer ] = { }
            frames_for_dealer = self.list_frames( dealer )
            for frame in frames_for_dealer:
                all_data[ dealer ][ frame ] = self.read_frame( dealer, frame )

        return all_data

    def write_frame( self, dealer, frame_name, frame_data ):
        ''' write the given frame data to the given frame name for the given dealer to the db '''
        raise NotImplementedError( 'write frame not implemented in base class' )
        
    def write_all( self, all_data ):
        ''' traverse the passed dict of dicts and write each frame to the db '''

        for dealer in all_data:
            for frame_name, frame_data in all_data[ dealer ].items():
                self.write_frame( dealer, frame_name, frame_data )

class PickleDB( SessionBase ):

    ''' simple pickle implementation which works by pickling the dataframes into files
    laid out as:

    mall_data/
       |------GC32/
       |        |----current_sales.obj
       |        |----settlements.objdf = pandas.read_html( page.content )[1
       |        |----etc etc
       |------SC32/
                |----current_sales.obj

    '''

    def __init__( self, root = _FILES_HOME ):
        super( PickleDB, self ).__init__()
        self.root = root

    def list_dealers( self ):
        ''' list dealers in db '''
        return [ x for x in os.listdir( self.root ) if os.path.isdir( self.root + x ) ]

    def list_frames( self, dealer ):
        ''' list frames for dealer '''
        return [ x.replace( '.obj', '' ) for x in os.listdir( self.root + dealer ) if x.endswith( '.obj' ) ]

    def read_frame( self, dealer, frame_name ):
        ''' read one frame for the dealer by name '''

        return pickle.load( open( self.root + dealer + '/' + frame_name + '.obj', 'rb' ) )

    def write_frame( self, dealer, frame_name, frame_data ):
        ''' write the given frame data to the given frame name for the given dealer to the db '''

        if not os.path.exists( self.root + dealer ):
            os.mkdir( self.root + dealer )
        pickle.dump( frame_data, open( self.root + dealer + '/' + frame_name + '.obj', 'wb' ) )

def getSession( clazz = PickleDB ):
    ''' return a session, using clazz to construct '''

    return clazz()

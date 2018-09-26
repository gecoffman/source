#!/usr/bin/python

''' Back up Grace's stuff '''

import os
import re
from   subprocess import Popen, PIPE
from   datetime   import date, datetime

_EXTENSIONS = [
    'odt', # Open Office Document
    'msk', # Manuscript Document
    'txt', # Gwace's vi files
]

_HOME  = '/home/ekarg'
_TODAY = date.today().strftime( '%Y%m%d' )
_FIND  = '/usr/bin/find'
_TAR   = '/bin/tar'
_LINE  = '-' * 80
_DEST  = _HOME + '/backups/backup%s.tgz' % _TODAY

def log( message ):
    ''' poor man's logger :) '''

    print _LINE
    print datetime.now().strftime( '%Y-%m-%d %H:%M:%S : ' ) + message
    print _LINE

def runCommand( command ):
    ''' run a system command and return the return code, stdout and stderr buffers '''

    log( 'running command %s' % command )
    p = Popen( command, shell = True, stdout = PIPE, stderr = PIPE )
    out, err = p.communicate()

    rc = p.returncode

    log( 'result\n  RC : %d\n  OUT: %s\n  ERR: %s' % ( rc, out, err ) )
    return rc, out, err

def findFiles( path = _HOME + '/*', extensions = _EXTENSIONS ):
    ''' find files anywhere under the path specified that match the extensions '''

    findCommand = _FIND + ' %s -type f' % path
    numExts = len( extensions )
    for extension in extensions:
        numExts -= 1
        findCommand += ' -name \'*.%s\'' % extension
        if numExts:
            findCommand += ' -o'
    
    rc, out ,err = runCommand( findCommand )
    return out.split('\n')

def main():
    ''' do things '''

    log( 'starting' )
    fileList = findFiles()
    fileList.pop() # for some reason always has one blank line

    runCommand( _TAR + ' cvzf %s %s' % ( _DEST, ' '.join( [ '\'%s\'' % x for x in fileList ] ) ) )

if __name__ == '__main__':
    main()

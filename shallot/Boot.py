
from cymbeline.Auth import *


from cymbeline.Objects import Object,Provider,LocalGC
from cymbeline.BaseProviders import Pool
from cymbeline.DB import HierDB,MemoryDB
from cymbeline.HTTPServer import HTTP
from cymbeline.Remote import *


from cymbeline.IC import CymbelineIC

import sys
import time

import sqlite
import MySQLdb

from shallot.Player import Player
from shallot.Libscanner import Libscanner
from shallot.Library import Library

__version_int__ = 2

def connect_db(gc):

    
#    pool = Pool(gc, 'db', factory = MySQLdb.connect, factory_param_map = {'user':'root','db':'shallot'})
    pool = Pool(gc, 'db', factory = sqlite.connect, factory_param_map = {'database':'shallot.db','encoding':'utf-8'})    
    gc.registerProvider(pool)



def setup(gc):
    settings = HierDB(gc, "settings")
    
    settings.mktree(['global'])
    

def boot(gc, localname='/shallot/'):
    print
    print "Welcome to Shallot"
    print "------------------"
    print "The music thingy"
    print "Amoeba Release"
    print "(c) 2004 Yann Ramin"
    print
    print "Creating new local global context on " + localname + "..."
    gc = LocalGC(gc, localname)
    print "Loading up my configuration..."

    


    gc.registerProvider(HierDB(gc, '/system/httpsession', autoload = 0))


    http = HTTP(gc, 'http_'+localname[1:-1])
    gc.registerProvider(http)
    http.start()
    
    try:
        version = settings.read_t(('global', 'version'))
        if (version < __version_int__):
            setup(gc)
            
    except:
        setup(gc)


    print
    print
    sys.stdout.write("Creating database pool...")
    
    connect_db(gc)
    print "OK"

    print "Creating Library...",
    lib = Library(gc, 'library')
    gc.registerProvider(lib)
    print "OK"

    print "Creating library scanner...",
    libscan = Libscanner(gc, 'libscanner')
    gc.registerProvider(libscan)
    print "OK"
    print
    print

    print "Scanning library..."
    time.sleep(.1)
    libscan.scan()


    print "Creating player..."
    player = Player(gc, 'player')
    gc.registerProvider(player)
    

    print "Creating remote..."
    remote = Remote(gc, 'remote', 'shallot')
    gc.registerProvider(remote)
    remote.publish('player', 'player')

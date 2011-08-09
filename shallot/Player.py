from shallot.Object import Object
from shallot.Playlist import Playlist
from shallot.Library import MusicFilePrimitive
from cymbeline.Objects import Provider,Thread
import audioplay.player

import threading

class PlaylistPlayer(Thread):
    def __init__(self, gc, name, playlist):
        Thread.__init__(self, gc, name)
        self.db = gc['db']
        self.cont = threading.Event()
        self.cont.set()
        self.playlist = playlist


    def run(self):
        while self.cont.isSet() and self.playlist:
            player = self.GC['player']
            self.playlist.update()
            song = self.playlist.next()

            root = self.GC['/system/settings'].read('shallot-music')

            print song.filename
            player._playfile(root + song.filename)
            
        

class Player(Provider):
    def __init__(self, gc, name):
        Provider.__init__(self, gc, name)
        self.db = gc['db']
        self.player = audioplay.player.Player()


        
        self.player_manager = PlaylistPlayer(gc,
                                             name + '_playlistplayer_thread',
                                             Playlist(gc, '_library'))


        
        self.player_manager.start()
        self.status = 'Playing'

    def repeat(self):
        p = self.active_playlist()
        if p.playmode == 'repeat':
            p.playmode = 'random'
        else:
            p.playmode = 'repeat'
        
    def random(self):
        pass

    def active_playlist(self):
        return self.player_manager.playlist

    def pretty_pos(self):
        return self.player.pretty_pos()

    def current_song(self):
        song = self.active_playlist().current()
        return song.mdata

    def stop(self):
        self.player_manager.cont.clear()
        self.player.stop()
        self.status = 'Stopped'

    def next(self):
        self.player.stop()
             
        
    def start(self):
        self.player_manager.start()
        self.status = 'Playing'

    def request(self, id, goto):

        self.active_playlist().request(id)
        if goto:
            self.next() # check if skip to next enabled

    def pause(self):
        if self.status == 'Playing':
            self.player.pause()
            self.status = 'Paused'
        else:
            self.player.unpause()
            self.status = 'Playing'
        
    def _playfile(self, file):
        if self.player.status['playing'].isSet():
            self.player.stop()
            self.player.status['finished'].wait()

        try:
            self.player.load_file(file)
            self.player.play(wait_finish = True)
        except:
            pass
        
        
        
        
    

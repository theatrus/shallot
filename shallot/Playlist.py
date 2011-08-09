from shallot.Object import Object
import random


class Playlist(Object):
    def __init__(self, gc, id):
        Object.__init__(self, gc)
        self.songs = []
        self.index = 0
        self.playmode = 'random'
        self.id = id

        self._request = []

        if id is '_library':
            self.songs = gc['library'].get_files()
            

    def update(self):
        if id is '_library':
           self.songs = self.GC['library'].get_files()
           return
       
    def current(self):
        return self.songs[self.index]


    def request(self, id):
        l = len(self.songs)

        self._request.append(id)


    def next(self):
        if len(self._request) is not 0:
            self.index = self._request[0]
            del self._request[0]

        elif self.playmode is 'random':
            self.index = random.randint(0,len(self.songs))
        elif self.playmode is 'linear':
            if self.index + 1 >= len(self.songs):
                self.index = -1
                self.index = self.index + 1
        elif self.playmode is 'repeat':
            pass
                
        return self.songs[self.index]
    

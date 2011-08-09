from time import time
from cymbeline.Objects import Provider
from shallot.Object import Object
import psyco

class MusicFileB(Object):
    def __init__(self, gc, file):
        self.file = file
    def __getitem__(self, name):
        return self.file

class MusicFile(Object):

    def _create_update(self, file, cargs, update = False, create = False):
        db = self.get_db()
        self.mdata = {}

        if create or update is True:
            data = {
                'file':file,
                'title': cargs['title'],
                'artist': cargs['artist'],
                'genre': cargs['genre'],
                'album': cargs['album'],
                'track': cargs['track'],
                'comment': cargs['comment'],
                'bitrate': int(cargs['bitrate']),
                'length': int(cargs['length']),
                'metadate': int(time())
                }

        if create is True:
            data['metadate'] = int(time())
            
            cur = db.cursor()
            d =         {'file': file,
                         'format': cargs['format'],
                         'size' : int(cargs['size']),
                         'mtime' : int(cargs['mtime'])
                         }

            print d
            cur.execute("INSERT INTO music (file, format, size, mtime) VALUES (%(file)s, %(format)s, %(size)s, %(mtime)s)", d)

            
#create table music_info (file text, title text, artist text, genre text, album text, track text, comment text, bitrate int, length int, metadate timestamp);


            cur.execute("INSERT INTO music_info (file,title,artist,genre,album,track,comment,bitrate,length,metadate) VALUES (%(file)s, %(title)s, %(artist)s, %(genre)s, %(album)s, %(track)s, %(comment)s, %(bitrate)s, %(length)s, %(metadate)s)",
                        data
                        )

            
            
            db.commit()
            
        if update is True:
            print "Update "+file
            cur = db.cursor()

            print "Update",file
            
            cur.execute('UPDATE music SET format = %(format)s, size = %(size)s, mtime = %(mtime)s WHERE file = %(file)s',
                        {'file': file,
                         'format': cargs['format'],
                         'size' : int(cargs['size']),
                         'mtime' : int(cargs['mtime']),
                         }
                        )
            data['mtime'] = cargs['mtime']

            cur.execute("UPDATE music_info SET title = %(title)s, artist = %(artist)s, genre = %(genre)s, album = %(album)s, track = %(track)s, comment = %(comment)s, bitrate = %(bitrate)s, length = %(length)s, metadate = %(metadate)s WHERE metadate < %(mtime)s AND file = %(file)s",
                        data
                        )
            db.commit()

            # / Update
                        



    def _get_data(self, gc, cargs, file, query_data):
        db = self.get_db()
        self.mdata = {}
        # Just Get Info
        cur = db.cursor()


        # Shortcut for queries already done for us :)
        if query_data is None:
            cur.execute("SELECT format,size,mtime,title,artist,genre,album,track,comment,bitrate,length,metadate FROM music,music_info WHERE music.file = %(file)s AND music.file = music_info.file", {'file': file})
            data = cur.fetchone()
        else:
            data = query_data
            
        
        if data is None:
            self.release_db()
            raise
        
        self.mdata['file'] = file
        self.mdata['format'] = data[0]
        self.mdata['size'] = data[1]
        self.mdata['mtime'] = data[2]
        

        self.mdata['title'] = data[3]
        self.mdata['artist'] = data[4]
        self.mdata['genre'] = data[5]
        self.mdata['album'] = data[6]
        self.mdata['track'] = data[7]
        self.mdata['comment'] = data[8]
        self.mdata['bitrate'] = data[9]
        self.mdata['length'] = data[10]
        self.mdata['metadate'] = data[11]
            
        self.release_db()


    def __init__(self, gc, file, update = False, cargs = False, create = False, query_data = None):
        Object.__init__(self, gc)

        self.mdata = {}

        if file is None:
            raise

        if create or update is True:
            self._create_update(file, cargs, update, create)

        self._get_data(gc, cargs, file, query_data)


        self.filename = file
        
        
    def __getitem__(self,name):
        return self.mdata[name]
        
            
class MusicFilePrimitive:
    def __getitem__(self,name):
        return self.mdata[name]
        


class Library(Provider):
    def __init__(self, gc, name):
        Provider.__init__(self, gc, name)
        self.db = gc['db']
        
    
    def get_file(self, file):
        return MusicFile(self.GC, file)

    def add_file(self, file, fileinfo):

        a = MusicFile(self.GC, file, create = True, cargs = fileinfo,  update = False)
        return a

    def update_file(self, file, finfo):
        a = MusicFile(self.GC, file, update = True, cargs = finfo)
        return a

    def get_files(self):
        db = self.db.get()
        cur = db.cursor()
        
        cur.execute("SELECT music.file,format,size,mtime,title,artist,genre,album,track,comment,bitrate,length,metadate FROM music,music_info WHERE music.file = music_info.file AND format != 'unknown' ORDER BY artist,title")
        
        
        
        music = []
        data = cur.fetchone()
        while data:

            data = list(data)
            
            
            file = data[0]
            del data[0]
            a = MusicFile(self.GC, file, query_data = data)
        

            music.append(a)
            data = cur.fetchone()


        self.db.finish(db)
        return music

#!/usr/bin/env python


from ID3 import *
import eyeD3
import os
import re
from os.path import join,getsize
import string
from cymbeline.Objects import Provider

class Libscanner(Provider):
    def __init__(self, gc, name):
        Provider.__init__(self, gc, name)

    def interp_name(self, file):
        """ Returns a tuple of Artist - Title generated from the file name """
        file = re.sub('.*/','',file)

        filem = re.search('(.*) - (.*)\.(.*)', file)
        if filem is not None:
            return [filem.group(1), filem.group(2)]

        filem = re.search('(.*)\.(.*)', file)
        return ['', filem.group(1)]
        

    def id3_transform(self, finfo, id3info, item, item2):
        try:
            finfo[item2] = id3info[item]
        except:
            finfo[item2] = ''

    def scan(self):
        
        scan_file = 0
        files = []
        sroot = '/media/mp3/Organized MP3s'
        walk =  os.walk(sroot)
#        walk =  os.walk('.')

        for root,dirs,dfiles in walk:
            if len(dfiles) is not 0:
                root = re.sub(sroot + '/', '', root)
                files = files + [join(root,name) for name in dfiles]
                #files = files + dfiles
            
        print len(files), "files scanned, "

        for file in files:
            file = re.sub(sroot + '/', '', file)
            fullfile = sroot + '/' + file
            #fullfile = file
            fstat = os.stat(fullfile) # Stat the file so we can determine changes
        
            ext = file.split('.')[-1]

            finfo = {'format' : '',
                     'size' : '',
                     'mtime' : '',
                     'title' : '',
                     'artist' : '',
                     'genre' : '',
                     'album' : '',
                     'track' : 0,
                     'comment': '',
                     'bitrate': 0,
                     'vbr': 0,
                     'comment': '',
                     'length': 0,
                     'metadate': 0
                     }

            finfo['size'] = fstat.st_size
            finfo['mtime'] = fstat.st_mtime
            

            try:
                f = self.GC['library'].get_file(file)
            except:
                f = {}

            try:
                mtime = f['mtime']
                if mtime < finfo['mtime']:
                    scan_file = 1

            except KeyError:
                scan_file = 1

            


            if scan_file is 1:
                print "Scanning ",file
                if file.rfind('.mp3') is not -1:
                    finfo['format'] = 'mp3'
                    
                    
                    try:
                        
                        audioFile = eyeD3.Mp3AudioFile(fullfile);
                        tag = audioFile.getTag();
                        
                        
                        
                        finfo['length'] = audioFile.getPlayTime()
                        finfo['bitrate'] = audioFile.getBitRate()[1]
                        finfo['vbr'] = audioFile.getBitRate()[0]
                        if tag is None:
                            raise # goto interp name mode
                        
                        finfo['artist'] = string.strip(tag.getArtist(), '\x00')
                        finfo['title'] = string.strip(tag.getTitle(), '\x00')

                        try:
                            g =  tag.getGenre()
                            if g is None:
                                raise
                            
                            finfo['genre'] = g.getName()
                        except:
                            finfo['genre'] = 'Unknown'
                            
                            
                            finfo['album'] = string.strip(tag.getAlbum(), '\x00')
                            finfo['track'] = tag.getTrackNum()[0]
                            
                            
                            
                            
                            
                            
                            
                    except:
                        i =  self.interp_name(file)
                        finfo['artist'] = i[0]
                        finfo['title'] = i[1]
                        finfo['genre'] = 'Unknown'
                            
                
                            
                elif file.rfind('.aif') is not -1:
                    finfo['format'] = 'aiff';
                    i =  self.interp_name(file)
                    finfo['artist'] = i[0]
                    finfo['title'] = i[1]
                    finfo['genre'] = 'Unknown'
                    
                elif file.rfind('.wav') is not -1:
                    finfo['format'] = 'wav';
                    i =  self.interp_name(file)
                    finfo['artist'] = i[0]
                    finfo['title'] = i[1]
                    finfo['genre'] = 'Unknown'
                    
                else:

                    i =  self.interp_name(file)
                    finfo['artist'] = i[0]
                    finfo['title'] = i[1]
                    finfo['genre'] = 'Unknown'
                    finfo['format'] = 'unknown'
                    

                try:
                    f = self.GC['library'].get_file(file)
                except:
                    f = {}

                try:
                    mtime = f['mtime']
                except:
                    self.GC['library'].add_file(file, finfo)
                    f = self.GC['library'].get_file(file)

                else:
                    if mtime < finfo['mtime']:
                        self.GC['library'].update_file(file, finfo)

                    
            scan_file = 0
            # /if scan_file is 1
            
        print 'files indexed'
        # The end



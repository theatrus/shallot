


import cymbeline.Dynmodule



import time


class shallotweb(cymbeline.Dynmodule.Dynmodule):


    def logout(self):
        
        self.http.session.del_session()
        
        self.http._addheaders['Location'] =  '/dynamic/welcome/welcome'
        self.serve_header(302, 'Temporary Redirect', 'text/html')
    def playlist(self):
        self.serve_html_header()



        

        music = self.GC['player'].active_playlist().songs
        self.p('<table border="0"><tr><th>Artist</th><th>Title</th><th>&nbsp;</th></tr>')
        i = 0
        lastArt = ""
        bg = "#DDDDDD"
        while i < len(music):
            x = music[i]
            if lastArt == x['artist']:
                pass
            else:
                if bg == '#DDDDDD':
                    bg = '#BBBBBB'
                else:
                    bg = '#DDDDDD'
                lastArt = x['artist']
            
            self.p('<tr bgcolor="'+bg+'"><td>' + x['artist'] + '</td>')
            self.p('<td>' + x['title'] + '</td>')

            self.p('<td><a target="playerFrame" href="player?action=request&request='+`i`+'">Play</a></td>')
            self.p('<td><a target="playerFrame" href="player?action=request&goto=0&request='+`i`+'">Queue</a></td>')
            self.p('</tr>')
            i = i + 1
        self.p('</table>')
        

    def welcome(self):
        self.serve_html_header()
        music = self.GC['library'].get_files()
        self.p('<table border="1"><tr><th>Artist</th><th>Title</th><th>File</th></tr>')
        for x in music:
            self.p('<tr><td>' + x['artist'] + '</td><td>' + x['title'] + '</td><td>' + x['file'] +  "</td></tr>")

        self.p('</table>')


    def menu(self):
        self.serve_html_header()
        
        self.p('<html><head></head><body bgcolor="#EEEECC">')
        self.p('<b>Welcome to ShallotWeb</b><br>')
        self.p('<a href="setup" target="mainFrame">Setup</a> <a href="playlist" target="mainFrame">Active Playlist View</a>')
        
        self.p('</body></html>')


    def setup(self):
        self.serve_html_header()

        try:
            libroot = self.GC['/system/settings'].read('shallot_lib')
        except:
            libroot = 'undefined'
        
        self.p('<html><head></head><body bgcolor="#FFFFFF">')
        self.p('<h1>ShallotWeb Setup</h1>')
        self.p('Library root: '+libroot)
        
        self.p('</body></html>')


    def player(self):
        
        mplayer = self.GC['player']
        apl = mplayer.active_playlist()
        
        try:
            action = self.http.form_arg['action'][0]
        except:
            action = ""

            
        if action == 'Next':
            
            mplayer.next()
            time.sleep(0.5)
            #self.http._addheaders['Location'] =  'player'
            #self.serve_header(302, 'Temporary Redirect', 'text/html')
        elif action == 'Pause':
            mplayer.pause()
        elif action == 'request':
            try:
                goto = self.http.form_arg['goto'][0]
                mplayer.request(int(self.http.form_arg['request'][0]), False)
            except:
                mplayer.request(int(self.http.form_arg['request'][0]), True)

            time.sleep(0.5)
        elif action == 'Repeat':

            if apl.playmode is 'repeat':
                apl.playmode = 'random'
            else:
                apl.playmode = 'repeat'
            
            
        self.serve_html_header()
        self.p('<html><head><META HTTP-EQUIV=Refresh CONTENT="3; URL=player"></head><body bgcolor="#EEEEEE">')
        self.p('<table border=0 width=100%>')
        self.p('<tr>')
        
        self.p('<td>')




        self.p("<b>Shallot Player: " + mplayer.status + "</b><br>")
        current_song = apl.current()
        self.p("Playing: <i>%s - %s</i>" % (current_song['artist'],
                                            current_song['title']))
        self.p(current_song['format'])
        self.p(current_song['bitrate'])


        self.p('<table border="1" style="float: right"><tr><td width="200">')
        
        self.p('<img src=/bar.gif height=4 border=2 width=' + `((mplayer.player.file.position / mplayer.player.file.length) * 200)`)
        self.p('>')
        self.p('</td></tr></table>')


        self.p("<br>" + mplayer.player.pretty_pos()[0] + "/" + mplayer.player.pretty_pos()[1])
        self.p(apl.playmode);


        self.p('</td>')
        self.p('<td width="30%">')
        
        self.p('<form method=GET>')
        self.p('<input type=submit value="Next" name=action>')
        self.p('<input type=submit value="Pause" name=action>')
#        self.p('<input type=submit value="Refresh" name=action>')

        self.p('<input type=submit value="Repeat" name=action>')
        self.p('</form>')


        self.p('</td></tr></table>')
               
        

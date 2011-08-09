

import cymbeline.Objects 


class Object(cymbeline.Objects.Object):
    """ Prevents multiple database connections being hogged by the same object. """
    def __init__(self, gc):
        self._db = None   #
        self._db_count = 0
        cymbeline.Objects.Object.__init__(self, gc)

    def get_db(self):
        if self._db is None:
            self._db = self.GC['db'].get()
            self._db_count = 1
        #else:
        #    self._db_count = self._db_count + 1
        return self._db

    def release_db(self):
        self._db_count = self._db_count - 1
        #if self._db_count is 0:
        self.GC['db'].finish(self._db)
        self._db = None
            
            

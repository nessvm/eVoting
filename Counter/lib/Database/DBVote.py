__author__ = 'nessvm'

import pg


class DBVote(pg.DB):
    """Specific class for handling the eVoting database"""

    def __init__(self):
        pg.DB.__init__(self, dbname='evoting', host='localhost', port=5432,
                       user='postgres', passwd='BL4CKh0l3')
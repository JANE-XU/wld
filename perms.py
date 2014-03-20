"""
Module handling all sorts of permissions
"""

import datetime
from storm.locals import Storm, Int, DateTime, Unicode

from wld.validator import unicoder


class BoardPerms(Storm):
    """
    I represent one of potentially many groups a user must 
    be a member of to view a Board.

    ###Example####

    board = store.add(Board())
    board.name = u'Awesome Stuff'
    board_perm = store.add(BoardPerm(name='raid_group_1'))
    board.perms.add(board_perm)
    
    user = store.add(User())
    print user.viewableBoards() #This will not include u'Awesome Stuff' in the output
    
    user.board_perms.add(board_perm)
    print user.viewableBoards() #Now u'Awesome Stuff' will be included now that user has the required permissions to view it

    ##############

    @ivar created: Timestamp of my entry in the database
    @ivar name: A name to make referencing me a bit easier and intuitive
    """
    __storm_table__ = 'boards_perms'
    id = Int(primary=True)
    created = DateTime(default=datetime.datetime.now())
    name = Unicode(validator=unicoder)


    def __init__(self, name):
        self.name = name



class _LinkBoardPerms(Storm):
    """
    I match a Board with BoardPerms required to view it.

    @ivar board_id: ID of a Board object
    @ivar perm_id: ID of a BoardPerm object
    """
    __storm_table__ = "boards_perms_link"
    id = Int(primary=True)
    board_id = Int()
    perm_id = Int()



class _LinkUserBoardPerms(Storm):
    """
    I match a User with their BoardPerms

    @ivar user_id: ID of a User object
    @ivar perm_id: ID of a BoardPerm object
    """
    __storm_table__ = "user_boards_perms_link"
    id = Int(primary=True)
    user_id = Int()
    perm_id = Int()

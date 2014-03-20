"""
Model for Boards and Threads on the Forum
"""

import datetime
from storm.locals import Storm, Int, DateTime, Unicode, ReferenceSet, Reference

from wld.db import getStore
from wld.perms import BoardPerms, _LinkBoardPerms
from wld.user import User
from wld.validator import unicoder



class Board(Storm):
    """
    I represent a category of discussion on the forums.

    @ivar created: Timestamp of my entry in the database
    @ivar name: Word or phrase that will be used to represent me on the website
    @ivar description: A brief explanation of what subject matter my Threads will contain 

    @ReferenceSet threads: A storm ReferenceSet object with all of my Threads
    @ReferenceSet perms: A storm ReferenceSet object with all permissions required for me to be viewed by a User
    """
    __storm_table__ = 'boards'
    id = Int(primary=True)
    created = DateTime(default=datetime.datetime.now())
    name = Unicode(validator=unicoder)
    description = Unicode(validator=unicoder)
    
    threads = ReferenceSet(id, "Thread.board_id")
    perms = ReferenceSet(id, "_LinkBoardPerms.board_id", "_LinkBoardPerms.perm_id", "BoardPerms.id")


    def addPermByName(self, perm_name):
        """
        Tie me to a BoardPerm by it's name.

        @param perm_name: The 'name' value of the BoardPerm to which I'll be joined.
        """
        store = getStore()
        perm = store.find(BoardPerm, BoardPerm.name == perm_name)
        self.perms.add(perm)


    def removePermByName(self, perm_name):
        """
        Remove my ties to a BoardPerm by it's name.

        @param perm_name: The 'name' value of the BoardPerm to which I'll no longer be tied
        """
        store = getStore()
        perm = store.find(BoardPerm, BoardPerm.name == perm_name)
        self.perms.remove(perm)


    def listPerms(self):
        """
        Return a list of names of BoardPerms to which I am tied
    
        @type return: A list of unicodes
        """
        perms = []
        for perm in self.perms:
            perms.append(perm.name)

        return perms



class Thread(Storm):
    """
    I represent a discussion on a Board.

    @ivar created: Timestamp of my entry in the database
    @ivar name: The topic that will be discussed
    @ivar board_id: ID of the Board to which I belong
    @ivar user_id: ID of the User that created me 

    @ReferenceSet messages: A storm ReferenceSet object with all of my Messages
    @Reference user: The User that created me.
    """
    __storm_table__ = 'boards_threads'
    id = Int(primary=True)
    created = DateTime(default=datetime.datetime.now())
    name = Unicode(validator=unicoder)
    board_id = Int()
    user_id = Int()

    board = Reference(board_id, "Board.id")
    messages = ReferenceSet(id, "Message.thread_id")
    user = Reference(user_id, "User.id")



class Message(Storm):
    """
    I am a post in a Thread.

    @ivar created: Timestamp of my entry in the database
    @ivar last_edited: Timestamp of the most-recent time my message was edited.  I am NULL by default
    @ivar message: The message the User typed to be read by other Users
    @ivar thread_id: ID of the Thread to which I belong
    @ivar user_id: ID of the User that created me

    @Reference user: The User that created me
    """
    __storm_table__ = 'boards_messages'
    id = Int(primary=True)
    created = DateTime(default=datetime.datetime.now())
    last_edited = DateTime(default=None)
    message = Unicode(validator=unicoder)
    thread_id = Int()
    user_id = Int()
    
    thread = Reference(thread_id, "Thread.id")
    user = Reference(poster_id, "User.id")


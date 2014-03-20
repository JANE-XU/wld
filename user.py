"""
I model a website user
"""

from storm.locals import Storm, Int, Unicode, DateTime

from wld.board import BoardPerms
from wld.db import getStore
from wld.perms import _LinkUserBoardPerms
from wld.validator import unicoder



class User(Storm):
    """
    I am a website user.  I can browse the site, view boards, and potentially modify other User objects.

    @ivar username: A unique name to identify me
    @ivar email: The email address tied to me
    @ivar first_name: My first name
    @ivar last_name: My surname

    @ReferenceSet board_perms: A storm ReferenceSet of all my Board permissions
    """
    __storm_table__ = 'users'
    id = Int(primary=True)
    username = Unicode(validator=unicoder)
    email = Unicode(validator=unicoder)
    first_name = Unicode(validator=unicoder)
    last_name = Unicode(validator=unicoder)
    
    board_perms = ReferenceSet(id, _LinkUserBoardPerms.user_id, _LinkUserBoardPerms.perm_id, BoardPerms.id)

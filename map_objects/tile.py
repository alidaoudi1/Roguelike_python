class Tile :
    def __init__(self,blocked,block_sight=None):
        self.blocked = blocked
        if block_sight == None:
            block_sight = blocked
        self.explored = False
        self.block_sight=block_sight
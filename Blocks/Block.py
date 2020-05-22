from Shared import GameObject
from Shared import GameConstants


class Block(GameObject):

    def __init__(self, position, surface, game):
        self.__game = game
        self.__sdistance = 0

        super().__init__(position, GameConstants.BLOCK_SIZE, surface)

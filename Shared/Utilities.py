import pygame


def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)


def load_map():
    for line in fileinput.input(os.path.join("Assets", "Levels", "level" + str(level) + ".dat")):
        for currentBlock in line:
            if currentBlock == '1':
                block = Block([x, y], load_image(GameConstants.SPRITE_BLOCK, GameConstants.BLOCK_SIZE), self)
                self.__blocks.add(block)

            x += GameConstants.BLOCK_SIZE[0]

        x = 0
        y += GameConstants.BLOCK_SIZE[1]
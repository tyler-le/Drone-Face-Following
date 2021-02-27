import pygame


# Create Game Window
def init():
    pygame.init()
    window = pygame.display.set_mode((400, 400))


# Get Key presses
def getKeypress(keyName):
    isPressed = False
    for event in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    if keyInput[myKey]:
        isPressed = True

    pygame.display.update()
    return isPressed


def main():
    if getKeypress("LEFT"):
        print("LEFT KEY PRESSED")

    if getKeypress("SPACE"):
        print("SPACE KEY PRESSED")


if __name__ == '__main__':
    init()
    while True:
        main()

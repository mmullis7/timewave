import pygame
import threading
import time


# Credit for shipImage thanks to MillionthVector
# link to his blog http://millionthvector.blogspot.de.
#
# Credit for heart pixel art:
# DontMind8.blogspot.com
#
# Credit for coin:
# dontmind8.blogspot.com
#
#


class Ship:
    """
    Description: This class is used for the ship
    """

    def __init__(self, x, y):
        """
        :param x: x cord for the ship
        :param y: y cord for the ship
        """
        self.shipImage = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/blueships.png')
        if x > 0:
            self.x = x
        else:
            x = 0
        if y > 0:
            self.y = y
        else:
            y = 0

        self.velocity = 2
        self.x_center = 300
        self.hitbox = (self.x, self.y, 95, 65)


class PowerUp:
    """
    Description: This class creates power up objects which are objects that give some type of benefit to the player
                 for example, more life, slow down time, extra points, etc.
    """

    def __init__(self, x, y, version, image, updown):
        """
        :param x:   x cord for screen
        :param y:   y cord for screen
        :param version: type of power up. Can be either 'heart', 'hourglass', 'coin'
        :param image: the image for this power up
        :param updown: True if power up item is moving up and False if moving down
        """
        if x > 0:
            self.x = x
        else:
            x = 0
        if y > 0:
            self.y = y
        else:
            y = 0

        if version == 'hourglass':
            self.version = 'hourglass'
        elif version == 'heart':
            self.version = 'heart'
        elif version == 'coin':
            self.version = coin
        else:
            self.version = 'hourglass'

        self.image = image
        self.updown = updown
        self.hitbox = (self.x, self.y, 32, 32)

    def hit(self):
        if self.version == 'hourglass':
            pass
        elif self.version == 'coin':
            pass

    def kill(self):
        # right now just throw the guy off the screen lol
        self.x = 0
        self.y = 2000


def redraw(heart, shots):
    """
    Description: this function redraws the input to the screen for everything
    """
    screen.fill((80, 80, 80))
    # heart containers
    for i in range(heart):
        screen.blit(heart16, (i*25+15, 15))

    # power ups
    for power in powerUps:
        screen.blit(power.image, (power.x, power.y))
        # pygame.draw.rect(screen, (255, 0, 0), power.hitbox, 2)

    # ship
    screen.blit(ship.shipImage, (ship.x, ship.y))
    # pygame.draw.rect(screen, (255, 0, 0), ship.hitbox, 2)

    for shot in shots:
        screen.blit(beam, shot)

    pygame.display.update()


if __name__ == "__main__":
    screenWidth = 1200
    screenHeight = 600
    dimensions = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(dimensions)

    pygame.init()
    pygame.display.set_caption("TimeWave")
    clock = pygame.time.Clock()

    # images
    heart16 = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/heart_pixel_art_16x16.png')
    heart32 = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/heart_pixel_art_32x32.png')
    hourglass = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/Hourglass.png')
    coin = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/coin.png')
    background = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/back.png')
    beam = pygame.image.load('C:/Users/18504/PycharmProjects/HelloWorld/beam.png')
    run = True  # state of game

    # create ship and power ups
    ship = Ship(300, 275)
    powerUps = [PowerUp(700, 400, 'heart', heart32, True), PowerUp(800, 100, 'hourglass', hourglass, False),
                PowerUp(900, 10, 'hourglass', hourglass, True), PowerUp(1500, 250, 'heart', heart32, False),
                PowerUp(1100, 300, 'coin', coin, True)]

    numHearts = 3  # amount of life
    beams = []

    # first draw to screen
    redraw(numHearts, beams)

    k = 0  # k is used to add small delay to updating the movement of the ship and power ups
    start = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If they click the Close button on the display
                run = False

        # Keyboard Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and ship.y > 5:  # Key: w    :   Move Ship Up
            ship.y -= 1
            ship.hitbox = (ship.x, ship.y, 95, 65)
        if keys[pygame.K_s] and ship.y < screenHeight - 69:  # key: s    :   Move ship down
            ship.y += 1
            ship.hitbox = (ship.x, ship.y, 95, 65)
        if keys[pygame.K_SPACE] and time.time() - start > 0.5:
            start = time.time()
            beams.append([ship.x + 25, ship.y + 16])

        if keys[pygame.K_a]:  # key: a    :   Slow down
            slowDown = True
        else:
            slowDown = False

        wait = 15
        if k == wait:
            k = 0
            for power in powerUps:
                if power.updown:  # if power up item is moving up
                    power.y -= 2
                    power.hitbox = (power.x, power.y, 32, 32)
                    if power.y < 5:  # begin to move down when at top of screen
                        power.updown = False
                else:  # else power up item is moving down
                    power.y += 2
                    power.hitbox = (power.x, power.y, 32, 32)
                    if power.y > screenHeight - 26:  # begin to move up if at bottom of screen
                        power.updown = True

                if slowDown:  # move all the power up items slower
                    power.x -= ship.velocity / 2
                    power.hitbox = (power.x, power.y, 32, 32)
                    if ship.x > 150:  # move the ship back a little of time until a defined distance
                        ship.x -= ship.velocity
                        ship.hitbox = (ship.x, ship.y, 95, 65)
                else:
                    power.x -= ship.velocity  # else move at normal pace
                    power.hitbox = (power.x, power.y, 32, 32)
                    if ship.x < ship.x_center:  # and move ship closer to center over time if not at center
                        ship.x += ship.velocity
                        ship.hitbox = (ship.x, ship.y, 95, 65)

        for power in powerUps:
            if power.y < ship.y + 65 and power.y + 32 > ship.y:
                if power.x + 16 < ship.x + 95 and power.x + 32 > ship.x:
                    power.hit()
                    if power.version == 'heart':
                        if numHearts < 6:
                            numHearts += 1
                        else:
                            pass
                            # add points
                    power.kill()

        k += 1
        redraw(numHearts, beams)  # redraw the screen
        if numHearts == 0:  # if you have no hearts then the game is over
            run = False

        for shot in beams:
            shot[0] += 1

    pygame.quit()

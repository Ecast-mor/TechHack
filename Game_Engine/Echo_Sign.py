import pygame

pygame.init()
currentWindow = pygame.display.Info()
windowHeight, windowWidth = currentWindow.current_h, currentWindow.current_w
screen = pygame.display.set_mode((windowWidth, windowHeight-60), pygame.SCALED)

background = "Game_Engine/tavern.jpg"
image = pygame.image.load(background)
image = pygame.transform.scale(image,(windowWidth, windowHeight-60))
rect = image.get_rect(midtop = (windowWidth//2,0))


scroll = "Game_Engine/scroll.png"
sImage = pygame.image.load(scroll)
sImage = pygame.transform.scale(sImage,(windowWidth*.30,windowHeight*.50))
sRect = sImage.get_rect(midright=(windowWidth,windowHeight-windowHeight*.25))

letters = "Game_Engine/transparent_letters.png"
lImage = pygame.image.load(letters)
lImage = pygame.transform.scale(lImage,(windowWidth*.20,windowHeight*.30))
lRect = lImage.get_rect(center = (windowWidth-sRect.x,windowHeight-windowHeight*.25))

class Game():
    def init(self):
        self.paused = False
        self.start = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    screen.blit(image, rect)
    screen.blit(sImage,sRect)
    screen.blit(lImage, lRect)
    pygame.display.update()

pygame.quit()
import pygame
import os

pygame.init()
currentWindow = pygame.display.Info()
windowHeight, windowWidth = currentWindow.current_h, currentWindow.current_w
screen = pygame.display.set_mode((windowWidth, windowHeight))

background = "Game_Engine/tavern_background.png"


image = pygame.image.load(background)
image = pygame.transform.scale(image, (windowWidth,windowHeight))
rect = image.get_rect(center=(windowWidth//2, windowHeight//2))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(image,rect)
    pygame.display.update()
pygame.quit
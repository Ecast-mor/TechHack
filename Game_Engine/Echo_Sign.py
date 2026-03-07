import pygame
import random
import os

pygame.init()

clock = pygame.time.Clock()


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

def letter_choice():
    folder = "Game_Engine/letters"

    folder_list = os.listdir(folder)
    file = random.choice(folder_list)
    full_path =  os.path.join(folder,file)
    handImage = pygame.image.load(f"{full_path}")
    handImage = pygame.transform.scale(handImage, (100,100))
    handRect = handImage.get_rect(center =(windowWidth//2,windowHeight//2))
    screen.blit(handImage,handRect)


    print(file)
        

start_time = pygame.time.get_ticks()
duration = 3000 



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill((0, 0, 0))
    screen.blit(image, rect)
    screen.blit(sImage,sRect)
    letter_choice()
    pygame.display.update()

pygame.quit()
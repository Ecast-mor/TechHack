import pygame
import random
import os
import queue
import threading 
import sys 
# sys.path.append("Core_cv")
# from handTracking import run_vision


pygame.init()
clock = pygame.time.Clock()

start_time = pygame.time.get_ticks()
duration = 3000 

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

def walksprite(dir, posx, posy, spritenum):
    folder = "Game_Engine/walksprites"

    file = str(spritenum) + ".png"
    full_path =  os.path.join(folder,dir, file)
    handImage = pygame.image.load(f"{full_path}")

    colorImage = pygame.Surface(handImage.get_size()).convert_alpha()
    color = pygame.Color(0, 255, 0)
    colorImage.fill(color)

    handImage.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

    handImage = pygame.transform.scale(handImage, (50,50))
    handRect = handImage.get_rect(center =(posx,posy))
    screen.blit(handImage,handRect)



# recived_queue = queue.Queue(maxsize=1)
# target_queue = queue.Queue(maxsize=1)



# target_queue.put("A")



# def letter_choice():
#     folder = "Game_Engine/letters"

#     folder_list = os.listdir(folder)
#     file = random.choice(folder_list)
#     full_path =  os.path.join(folder,file)
#     handImage = pygame.image.load(f"{full_path}")
#     handImage = pygame.transform.scale(handImage, (100,100))
#     handRect = handImage.get_rect(center =(windowWidth//2,windowHeight//2))
#     screen.blit(handImage,handRect)

# hand_tracking = threading.Thread(target=run_vision, args=(target_queue,recived_queue), daemon=True)
# hand_tracking.start()        

spritenum = 0
dir = "forward"

running = True
while running:
    clock.tick(60)
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # try:
        #     correct_sign = recived_queue.get_nowait()

        #     if correct_sign == "A":
        #         print("you made and A")

        #         target_queue.put("A")
        # except queue.Empty:
        #     pass

    
    screen.fill((0, 0, 0))
    screen.blit(image, rect)
    screen.blit(sImage,sRect)
    # letter_choice()
    # run_vision(target_queue, recived_queue)
    walksprite(dir, windowWidth//3, windowHeight//3, spritenum)
    spritenum = (spritenum + 1) % 4
    pygame.display.update()

pygame.quit()


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

class Customer():
    def __init__(self):
        self.animations = {}
        self.dir = "back"
        self.current_frame = 0
        self.animationTimer = 0
        self.ypos = 100

        self.load_images() 

        self.image = self.animations[self.dir][0]
        self.rect = self.image.get_rect(center=(windowWidth//2, windowHeight - self.ypos))


    def load_images(self):
        folder = "Game_Engine/walksprites"

        for subfolder in os.listdir(folder):
            subfolderPath = os.path.join(folder, subfolder)

            if os.path.isdir(subfolderPath):
                sprite_frames = []
                for file in sorted(os.listdir(subfolderPath)):
                    full_path = os.path.join(subfolderPath, file)
                    image = pygame.image.load(full_path).convert_alpha()
                    sprite_frames.append(image)

                self.animations[subfolder] = sprite_frames

    def animate(self, dt):
        frameSpeed = 100
        frames = self.animations[self.dir]

        self.animationTimer += dt

        if self.animationTimer >= frameSpeed:
            self.animationTimer = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]

    def move(self):
        if self.dir == "forward":
            self.ypos += 5
        else:
            self.ypos -= 5
        self.rect = self.image.get_rect(center=(windowWidth//2, windowHeight + self.ypos))
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
# def walksprite(dir, posx, posy, spritenum):
#     folder = "Game_Engine/walksprites"

#     file = str(spritenum) + ".png"
#     full_path =  os.path.join(folder,dir, file)
#     handImage = pygame.image.load(f"{full_path}")

#     colorImage = pygame.Surface(handImage.get_size()).convert_alpha()
#     color = pygame.Color(0, 255, 0)
#     colorImage.fill(color)

#     handImage.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

#     handImage = pygame.transform.scale(handImage, (50,50))
#     handRect = handImage.get_rect(center =(posx,posy))
#     screen.blit(handImage,handRect)

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
    handImage = pygame.transform.scale(handImage, (300,300))
    handRect = handImage.get_rect(center =(windowWidth- windowWidth*.15,(windowHeight-windowHeight*.25)))
    screen.blit(handImage,handRect)

    print(file)
        

start_time = pygame.time.get_ticks()
duration = 3000 

customer = Customer()

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
    letter_choice()
    customer.animate(5)
    customer.move()
    customer.draw()
    pygame.display.update()

pygame.quit()


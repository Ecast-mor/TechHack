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
        self.waiting = False
        self.queuenum = 0

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
                    image = pygame.transform.scale(image,(windowWidth*.03,windowHeight*.07))
                    sprite_frames.append(image)

                self.animations[subfolder] = sprite_frames

    def animate(self, dt):
        frameSpeed = 100
        frames = self.animations[self.dir]

        self.animationTimer += dt

        if self.waiting == False or (windowHeight + self.ypos) > (windowHeight // 4 + (self.queuenum * 70)):
            self.move()

            if self.animationTimer >= frameSpeed:
                self.animationTimer = 0
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]
            if ((windowHeight + self.ypos) < (windowHeight // 4 + (self.queuenum * 70))):
                self.waiting = True
        else:
            self.image = frames[0]

    def move(self):
        if self.dir == "forward":
            self.ypos += 3
            self.rect = self.image.get_rect(center=(windowWidth//2, windowHeight + self.ypos))
        else:
            self.ypos -= 3
            self.rect = self.image.get_rect(center=(windowWidth//2 - 70, windowHeight + self.ypos))
    
    def finished(self):
        self.dir = "forward"
        self.waiting = False
    
    def queueReduce(self):
        self.queuenum -= 1
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
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

customerArray = []
customerArray.append(Customer())
customerArray.append(Customer())
customerArray[1].queuenum = 1

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
    for customer in customerArray:
        customer.animate(10)
        customer.draw()
    if customerArray[0].waiting == True and customerArray[0].dir == "back":
        customerArray[0].finished()
        for customer in customerArray[1:]:
            customer.queueReduce()
    pygame.display.update()

pygame.quit()


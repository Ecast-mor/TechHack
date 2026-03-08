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

        if (windowHeight + self.ypos) > (windowHeight // 4):
            self.move()

            if self.animationTimer >= frameSpeed:
                self.animationTimer = 0
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]
        else:
            self.image = frames[0]
            self.waiting = True

    def move(self):
        if self.dir == "forward":
            self.ypos += 2
        else:
            self.ypos -= 2
        self.rect = self.image.get_rect(center=(windowWidth//2, windowHeight + self.ypos))
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
currentWindow = pygame.display.Info()
windowHeight, windowWidth = currentWindow.current_h, currentWindow.current_w
screen = pygame.display.set_mode((windowWidth, windowHeight-60), pygame.SCALED)

start = False
pause = False

font = pygame.font.SysFont(None, 50)
def Menus():
    if start == False:
        pygame.draw.rect(screen, (173, 216, 230), (0, 0, windowWidth,windowHeight))

        title = font.render("ECHO SIGN", True, (0,0,0))
        title_rect = title.get_rect(center=(windowWidth//2, (windowHeight//2)-50))
        screen.blit(title,title_rect)
        start_text = font.render("Press Space to Start", True, (0,0,0))
        start_text_rect = start_text.get_rect(center = (windowWidth//2, windowHeight//2))
        screen.blit(start_text,start_text_rect)

    elif pause == True:
        pygame.draw.rect(screen, (173, 216, 230), (0, 0, windowWidth,windowHeight))
        paused = font.render("YOU ARE", True, (0,0,0))
        paused_rect = paused.get_rect(center=(windowWidth//2, (windowHeight//2)-50))
        screen.blit(paused,paused_rect)
        pause_under = font.render("CURRENTLY PAUSED", True, (0,0,0))
        pause_under_rect = pause_under.get_rect(center = (windowWidth//2, windowHeight//2))
        screen.blit(pause_under,pause_under_rect)
        
        return_text = font.render("HIT ESCAPE TO RETURN",True, (0,0,0))
        return_rect = return_text.get_rect(center = (windowWidth//2, (windowHeight//2)+50))
        screen.blit(return_text, return_rect)
    else:
        screen.fill((0, 0, 0))
        screen.blit(image, rect)
        screen.blit(sImage,sRect)
        letter_choice()
        customer.animate(10)
        customer.draw()



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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start == False:
                start = True
            if event.key == pygame.K_p and pause == False:
                pause = True
            if event.key == pygame.K_ESCAPE and pause == True:
                pause = False

        # try:
        #     correct_sign = recived_queue.get_nowait()

        #     if correct_sign == "A":
        #         print("you made and A")

        #         target_queue.put("A")
        # except queue.Empty:
        #     pass

    Menus()
    pygame.display.update()

pygame.quit()


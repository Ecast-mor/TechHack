import pygame
import random
import os

pygame.init()

clock = pygame.time.Clock()

# class Player():
#     def __init__(self):
#         self.health = 100
#         self.attack_power = 3
#         self.speed = 5
#         self.level = 0

#         self.animations = {}
#         self.animation = "Idle"
#         self.current_frame = 0
#         self.animationTimer = 0

#         self.load_images()

#         self.image = self.animations[self.animation][0]
#         self.rect = self.image.get_rect(center=(wW//2, wH//2))
#         self.flipped = False
#         self.facingLeft = False

#         self.slash = pygame.image.load("slash.png")
#         self.slashRect = None

#         self.attacking = False

       
#     def load_images(self):
#         folder = "Knight_1"

#         for subfolder in os.listdir(folder):
#             subfolderPath = os.path.join(folder, subfolder)

#             if os.path.isdir(subfolderPath):
#                 sprite_frames = []
#                 for file in sorted(os.listdir(subfolderPath)):
#                     full_path = os.path.join(subfolderPath, file)
#                     image = pygame.image.load(full_path).convert_alpha()
#                     sprite_frames.append(image)

#                 self.animations[subfolder] = sprite_frames
        
        

#     def animate(self, dt):
#         frameSpeed = 100
#         frames = self.animations[self.animation]

#         self.animationTimer += dt

#         if self.animationTimer >= frameSpeed:
#             self.animationTimer = 0
#             self.current_frame = (self.current_frame + 1) % len(frames)
#             self.image = frames[self.current_frame]
        
#         if self.animation.startswith("Attack"):
#             self.attacking = False
#             self.slashRect = None
        
#     def flip_animation(self):
#              for animation_name in self.animations:
#                 flipped_frames = []
#                 for frame in self.animations[animation_name]:
#                     flipped = pygame.transform.flip(frame, True, False)
#                     flipped_frames.append(flipped)

#                 self.animations[animation_name] = flipped_frames

#     def draw(self):
#         screen.blit(self.image, self.rect)


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
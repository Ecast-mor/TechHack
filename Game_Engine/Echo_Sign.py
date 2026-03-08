import pygame
import random
import os
import queue
import threading 
import sys 
sys.path.append("Core_cv")
from handTracking import run_vision


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

def get_new_letter_image():
    folder = "Game_Engine/letters"
    folder_list = os.listdir(folder)
    file = random.choice(folder_list)
    target_name = file.split('.')[0].upper()
    full_path =  os.path.join(folder,file)
    handImage = pygame.image.load(f"{full_path}")
    handImage = pygame.transform.scale(handImage, (300,300))
    

    print(file)
    return target_name, handImage

target_queue = queue.Queue()
result_queue = queue.Queue()
frame_queue = queue.Queue(maxsize=30) 

vision_thread = threading.Thread(target=run_vision, args=(target_queue, result_queue, frame_queue))
vision_thread.daemon = True
vision_thread.start()



start_time = pygame.time.get_ticks()
duration = 3000 

customerArray = []
customerArray.append(Customer())
current_letter_name, current_letter_image = get_new_letter_image() # Load the first letter before the loop starts
target_queue.put(current_letter_name) # Send the first target to the vision thread
handRect = current_letter_image.get_rect(center =(windowWidth- windowWidth*.15,(windowHeight-windowHeight*.25)))
latest_camera_frame = None 


running = True
while running:
    dt = clock.tick(60)
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        correct_sign = result_queue.get_nowait()

        if correct_sign == current_letter_name:
            print(f"you made an {correct_sign}!")
            current_letter_name, current_letter_image = get_new_letter_image()
            handRect = current_letter_image.get_rect(center =(windowWidth- windowWidth*.15,(windowHeight-windowHeight*.25)))
            target_queue.put(current_letter_name)
    except queue.Empty:
        pass
        
    try:
    # Loop until empty so we always get the freshest frame and prevent lag
        latest_camera_frame = frame_queue.get_nowait()
        
    except queue.Empty:
        pass

    
    screen.fill((0, 0, 0))
    screen.blit(image, rect)
    screen.blit(sImage,sRect)

    screen.blit(current_letter_image, handRect)

    customerArray[0].animate(dt)
    customerArray[0].draw()

    if latest_camera_frame is not None:
        # Draw it in the top left corner (x=20, y=20)
        screen.blit(latest_camera_frame, (20, 20))

    for customer in customerArray:
        customer.animate(10)
        customer.draw()
    if customerArray[0].waiting == True and customerArray[0].dir == "back":
        customerArray[0].finished()
        for customer in customerArray[1:]:
            customer.queueReduce()
    pygame.display.update()

pygame.quit()


import pygame
import random
import os
import queue
import threading 
import sys 
sys.path.append("Core_cv")
from handTracking import run_vision


customerArray = []
customerQueue = 0
currentCustomer = 0

pygame.init()
music = pygame.mixer.Sound("Game_Engine/Music.wav")
clock = pygame.time.Clock()

class Customer():
    def __init__(self, letter, queuenum):
        self.animations = {}
        self.dir = "back"
        self.current_frame = 0
        self.animationTimer = 0
        self.ypos = 100
        self.waiting = False
        self.queuenum = queuenum
        self.letter = letter

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
            self.ypos += 5
            self.rect = self.image.get_rect(center=(windowWidth//2, windowHeight + self.ypos))
        else:
            self.ypos -= 5
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

font = pygame.font.Font(None, 50)
start = False
pause = False

def Menus():
    global customerArray
    global customerQueue
    global currentCustomer
    if start == False:
        pygame.draw.rect(screen, (173, 216, 230), (0, 0, windowWidth,windowHeight))
        logo = pygame.image.load("Game_Engine/ECHO_SIGN.png") 
        logoRect = logo.get_rect(center = (windowWidth//2, windowHeight//4))
        screen.blit(logo, logoRect)

        start_text = font.render("Press Space to Start", True, (0,0,0))
        start_text_rect = start_text.get_rect(center = (windowWidth//2, windowHeight//2))
        screen.blit(start_text,start_text_rect)

    elif pause == True:
        pygame.mixer.pause()
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
        pygame.mixer.Sound.play(music)

        screen.fill((0, 0, 0))
        screen.blit(image, rect)
        screen.blit(bImage,bRect)
        screen.blit(sImage,sRect)
        pygame.draw.rect(screen, (0,0,0),(20,20,340,260))
        screen.blit(current_letter_image, handRect)

        if latest_camera_frame is not None:
            # Draw it in the top left corner (x=20, y=20)
            screen.blit(latest_camera_frame, (20, 20))

        for customer in customerArray:
            customer.animate(dt)
            customer.draw()

        if customerArray[0].ypos > windowHeight:
                del customerArray[0]
                currentCustomer -= 1


        if (random.randint(0,150) == 50 or customerQueue < 2) and customerQueue < 12 :
            customerArray.append(Customer(get_new_letter(), customerQueue))
            customerQueue += 1
        render_letter(current_letter_name, handRect)
        

background = "Game_Engine/tavern.jpg"
image = pygame.image.load(background)
image = pygame.transform.scale(image,(windowWidth, windowHeight-60))
rect = image.get_rect(midtop = (windowWidth//2,0))

bartender = "Game_Engine/Plant2_Idle.png"
bImage = pygame.image.load(bartender)
bImage = pygame.transform.scale(bImage,(102, 114))
bRect = bImage.get_rect(midtop = (windowWidth//2 - 65,55))

scroll = "Game_Engine/scroll.png"
sImage = pygame.image.load(scroll)
sImage = pygame.transform.scale(sImage,(windowWidth*.30,windowHeight*.50))
sRect = sImage.get_rect(midright=(windowWidth,windowHeight-windowHeight*.25))

def get_new_letter_image(letter):
    folder = "Game_Engine/letters"
    file = letter.lower() + ".png"
    target_name = letter[0]
    full_path =  os.path.join(folder,file)
    
    handImage = pygame.image.load(f"{full_path}")
    handImage = pygame.transform.scale(handImage, (300,300))

    return target_name, handImage

def render_letter(letter, handRect):
    sign_letter = font.render(f"{letter}", True, (0,0,0))
    
    sign_letter_rect = sign_letter.get_rect(center =(handRect.x + 150,handRect.y + 275))
    screen.blit(sign_letter, sign_letter_rect)

def get_new_letter():
    return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

target_queue = queue.Queue()
result_queue = queue.Queue()
frame_queue = queue.Queue(maxsize=30) 

vision_thread = threading.Thread(target=run_vision, args=(target_queue, result_queue, frame_queue))
vision_thread.daemon = True
vision_thread.start()


start_time = pygame.time.get_ticks()
duration = 3000 

current_letter_name, current_letter_image = get_new_letter_image(get_new_letter()) # Load the first letter before the loop starts
customerArray.append(Customer(current_letter_name, customerQueue))
customerQueue += 1
target_queue.put(current_letter_name) # Send the first target to the vision thread
handRect = current_letter_image.get_rect(center =(windowWidth- windowWidth*.15,(windowHeight-windowHeight*.25)))
render_letter(current_letter_name, handRect)
latest_camera_frame = None 

running = True
while running:
    dt = clock.tick(60)
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
                pygame.mixer.unpause()
                pause = False
    try:
        correct_sign = result_queue.get_nowait()

        if correct_sign == current_letter_name:
            # print(f"you made an {correct_sign}!")
            customerArray[currentCustomer].finished()
            currentCustomer += 1
            customerQueue -= 1
            for customer in customerArray[currentCustomer:]:
                customer.queueReduce()
            current_letter_name, current_letter_image = get_new_letter_image(customerArray[currentCustomer].letter)
            handRect = current_letter_image.get_rect(center =(windowWidth- windowWidth*.15,(windowHeight-windowHeight*.25)))
            target_queue.put(customerArray[currentCustomer].letter)
    except queue.Empty:
        pass
        
    try:
    # Loop until empty so we always get the freshest frame and prevent lag
        latest_camera_frame = frame_queue.get_nowait()
        
    except queue.Empty:
        pass

    Menus()

    pygame.display.update()

pygame.quit()


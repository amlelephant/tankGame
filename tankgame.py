'''
Created on Apr 15, 2024
'''
import pygame, sys
from pygame.locals import QUIT
import random
from pickle import FALSE

#CONSTANT VARIABLE CREATION
COOLDOWN = 0.03
COLOR = (255, 100, 98) 
WHITE = 255,255,255
BLACK = 0,0,0
SURFACE_COLOR = (0,0,0) 
WIDTH = 1000
HEIGHT = 1000
SPEED = 3
BULLETSPEED = 18
red = (210, 43, 43)
DISPLAYSURF = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Hello World!')


gamelife=True
winner=""

#TANK CLASS
class tank(pygame.sprite.Sprite):
    def __init__(self, height, width):
        super().__init__()
        self.health = 2
        self.cooldown = 0
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR)
        self.orientation = "up"
        self.speed = SPEED
        self.collideOrientation = "up"

        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height)) 

        self.rect = self.image.get_rect() 

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, pixels):
        self.rect.y += pixels

    def moveBack(self, pixels):
        self.rect.y -= pixels

#BULLET CLASS
class bullet(tank):
    def __init__(self,width,height):
        super().__init__(width,height)
        self.isFired = False
        self.image=pygame.Surface([width,height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        self.orientation = "up"

        pygame.draw.rect(self.image,red,pygame.Rect(0,0,width,height))

        self.rect=self.image.get_rect()
    def fireup(self):
        self.isFired = True
    def firedown(self):
        self.isFired = True

#BULLET RESET FUNC
def normPos1():
    bullet1.rect.x=(tank1.rect.x + (tank1.rect.width/2) - (bullet1.rect.width/2))
    bullet1.rect.y=(tank1.rect.y + (tank1.rect.height/2) - (bullet1.rect.height/2))
def normPos2():
    bullet2.rect.x=(tank2.rect.x + (tank2.rect.width/2) - (bullet2.rect.width/2))
    bullet2.rect.y=(tank2.rect.y + (tank2.rect.height/2) - (bullet2.rect.height/2))

#FIRE LOGIC
def fire_logic():

    #tank1 up
    if bullet1.isFired and bullet1.orientation == "up":
        if bullet1.rect.y>0 and bullet1.rect.y<1000:
            bullet1.rect.y-=BULLETSPEED
            if bullet1.rect.y<1 or bullet1.rect.y>999:
                normPos1()
                bullet1.isFired=False
    #tank1 down
    if bullet1.isFired and bullet1.orientation == "down":
        if bullet1.rect.y>0 and bullet1.rect.y<1000:
            bullet1.rect.y+=BULLETSPEED
            if bullet1.rect.y<1 or bullet1.rect.y>999:
                normPos1()
                bullet1.isFired=False
    #tank1 left
    if bullet1.isFired and bullet1.orientation == "left":
        if bullet1.rect.x>0 and bullet1.rect.x<1000:
            bullet1.rect.x-=BULLETSPEED
            if bullet1.rect.x<1 or bullet1.rect.x>999:
                normPos1()
                bullet1.isFired=False

    #tank1 right
    if bullet1.isFired and bullet1.orientation == "right":
        if bullet1.rect.x>0 and bullet1.rect.x<1000:
            bullet1.rect.x+=BULLETSPEED
            if bullet1.rect.x<1 or bullet1.rect.x>999:
                normPos1()
                bullet1.isFired=False
    #tank2 up
    if bullet2.isFired and bullet2.orientation == "up":
        if bullet2.rect.y>0 and bullet2.rect.y<1000:
            bullet2.rect.y-=BULLETSPEED
            if bullet2.rect.y<1 or bullet2.rect.y>999:
                normPos2()
                bullet2.isFired=False
    #tank2 down
    if bullet2.isFired and bullet2.orientation == "down":
        if bullet2.rect.y>0 and bullet2.rect.y<1000:
            bullet2.rect.y+=BULLETSPEED
            if bullet2.rect.y<1 or bullet2.rect.y>999:
                normPos2()
                bullet2.isFired=False
    #tank2 left
    if bullet2.isFired and bullet2.orientation == "left":
        if bullet2.rect.x>0 and bullet2.rect.x<1000:
            bullet2.rect.x-=BULLETSPEED
            if bullet2.rect.x<1 or bullet2.rect.x>999:
                normPos2()
                bullet2.isFired=False
    #tank2 right
    if bullet2.isFired and bullet2.orientation == "right":
        if bullet2.rect.x>0 and bullet2.rect.x<1000:
            bullet2.rect.x+=BULLETSPEED
            if bullet2.rect.x<1 or bullet2.rect.x>999:
                normPos2()
                bullet2.isFired=False

#TEXT DISPLAYER    
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#Collision Logic
def bulletcoll():
    global tank1life
    global tank2life
    if pygame.sprite.collide_mask(bullet1,tank2):
        tank2life-=1
        bullet1.isFired=False
        bullet2.isFired=False
        normPos1()
        normPos2()
    if pygame.sprite.collide_mask(bullet2,tank1):
        tank1life-=1
        bullet1.isFired=False
        bullet2.isFired=False
        normPos1()
        normPos2()
    if pygame.sprite.collide_mask(bullet1,bullet2):
        bullet1.isFired=False
        bullet2.isFired=False
        normPos1()
        normPos2()
    for item in rectangles:
        if pygame.Rect.colliderect(bullet1.rect, item):
            bullet1.isFired=False
            normPos1()
        if pygame.Rect.colliderect(bullet2.rect, item):
            bullet2.isFired=False
            normPos2()

#TANK COLLISION LOGIC
def tankcoll():
    if pygame.sprite.collide_mask(tank1,tank2):
        if tank1.orientation == "up":
            tank1.moveBack(SPEED)
            normPos1()
        if tank1.orientation == "down":
            tank1.moveForward(SPEED)
            normPos1()
        if tank1.orientation == "left":
            tank1.moveRight(SPEED)
            normPos1()
        if tank1.orientation == "right":
            tank1.moveLeft(SPEED)
            normPos1()
        if tank2.orientation == "up":
            tank2.moveBack(SPEED)
            normPos2()
        if tank2.orientation == "down":
            tank2.moveForward(SPEED)
            normPos2()
        if tank2.orientation == "left":
            tank2.moveRight(SPEED)
            normPos2()
        if tank2.orientation == "right":
            tank2.moveLeft(SPEED)
            normPos2()
        
    for item in rectangles:
        if pygame.Rect.colliderect(tank1.rect, item):
            tank1.speed = 0
            if tank1.orientation == "up":
                
                tank1.moveForward(SPEED)
                normPos1()
            if tank1.orientation == "down":
                tank1.moveBack(SPEED)
                normPos1()
            if tank1.orientation == "left":
                tank1.moveRight(SPEED)
                normPos1()
            if tank1.orientation == "right":
                tank1.moveLeft(SPEED)
                normPos1()
        if pygame.Rect.colliderect(tank2.rect, item):
            tank2.speed = 0
            if tank2.orientation == "up":
                tank2.moveForward(SPEED)
                normPos2()
            if tank2.orientation == "down":
                tank2.moveBack(SPEED)
                normPos2()
            if tank2.orientation == "left":
                tank2.moveRight(SPEED)
                normPos2()
            if tank2.orientation == "right":
                tank2.moveLeft(SPEED)
                normPos2()
            

#INITAL POS CORRECTION
def initCorrect():
    for item in rectangles:
        if pygame.Rect.colliderect(tank1.rect, item):
            if tank1.orientation == "up":
                tank1.moveForward(SPEED)
                normPos1()
            if tank1.orientation == "down":
                tank1.moveBack(SPEED)
                normPos1()
            if tank1.orientation == "left":
                tank1.moveRight(SPEED)
                normPos1()
            if tank1.orientation == "right":
                tank1.moveLeft(SPEED)
                normPos1()
        if pygame.Rect.colliderect(tank2.rect, item):
            if tank2.orientation == "up":
                tank2.moveForward(SPEED)
                normPos2()
            if tank2.orientation == "down":
                tank2.moveBack(SPEED)
                normPos2()
            if tank2.orientation == "left":
                tank2.moveRight(SPEED)
                normPos2()
            if tank2.orientation == "right":
                tank2.moveLeft(SPEED)
                normPos2()

#WIN LOGIC
def getwin():
    global tank1life
    global tank2life
    global gamelife
    global winner
    if tank1life <=0:
        gamelife = False
        winner="TANK 2!"
    elif tank2life<=0:
        gamelife = False
        winner="TANK 1!"

#PYGAME CREATION
pygame.init() 

size = (WIDTH, HEIGHT) 
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Creating Sprite") 

font1 = pygame.font.Font(None, 24)

all_sprites_list = pygame.sprite.Group() 

#VARIABLE CREATION
tank1 = tank(20, 20) 
tank1.rect.x = 500
tank1.rect.y = 750
bullet1=bullet(5,5)

tank2 = tank(20, 20) 
tank2.rect.x = 500
tank2.rect.y = 250
bullet2=bullet(5,5)

tank1life=5
tank2life=5

#SPRITE CREATION
bullet1.rect.x=(tank1.rect.x + (tank1.rect.width/2) - (bullet1.rect.width/2))
bullet1.rect.y=(tank1.rect.y + (tank1.rect.height/2) - (bullet1.rect.height/2))
all_sprites_list.add(tank1,bullet1)

bullet2.rect.x=(tank2.rect.x + (tank2.rect.width/2) - (bullet2.rect.width/2))
bullet2.rect.y=(tank2.rect.y + (tank2.rect.height/2) - (bullet2.rect.height/2))
all_sprites_list.add(tank2,bullet2) 

def generate_rectangles():
    rectangles = []
    num_rectangles = random.randint(5, 20)  # Adjust the range of the number of rectangles as needed

    for _ in range(num_rectangles):
        rect_width = random.randint(50, 200)  # Adjust the range of rectangle width as needed
        rect_height = random.randint(50, 200)  # Adjust the range of rectangle height as needed

        # Generate random position until no overlap
        while True:
            x = random.randint(0, WIDTH - rect_width)
            y = random.randint(0, HEIGHT - rect_height)
            new_rect = pygame.Rect(x, y, rect_width, rect_height)
            overlap = False
            for existing_rect in rectangles:
                if new_rect.colliderect(existing_rect):
                    overlap = True
                    break
            if not overlap:
                rectangles.append(new_rect)
                break

    return rectangles

def draw_map(rectangles):
    for rect in rectangles:
        pygame.draw.rect(screen, BLACK, rect)

rectangles=generate_rectangles()
def rectcollison():
    for item in rectangles:
        if pygame.Rect.colliderect(tank1.rect, item):
            pass
        if pygame.Rect.colliderect(tank2.rect, item):
            pass
initCorrect()
exit = True
clock = pygame.time.Clock() 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if gamelife == True:
        screen.fill(WHITE)
        #MAP CREATION
        rectcollison()
        draw_map(rectangles)
        bulletcoll()
        tankcoll()
        #TEXT DISPLAY
        print_text(font1, 900, 980, "TANK 1", BLACK)
        print_text(font1, 900, 10, "TANK 2", BLACK)
        print_text(font1, 10, 10, "Tank 1 life: "+str(tank1life), BLACK)
        print_text(font1,120,10,"Tank 2 life: "+str(tank2life),BLACK)
        #MOVEMENT LOGIC
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tank1.moveLeft(tank1.speed)
            tank1.orientation = "left"
            if bullet1.isFired == False:
                normPos1()
        if keys[pygame.K_RIGHT]:
            tank1.moveRight(tank1.speed)
            tank1.orientation = "right"
            if bullet1.isFired == False:
                normPos1()
        if keys[pygame.K_DOWN]:
            tank1.moveForward(tank1.speed)
            tank1.orientation = "down"
            if bullet1.isFired == False:
                normPos1()
        if keys[pygame.K_UP]:
            tank1.orientation = "up"
            tank1.moveBack(tank1.speed)
            if bullet1.isFired == False:
                normPos1()
        if keys[pygame.K_RCTRL]:
            if bullet1.isFired == False and tank1.cooldown <= 0:
                bullet1.orientation = tank1.orientation
                bullet1.fireup()
                tank1.cooldown = 1
        if keys[pygame.K_a]:
            tank2.orientation = "left"
            tank2.moveLeft(tank2.speed)
            if bullet2.isFired == False:
                normPos2()
        if keys[pygame.K_d]:
            tank2.orientation = "right"
            tank2.moveRight(tank2.speed)
            if bullet2.isFired == False:
                normPos2()
        if keys[pygame.K_s]:
            tank2.orientation = "down"
            tank2.moveForward(tank2.speed)
            if bullet2.isFired == False:
                normPos2()
        if keys[pygame.K_w]:
            tank2.moveBack(tank2.speed)
            tank2.orientation = "up"
            if bullet2.isFired == False:
                normPos2()
        if keys[pygame.K_LSHIFT]:
            if bullet2.isFired == False and tank2.cooldown <= 0:
                bullet2.orientation = tank2.orientation
                bullet2.fireup()
                tank2.cooldown = 1

        #FIRE LOGIC
        fire_logic()
        if tank1.cooldown > 0:
            tank1.cooldown -= COOLDOWN
        if tank2.cooldown > 0:
            tank2.cooldown -= COOLDOWN

        #CHECK WIN
        getwin()

        #RESET SPEED
        for item in rectangles:
            if pygame.Rect.colliderect(tank1.rect, item) == False:
                tank1.speed = SPEED
            if pygame.Rect.colliderect(tank2.rect, item) == False:
                tank2.speed = SPEED

        #DISPLAY SYSTEM
        all_sprites_list.update() 
        all_sprites_list.draw(screen) 
        pygame.display.flip() 
        clock.tick(60)

        pygame.display.update()
    else:
        screen.fill(SURFACE_COLOR) 
        print_text(font1,500,500,"GAME OVER! WINNER IS "+winner,WHITE)
        clock.tick(60)
        pygame.display.update()
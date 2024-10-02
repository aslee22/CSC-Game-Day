# -*- coding: utf-8 -*-
"""
Team Name:

Team Members:
    

Game Name:
    
"""
import random
import pygame


#player class

class player_main():
    def __init__(self):
        self.siz = 40
        self.col = "white"
        self.speed = 5
        self.hp = 1
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        
        
#enemy class
        
class enemy():
    def __init__(self, x,y, direc):
        self.pos = pygame.Vector2(x,y) #personal x and y coordinates
        self.col = "red"    #color of enemy
        self.direX = 0      #direction x so -1 or 1
        self.direY = 0      #direction y so -1 or 1
        self.siz = 30       #size of enemy
        self.directi = direc #can be R for Right, L for Left, U for Up, and D for Down of where it's headed
        
        if self.directi == "R":
            self.direX = 1
        if self.directi == "L":
            self.direX = -1
        if self.directi == "U":
            self.direY = -1
        if self.directi == "D":
            self.direY = 1
            
        self.speed = 5
        self.move_x = self.speed * self.direX
        self.move_Y = self.speed * self.direY
    def move(self):
        self.pos.x += self.move_x    #move in x direction
        self.pos.y += self.move_Y    #move in y direction
    def draw(self, screen):
        pygame.draw.rect(screen, self.col, pygame.Rect(self.pos.x-self.siz/2,  self.pos.y-self.siz/2, self.siz, self.siz))
    def collision_with_player(self, player_x, player_y, player_size):
        if (player_x < self.pos.x + self.siz and player_x + player_size > self.pos.x and player_y < self.pos.y + self.siz and player_y + player_size > self.pos.y):
            return True  # Collision detected
        return False  # No collision
            
    
    
#Enemy Spawner
"""
Spawns the red enemy blocks

"""
class enemy_spawner():
    def __init__(self, x,y, directi, wait, screen_height, screen_width):
        self.enemy_direct = directi
        self.pos = pygame.Vector2(x,y)      #spawner position (x,y)
        self.screen_h = screen_height
        self.screen_w = screen_width                 
        self.wait_spawn = wait      #wait time before enemy spawns
        self.siz = 40           #size of it, but doesn't matter much
        self.self_time = 0      #spawner timer count
        
    def update(self, enemy_array):
        self.self_time += 1
        if self.self_time > self.wait_spawn:        #If self_time > wait.spawn
            enemy_array.append(enemy(self.pos.x, self.pos.y, self.enemy_direct)) #spawn enemy at current (x,y) position
            self.self_time = 0
        
        #move to random location after spawning enemy
        if self.enemy_direct == "R" or self.enemy_direct == "L":
            self.pos.y = random.randint(self.siz, self.screen_h - self.siz)
        elif self.enemy_direct == "U" or  self.enemy_direct == "D":
            self.pos.x = random.randint(self.siz, self.screen_w - self.siz)

            
        
        
    
    
#player health
player_health = 0
    
def enemy_updates(curr_time, screen, enemy_arr, spawner_arr, player_x, player_y, player_size):
    i = 0
    while i < len(enemy_arr):    #loop through enemy array
        enemy_arr[i].move()      #make each enemy move from the array
        enemy_arr[i].draw(screen)    #draws the enemy 
        collided = False
        collided = enemy_arr[i].collision_with_player(player_x, player_y, player_size)    #Handles collision for each enemy with player
        
        if enemy_arr[i].pos.x > screen.get_width() or enemy_arr[i].pos.x < 0 or enemy_arr[i].pos.y > screen.get_height() or enemy_arr[i].pos.y < 0:    #If enemy goes out of bounds
            enemy_arr.pop(i)       #deletes the enemy
        elif collided == True:      #Checks if enemy collides with player
            enemy_arr.pop(i)    #deletes enemy
            global player_health
            player_health -=1
        
        i += 1
    for i in range(len(spawner_arr)):
        spawner_arr[i].update(enemy_arr)        #Updates Spawners

        
        
    
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


curr_time = 0 #counter for spawner
score = 0       #your score

enemy_array = []        #array for enemies
spawner_array = []      #array for spawners


# Game Screen Name text
pygame.display.set_caption('Simple Game')




# Set up font and size
font = pygame.font.SysFont(None, 100)  # Default font, size 100
# Set up text object for The End screen
text = font.render('The End', True, (0, 0, 0))  # Black color for the text
# Get the rectangle of the text to center it
text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))



#Set 4 spawners on each side of the screen.
spawner_array.append(enemy_spawner(0, screen.get_height() / 2, "R", 100, screen.get_height(), screen.get_width()))
spawner_array.append(enemy_spawner(screen.get_width(), screen.get_height() / 2, "L", 100, screen.get_height(), screen.get_width()))
spawner_array.append(enemy_spawner(screen.get_width() /2 , screen.get_width(), "U", 100, screen.get_height(), screen.get_width()))
spawner_array.append(enemy_spawner(screen.get_width() /2 , 0, "D", 100, screen.get_height(), screen.get_width()))


#Creates player object
player = player_main()
player_health = player.hp #sets health
player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #Sets player position

screentype = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if screentype == 0:
    # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        curr_time += 0.01 #increase time
        
        
        #Draw player on screen
        pygame.draw.rect(screen, "white", pygame.Rect(player.pos.x-player.siz/2,  player.pos.y-player.siz/2, player.siz, player.siz))
        
        #Move around keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
                player.pos.y -= 300 * dt
        if keys[pygame.K_s]:
                player.pos.y += 300 * dt
        if keys[pygame.K_a]:
                player.pos.x -= 300 * dt
        if keys[pygame.K_d]:
                player.pos.x += 300 * dt
        
        #Calls the enemy updates method
        enemy_updates(curr_time, screen, enemy_array, spawner_array, player.pos.x, player.pos.y, player.siz)
        
        
        score += 1/500 #Adds your score
        
        #The You Die and Score
        if player_health <= 0:
            screentype = 1
            print("You Died.")
            print("Score: "+str(round(score)))
        
    #Death screen
    if screentype == 1:
         screen.fill("white")
         screen.blit(text, text_rect)
         

        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    


pygame.quit()


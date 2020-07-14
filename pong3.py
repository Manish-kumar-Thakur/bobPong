#importing libraries

import os
import pygame
import sys
import time
import math
import random


pygame.init()
from pygame.locals import *

#frames per seconds
FPS =60

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 750
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#creating a clock object from pygame.time.Clock class
clock = pygame.time.Clock()

# Game Title
pygame.display.set_caption("Pong Game 3.8")
pygame.display.update()

def displaytext(text,fontsize,x,y,color):
    font = pygame.font.SysFont('sawasdee', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    gameWindow.blit(text, textpos)


def cpumove(cpu,ball):
    if ball.movement[0] > 0: #ensures that the CPU moves only when the ball is directed towards it
        #the extra addition of cpu.rect.height/5 ensures that the CPU will miss the ball sometimes
        if ball.rect.bottom > cpu.rect.bottom + cpu.rect.height/5:
            cpu.movement[1] = 10
        elif ball.rect.top < cpu.rect.top - cpu.rect.height/5:
            cpu.movement[1] = -10
        else:
            cpu.movement[1] = 0
    else:
        cpu.movement[1] = 0


class Paddle(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex,sizey),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image,self.color,(0,0,sizex,sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0,0]


    #A function which checks whether the paddle is going out of bounds and make corrections accordingly
    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    #An update function which updates the state and position of the paddle
    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    #A draw function which draws our paddle onto the screen
    def draw(self):
        #pygame.draw.rect(self.image,self.color,(0,0,self.sizex,self.sizey))
        gameWindow.blit(self.image,self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x , y , size , color , movement=[0 , 0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement = movement
        self.image = pygame.Surface((size , size), pygame.SRCALPHA , 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(size/2))
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 9
        self.score = 0
        self.movement = movement
        # This update functions detemines how the ball will move

    def update(self):
        if self.rect.top <= 0 or self.rect.bottom >=screen_height:  # reverses the vertical velocity on collision with top and bottom walls
            self.movement[1] = -1 * self.movement[1]
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.movement[0] = -1 * self.movement[0]
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = 1
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self):
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(self.size/2))
        gameWindow.blit(self.image,self.rect)

#The main function of our program
def main():
    game_over = False
    paddle = Paddle(screen_width / 10,screen_height/ 2, screen_width / 60, screen_height / 8, white)
    ball = Ball(screen_width / 2, screen_height/ 2, int(screen_width/48), red, [5, 5])
    cpu = Paddle(screen_width - screen_width / 10, screen_height / 2, screen_width / 60, screen_height / 8, white)


    # Game Loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:  # checks whether a key has been pressed or not
                if event.key == pygame.K_UP:  # If user has pressed the UP key
                    paddle.movement[1] = -9

                elif event.key == pygame.K_DOWN:  # If user has pressed the down key
                    paddle.movement[1] = 9  # Paddle moves downwards
            if event.type == pygame.KEYUP:  # If the user lifts the key
                paddle.movement[1] = 0  # Paddle stops moving
                if event.key == pygame.K_a:#cheat code
                    paddle.points +=1
        cpumove(cpu,ball)
        gameWindow.fill(black)
        pygame.draw.line(gameWindow, white, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # drawing user's paddle, cpu's paddle and ball
        paddle.draw()
        ball.draw()
        cpu.draw()

        # displaying the po.ints scored by the user and cpu
        displaytext(str(paddle.points), 20, screen_width / 8, 25, (white))
        displaytext(str(cpu.points), 20, screen_width - screen_width / 8, 25, (white))

        if pygame.sprite.collide_mask(paddle,ball):
            ball.movement[0] = -1 * ball.movement[0]
            ball.movement[1] = ball.movement[1] - paddle.movement[1]
            #print("SCORE!")
        if pygame.sprite.collide_mask(cpu,ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1]- cpu.movement[1]
        if ball.score == 1:
            cpu.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0

        paddle.update()
        ball.update()
        cpu.update()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()
main()







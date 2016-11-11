#!/usr/bin/env python 

""" 
A simple echo client 
""" 

import socket, pickle,pygame,os,sys,random
from pygame.locals import *

WHITE = 255,255,255
GREEN = 0,255,0
BLACK = 0,0,0
BLUE  = 0,0,255
RED   = 255,0,0

newMap = [[0 for x in range(9)] for x in range(9)]

            
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Tile")
pygame.init()


host = 'localhost' 
port = 50000 
size = 1024

idnum=None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port)) 
s.send('hello')
data=s.recv(size)
s.close()
idnum=int(data)
playerY=random.randint(1,8)
playerX=random.randint(1,8)

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port)) 
    s.send('mov,'+str(playerX)+','+str(playerY)+','+str(idnum)) 
    data = s.recv(size) 
    s.close()
    data=pickle.loads(data)
    newMap=data
    
    for y in range(0,len(newMap)):
        for x in range(0,len(newMap)):
            if newMap[x][y]==0:
                pygame.draw.rect(screen, GREEN, ((x-1)*50,(y-1)*50,50,50),0)
            if newMap[x][y]==1:
                pygame.draw.rect(screen, RED, ((x-1)*50,(y-1)*50,50,50),0)
                
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.display.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit(0)
            if event.key == K_UP:
                playerY=playerY-1
            if event.key == K_DOWN:
                playerY=playerY+1
            if event.key == K_LEFT:
                playerX = playerX-1
            if event.key == K_RIGHT:
                playerX=playerX+1
    
    clock.tick()
    pygame.display.update()
    #print(clock.get_fps())
    pygame.time.delay(100)

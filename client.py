#!/usr/bin/env python 

""" 
A simple echo client 
""" 

import socket, pickle,pygame,os,sys,random
from pygame.locals import *

colors=[
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,0,255),
    (140,204,230),
    ]
"""
players(1-5)
wall

"""

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
gridX=0
gridY=0

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    gridX=(playerX+50)//50+1
    gridY=(playerY+50)//50+1
    s.send('mov,'+str(gridX)+','+str(gridY)+','+str(idnum)) 
    data = s.recv(size) 
    s.close()
    data=pickle.loads(data)
    newMap=data
    
    for y in range(0,len(newMap)):
        for x in range(0,len(newMap)):
            if newMap[x][y]==0:
                pygame.draw.rect(screen, (139,69,19), ((x-1)*50,(y-1)*50,50,50),0)
            else:
                #Don't Draw Youself
                if newMap[x][y]!=idnum:
                    pygame.draw.rect(screen, colors[newMap[x][y]], ((x-1)*50,(y-1)*50,50,50),0)
                
    #Draw Yourself
    pygame.draw.rect(screen,colors[idnum],(playerX+25,playerY+25,50,50),0)
    pygame.display.update()
    keys=pygame.key.get_pressed()

    if keys[K_LEFT]:
        playerX-=10
    if keys[K_RIGHT]:
        playerX+=10

    if keys[K_UP]:
        playerY-=10

    if keys[K_DOWN]:
        playerY+=10

    
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.display.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit(0)
           
    
    clock.tick()
    #print(clock.get_fps())
    pygame.time.delay(20)

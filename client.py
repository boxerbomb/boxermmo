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
    (128,128,128)
    ]
"""
players(1-5)
wall

"""
reqX=0
reqY=0
newMap = [[0 for x in range(8)] for x in range(8)]


            
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

gridX=1
gridY=1
move_tick=3
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    if gridX>=(reqX+8)-2:
        if reqX<=16:
            gridX=gridX-1
            reqX=reqX+1
            print("id:",idnum)
            s.send("req,"+str(reqX)+","+str(reqY)+","+str(idnum),0)
    
    s.send('mov,'+str(gridX)+','+str(gridY)+','+str(idnum)) 
    data = s.recv(size) 
    s.close()
    data=pickle.loads(data)
    newMap=data
    
    for y in range(0,len(newMap)):
        for x in range(0,len(newMap)):
            if newMap[x][y]==0:
                pygame.draw.rect(screen, (139,69,19), ((x)*50,(y)*50,50,50),0)
            elif newMap[x][y]==5:
                pygame.draw.rect(screen, colors[newMap[x][y]], ((x)*50,(y)*50,50,50),0)
            else:
                pygame.draw.rect(screen, colors[newMap[x][y]], ((x)*50,(y)*50,50,50),0)
    pygame.font.init()
    font=pygame.font.Font(None,30)
    text=font.render("reqX:"+str(reqX)+" reqY:"+str(reqY),1,(255,255,255))
    screen.blit(text,(0,0))
        
    pygame.display.update()
    keys=pygame.key.get_pressed()
    move_tick=move_tick-1
    if keys[K_LEFT]:
        if move_tick==0:
            gridX-=1
            move_tick=3
        
    if keys[K_RIGHT]:
        if move_tick==0:
            gridX+=1
            move_tick=3

    if keys[K_UP]:
        if move_tick==0:
            gridY-=1
            move_tick=3

    if keys[K_DOWN]:
        if move_tick==0:
            gridY+=1
            move_tick=3
    if move_tick<0:
        move_tick=3

    
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

#!/usr/bin/env python 

""" 
A simple echo client 
""" 

import socket, pickle,pygame,os,sys,random,eztext
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
newReq=False

mapsize=24
newMap = [[0 for x in range(8)] for x in range(8)]


            
size = width, height = 600, 500
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

txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='>',x=0,y=400)
#false
txtOn=0

while True:

    if gridX>=(reqX+8)-2:
        if reqX+8<=mapsize-2:
            gridX=gridX-1
            reqX=reqX+1
            newReq=True
    if gridX<=(reqX)+2:
        if reqX>=1:
            gridX=gridX+1
            reqX=reqX-1
            newReq=True
    if gridY>=(reqY+8)-2:
        if reqY+8<=mapsize-2:
            gridY=gridY-1
            reqY=reqY+1
            newReq=True
    if gridY<=(reqY)+2:
        if reqY>=1:
            gridY=gridY+1
            reqY=reqY-1
            newReq=True
            
    if newReq==True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        print("id:",idnum)
        s.send("req,"+str(reqX)+","+str(reqY)+","+str(idnum))
        s.close()
        newReq=False
            

            
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
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

    if txtOn==1:
        pygame.draw.rect(screen,(255,255,255),(0,400,400,100))
        events=pygame.event.get()
        result=txtbx.update(events)
        txtbx.draw(screen)
        if result!=None:
            text=result
            result=0
            print(text)
            txtOn=0
            pygame.draw.rect(screen,(255,255,255),(0,400,400,100))
        
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
            if event.key == K_RETURN:
                txtOn=1
            if event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit(0)
           
    
    clock.tick(30)

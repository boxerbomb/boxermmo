#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket,pickle,random
from multiprocessing import Process
fullMap = [[0 for x in range(24)] for x in range(24)]
sendMap = [[0 for x in range(8)] for x in range(8)]
for y in range(0,24):
    for x in range(0,24):
        if x==0 or x==24 or y==0 or y==24:
            fullMap[x][y]=5
print(sendMap)
#[client,x,y,startx,starty]
players=[]

host = '' 
port = 50000 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)
row=0
parse=[]

startx=0
starty=0
while 1:       
    client, address = s.accept() 
    data = client.recv(size)
    parse=data.split(",")
    
    if parse[0]=="hello":
        print("New Player")
        players.append([client,random.randint(1,8),random.randint(1,8),0,0])
        client.send(str(len(players)))
        print(str(len(players)))

    
    if parse[0]=="mov":
        row=int(parse[3])-1
        fullMap[players[row][1]][players[row][2]]=0
        players[row][1]=int(parse[1])
        players[row][2]=int(parse[2])
        fullMap[players[row][1]][players[row][2]]=row+1

        for y in range(players[row][4],players[row][4]+8):
            for x in range(players[row][3],players[row][3]+8):
                sendMap[x-players[row][3]][y-players[row][4]]=fullMap[x][y]
        
    if parse[0]=="req":
        print("REQD")
        startx=int(parse[1])
        starty=int(parse[2])
        print(parse)
        row=int(parse[3])-1
        players[row][3]=startx
        players[row][4]=starty
        print(startx,startx+8)
        
    if data:
        senddata=pickle.dumps(sendMap)
        client.send(senddata) 
    client.close()


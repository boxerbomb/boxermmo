#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket,pickle,random
from multiprocessing import Process
Map = [[0 for x in range(9)] for x in range(9)]
#[client,x,y]
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
while 1:       
    client, address = s.accept() 
    data = client.recv(size)
    parse=data.split(",")
    
    if parse[0]=="hello":
        print("New Player")
        players.append([client,random.randint(1,8),random.randint(1,8)])
        client.send(str(len(players)-1))
        print(str(len(players)-1))

    
    if parse[0]=="mov":

        row=int(parse[3])
        
        Map[players[row][1]][players[row][2]]=0
        players[row][1]=int(parse[1])
        players[row][2]=int(parse[2])
        Map[players[row][1]][players[row][2]]=1
    if data:
        senddata=pickle.dumps(Map)
        client.send(senddata) 
    client.close()


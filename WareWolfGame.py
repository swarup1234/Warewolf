#!/usr/bin/env python
# coding: utf-8

# # ware wolf the game 

# In[6]:


# Initializing required libraries 
import sys, pygame, os
from random import choice, randint, sample
import numpy as np
from math import floor,ceil

# Getting the location of the images
if os.path.exists("./images"):
    os.chdir("./images")

# Determing the classes for each 

# god mafia class
class GODMAFIA(object):
    def __init__(self,playername,image):
        self.playername = playername
        self.alive = True
        self.MAFIA = False
        self.POLICE = False
        self.DOCTOR = False
        self.votedout = False
        self.votes = 0
        self.lastplayedround = 0
        self.kills = []
        self.voteoutplayer = ''
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.playerrect = self.image.get_rect()
    
    def outplayer(self,player):
        player.alive = False
        self.kills.append(player.playername)
    
    # votingout a player
    def voteoutplayers(self,player):
        self.voteoutplayer = player.playername
        player.votes+=1

# Mafia class
class MAFIA(object):
    def __init__(self,playername,image):
        self.playername = playername
        self.alive = True
        self.MAFIA = True
        self.POLICE = False
        self.DOCTOR = False
        self.votedout = False
        self.votes = 0
        self.lastplayedround = 0
        self.DOCTORHEALED = False
        self.kills = []
        self.voteoutplayer = ''
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.playerrect = self.image.get_rect()
    
    def outplayer(self,player):
        player.alive = False
        self.kills.append(player.playername)
    
    # votingout a player
    def voteoutplayers(self,player):
        self.voteoutplayer = str(player.playername)
        player.votes+=1
        
# Police class
class POLICE(object):
    def __init__(self,playername,image):
        self.playername = playername
        self.alive = True
        self.MAFIA = False
        self.POLICE = True
        self.DOCTOR = False
        self.votedout = False
        self.votes = 0
        self.lastplayedround = 0
        self.detections = []
        self.DOCTORHEALED = False
        self.voteoutplayer = ''
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.playerrect = self.image.get_rect()
    
    def detectplayer(self,player):
        if player.MAFIA == True:
            self.detections.append([(player.playername,1)])
            return(1)
        else:
            self.detections.append([(player.playername,0)])
            return(0)
    
    # votingout a player
    def voteoutplayers(self,player):
        self.voteoutplayer = player.playername
        player.votes+=1
        

# doctor class
class DOCTOR(object):
    def __init__(self,playername,image):
        self.playername = playername
        self.alive = True
        self.MAFIA = False
        self.POLICE = False
        self.DOCTOR = True
        self.votedout = False
        self.votes = 0
        self.lastplayedround = 0
        self.DOCTORHEALED = False
        self.heals = []
        self.voteoutplayer = ''
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.playerrect = self.image.get_rect()
        
    def healplayer(self,player):
        player.DOCTORHEALED = True
        player.alive = True
        self.heals.append(player.playername)
    
    # votingout a player
    def voteoutplayers(self,player):
        self.voteoutplayer = player.playername
        player.votes+=1
             
# Citizen class
class CITIZEN(object):
    def __init__(self,playername,image):
        self.playername = playername
        self.alive = True
        self.MAFIA = False
        self.POLICE = False
        self.DOCTOR = False
        self.votedout = False
        self.votes = 0
        self.lastplayedround = 0
        self.DOCTORHEALED = False
        self.voteoutplayer = ''
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.playerrect = self.image.get_rect()
    
    # votingout a player
    def voteoutplayers(self,player):
        self.voteoutplayer = player.playername
        player.votes+=1
        

# Creating the supporting functions:

# getting a list of alive players at the begining of the round 
def aliveplayers(lst):
    aliveplayers = []
    outplayers = []
    for l in lst:
        l.voteoutplayer = ''
        l.DOCTORHEALED = False
        if l.alive == True:
            aliveplayers.append(l)
        else:
            outplayers.append(l)
    return({"aliveplayers": aliveplayers, "outplayers": outplayers})

# removing the heals for all the players in the begining of the round
def healremove(lst):
    for l in lst:
        l.DOCTORHEALED = False
         
# voteoutlogic, max votes or this round out person or random choice
def voteoutplayerfinal(roundnumber,lst,outplayers):
    maxvotes = 0 
    smallest = max([x.votes for x in lst])
    outplayer = [l for l in lst if smallest == l.votes]
    if len(outplayer)>1 and len(outplayers)>0:        
        op = [l1 for l1 in outplayers if l1.lastplayedround==roundnumber]
        if len(op)>0:
            # Voting a person
            savename = []
            mouse_position = [0,0]
                
            # Highlighting the person voting
            pygame.draw.rect(screen, (255,0,255), op[0].playerrect,5)
            pygame.display.update()

            # Chosing the person to eliminate
            while len(savename)==0:            
                # Getting the events names 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        savename = [1]
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouse_position = pygame.mouse.get_pos()

                # Getting the player selected
                for plyer in aliveplayerlist:
                    if plyer.playerrect.collidepoint(mouse_position):
                        savename.append(plyer.playername)
                        outperson = plyer
                        pygame.draw.rect(screen, (255,0,0), op[0].playerrect,5)
                        pygame.display.update() 
            
            # Actually voting out that person
            op[0].voteoutplayers(outperson)
            smallest = max([x.votes for x in lst])
            outplayer = [l for l in lst if smallest == l.votes]
            outplayer = outplayer[0]
        else:
            outplayer = choice(outplayer)
    else:
        outplayer = choice(outplayer)
    
    outplayer.votedout = True
    outplayer.alive = False
    return(outplayer)
        

list_val = sample([GODMAFIA(playername = "PLAYER1", image = choice(os.listdir())),
                   MAFIA(playername = "PLAYER2", image = choice(os.listdir())),
                   MAFIA(playername = "PLAYER3",image = choice(os.listdir())),
                   DOCTOR(playername = "PLAYER4",image = choice(os.listdir())),
                   POLICE(playername = "PLAYER5",image = choice(os.listdir())),
                   CITIZEN(playername = "PLAYER6",image = choice(os.listdir())),
                   POLICE(playername = "PLAYER7",image = choice(os.listdir())),
                   CITIZEN(playername = "PLAYER9",image = choice(os.listdir()))],8)

gameround = 0
citycount =  100
roundstats = []
mafiacount = 100

# Having the parameters
global width 
global height
size = width, height =1000,1000
global screen_colour 
screen_colour = 0, 255, 0
global RedHeight
RedHeight = height//4

# Setting basic controls
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stopped = False

# Initializing the game 
pygame.init()

# Defining font sizes
global headfont
global fontval
headfont = pygame.font.SysFont("comicsans",40)
fontval = pygame.font.SysFont("comicsans",30)

# Getting the game font
text = headfont.render("Ware-wolf 1.0 Version", 1, (0,0,0))
game_message = "Start the Game ?"
mouse_position = (0,0)

# This is the game message 
def game_message_display(game_message,headfont,width=1000):
    text_message = headfont.render(game_message, 1, (0,0,0))
    x_val =  width//2-(text_message.get_width()//2)
    y_val =  (height*2)//3 - (text_message.get_height()//2)
    #pygame.draw.rect(screen, (120,0,0),(x_val-2, y_val-2,text_message.get_width()+2,text_message.get_height()+2))
    pygame.draw.rect(screen, (225,0,0),(0, y_val-2,width,text_message.get_height()+2))
    screen.blit(text_message, (x_val,y_val))
    
# Updating the screen when required
def ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message):
            # Filling the screen
            screen.fill(screen_colour)
            screen.fill((225,0,225),(0,0,width,RedHeight))

            # Printing the heading
            x_val =  width//2-(text.get_width()//2)
            y_val =  RedHeight+(text.get_height())-20
            pygame.draw.rect(screen, (255,0,0),(x_val-2, y_val-2,text.get_width()+2,text.get_height()+2),4)
            screen.blit(text, (x_val,y_val))

            # Printing the message at the center of the screen 
            game_message_display(game_message,headfont,width)

            # Finalising the locations of the Alive players
            nplayer = len(aliveplayerlist)
            balwidth = 150
            x = np.linspace(0+balwidth, width-balwidth, ceil(nplayer/2))
            y = np.linspace(RedHeight+balwidth,height-balwidth,2)
            alive_corners = [(x1,y1) for y1 in y for x1 in x]

            # Replacing the players rectangles
            i=0
            for player in aliveplayerlist:
                player.playerrect = player.playerrect.move(alive_corners[i][0]-player.playerrect.center[0],                                                       alive_corners[i][1]-player.playerrect.center[1])
                i+=1

            # Finalising the locations of the out players
            nplayer = len(outplayerlist)
            balwidth = 150
            x = np.linspace(0+balwidth, width-balwidth, ceil(nplayer))
            y = np.linspace(RedHeight//2,RedHeight//2,1)
            out_corners = [(x1,y1) for y1 in y for x1 in x]
            #print(out_corners)

            # Replacing the players rectangles
            i=0
            for player in outplayerlist:
                player.playerrect = player.playerrect.move(out_corners[i][0]-player.playerrect.center[0],                                                       out_corners[i][1]-player.playerrect.center[1])
                i+=1

            # Displaying each player
            for player in list_val:
                # Drawing the player and the background
                screen.blit(player.image, player.playerrect)
                pygame.draw.rect(screen, (255,0,0), player.playerrect,5)

                # Printing the players names
                Playertext = fontval.render(player.playername, 1, (0,0,255))
                xval = player.playerrect.right-player.playerrect.width//2-(Playertext.get_width()//2)
                yval = player.playerrect.bottom + 5
                #yval = player.playerrect.bottom+(Playertext.get_height())
                #textrect = pygame.Rect((xval,yval,Playertext.get_width(),Playertext.get_height()))

                # Printing the class name
                PlayerClass = fontval.render(type(player).__name__, 1, (0,0,255))
                xval1 = xval 
                yval1 = player.playerrect.top - PlayerClass.get_height() - 2

                # Printing the number of votes
                PlayerVotes = fontval.render("Votes: "+str(player.votes), 1, (0,0,255))
                xval2 = xval 
                yval2 = yval +  PlayerVotes.get_height()
                #textrect2 = pygame.Rect((xval1,yval1,PlayerClass.get_width(),PlayerClass.get_height()))

                screen.blit(Playertext, (xval,yval))
                screen.blit(PlayerClass, (xval1,yval1))
                screen.blit(PlayerVotes, (xval2,yval2))
                pygame.display.update()
            


# In[7]:


while not stopped:
    # Closing the game when we quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            stopped = True
            mafiacount = 200 
            pygame.quit()
    while citycount >0 and mafiacount!=0:
        clock.tick(10)
        # This goes inside the while
        gameround+= 1
        mafia = []
        police = []
        doctor = []

        # Closing the game when we quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                stopped = True
                mafiacount = 200 

        # Alive players/ outplayers
        val = aliveplayers(list_val)
        aliveplayerlist = val['aliveplayers']
        outplayerlist = val['outplayers']
        
        # Equating all the votes to zero 
        for pl in aliveplayerlist:
            pl.votes = 0
        
        # updating the screen
        ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message = "Round Number: "+str(gameround))
        
        # while mafia is lesser than the citzen
        mafiacount = len([x for x in aliveplayerlist if 'MAFIA' in type(x).__name__ ])
        citycount = len([x for x in aliveplayerlist if 'MAFIA' not in type(x).__name__ ])-len([x for x in aliveplayerlist if 'MAFIA' in type(x).__name__ ])
        message1 = ("There are " + str(citycount) +" more than mafia." + " mafia count: " + str(mafiacount))
        
        #pygame.time.wait(1000)
        # Printing the message at the center of the screen 
        game_message_display(message1,headfont,width)
        pygame.display.update()
        pygame.time.wait(1000)
        
        print("\n City Sleeps:  ")
        
        #pygame.time.wait(1000)
        # Printing the message at the center of the screen 
        game_message_display("City Sleeps",headfont,width)
        pygame.display.update()
        pygame.time.wait(1000)


        print("MAFIA WAKE UP")
        #pygame.time.wait(1000)
        # Printing the message at the center of the screen 
        game_message_display("MAFIA WAKE UP",headfont,width)
        pygame.display.update()
        pygame.time.wait(1000)
        
        # Mafia wake up: 
        eliminate = []
        eliminatename = []
        mouse_position = [0,0]
        # Highlighting Mafia list
        Mafialist = [x for x in aliveplayerlist if 'MAFIA' in type(x).__name__ ]
        for plyer in Mafialist:
            pygame.draw.rect(screen, (255,0,255), plyer.playerrect,5)
        pygame.display.update()
        
        # Chosing the person to eliminate
        while len(eliminatename)==0:            
            # Getting the events names 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    eliminatename = [1]
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    
            # Getting the player selected
            selectionlist = [x for x in aliveplayerlist if 'MAFIA' not in type(x).__name__ ]
            for plyer in selectionlist:
                if plyer.playerrect.collidepoint(mouse_position):
                    eliminatename.append(plyer.playername)
                    eliminate = plyer
                    for plyer1 in Mafialist:
                        pygame.draw.rect(screen, (255,0,0), plyer1.playerrect,5)
                    pygame.display.update()        
        
        
        #eliminate = sample([x for x in aliveplayerlist if 'MAFIA' not in type(x).__name__ ],1)
        eliminate.alive = False
        mafiaout = ("This person is ousted by Mafia "+ str(eliminate.playername))
        print(mafiaout)
        
        #pygame.time.wait(1000)
        # Printing the message at the center of the screen 
        game_message_display(mafiaout,headfont,width)
        pygame.display.update()
        pygame.time.wait(1000)
        

        # The actual game and updates 
        for l in aliveplayerlist:
            if "MAFIA" in type(l).__name__ :
                #print("Updating the mafia kills a person")
                l.kills.append(eliminate.playername)
            elif "DOCTOR" in type(l).__name__ :
                print("DOCTOR WAKE UP \n")
                #pygame.time.wait(1000)
                # Printing the message at the center of the screen 
                game_message_display("DOCTOR WAKE UP",headfont,width)
                pygame.display.update()
                pygame.time.wait(1000)
                
                # Doctor saves a person
                savename = []
                mouse_position = [0,0]
                
                # Highlighting Doctor
                pygame.draw.rect(screen, (255,0,255), l.playerrect,5)
                pygame.display.update()

                # Chosing the person to eliminate
                while len(savename)==0:            
                    # Getting the events names 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            savename = [1]
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            mouse_position = pygame.mouse.get_pos()

                    # Getting the player selected
                    for plyer in aliveplayerlist:
                        if plyer.playerrect.collidepoint(mouse_position):
                            savename.append(plyer.playername)
                            doc = plyer
                            pygame.draw.rect(screen, (255,0,0), l.playerrect,5)
                            pygame.display.update()  
                
                #doc = sample(aliveplayerlist,1)[0]
                doctorsave = ("Doctor saved person "+ str(doc.playername))
                print(doctorsave)
                
                #pygame.time.wait(1000)
                # Printing the message at the center of the screen 
                game_message_display(doctorsave,headfont,width)
                pygame.display.update()
                pygame.time.wait(1000)
                
                # healing the person
                l.healplayer(doc)
            elif "POLICE" in type(l).__name__ :
                print("POLICE WAKE UP \n")
                #pygame.time.wait(1000)
                # Printing the message at the center of the screen 
                game_message_display("POLICE WAKE UP",headfont,width)
                pygame.display.update()
                pygame.time.wait(1000)
                
                # Police detects a person
                savename = []
                mouse_position = [0,0]
                
                # Highlighting Police
                pygame.draw.rect(screen, (255,0,255), l.playerrect,5)
                pygame.display.update()

                # Chosing the person to eliminate
                while len(savename)==0:            
                    # Getting the events names 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            savename = [1]
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            mouse_position = pygame.mouse.get_pos()

                    # Getting the player selected
                    for plyer in aliveplayerlist:
                        if plyer.playerrect.collidepoint(mouse_position):
                            savename.append(plyer.playername)
                            pol = plyer
                            pygame.draw.rect(screen, (255,0,0), l.playerrect,5)
                            pygame.display.update() 
                
                # Saving the persopn
                #pol = sample([x for x in aliveplayerlist],1)[0]       
                val = l.detectplayer(pol)
                PoliceDetect = ("Police detects person: " + str(pol.playername) + " and is "+ str(val))
                print(PoliceDetect)
                
                #pygame.time.wait(1000)
                # Printing the message at the center of the screen 
                game_message_display(PoliceDetect,headfont,width)
                pygame.display.update()
                pygame.time.wait(1000)     

        print("\n City wakeup:  ")
        #pygame.time.wait(1000)
        # Printing the message at the center of the screen 
        game_message_display("CITY WAKES UP!",headfont,width)
        pygame.display.update()
        pygame.time.wait(1000)
        
        
        # The city gets up to get the results 
        if eliminate.alive:
            print("No one is dead")
            #pygame.time.wait(1000)
            # Printing the message at the center of the screen 
            game_message_display("No one is dead!",headfont,width)
            pygame.display.update()
            pygame.time.wait(1000)
            
            # updating the screen
            ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message = "City Votes")
        else:
            outplayerprint = ("Player "+str(eliminate.playername)+" is dead")
            print(outplayerprint)
            #pygame.time.wait(1000)
            # Printing the message at the center of the screen 
            game_message_display(outplayerprint,headfont,width)
            pygame.display.update()
            pygame.time.wait(1000)
            
            # Recalculating the list of alive players
            val = aliveplayers(list_val)
            aliveplayerlist = val['aliveplayers']
            outplayerlist = val['outplayers']
            
            # updating the screen
            ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message = "City Votes")

        print("\n City Vote:  ")
        # Voting out a player
        for l in sample(aliveplayerlist,len(aliveplayerlist)):
            
            outplayerprint = "Player "+str(l.playername)+" to vote please select a person to vote"
            
            # Printing the message at the center of the screen 
            game_message_display(outplayerprint,headfont,width)
            pygame.display.update()
            pygame.time.wait(1000)
            
            # Voting a person
            savename = []
            mouse_position = [0,0]
                
            # Highlighting the person voting
            pygame.draw.rect(screen, (255,0,255), l.playerrect,5)
            pygame.display.update()

            # Chosing the person to eliminate
            while len(savename)==0:            
                # Getting the events names 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        savename = [1]
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouse_position = pygame.mouse.get_pos()

                # Getting the player selected
                for plyer in aliveplayerlist:
                    if plyer.playerrect.collidepoint(mouse_position):
                        savename.append(plyer.playername)
                        outperson = plyer
                        pygame.draw.rect(screen, (255,0,0), l.playerrect,5)
                        pygame.display.update() 
            
            #outperson = choice(aliveplayerlist)
            person_outchoice = (str(l.playername) + " voted against " + str(outperson.playername))
            l.voteoutplayers(outperson)
            print(person_outchoice)
            
            # updating the screen
            ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message = person_outchoice)

        print("\n Final Voting Stats: ")
        # Getting the list of votes
        for l in aliveplayerlist:
            print(str(l.playername) + " has "+ str(l.votes) + " against him/her")

        # voting results
        vo = voteoutplayerfinal(gameround,aliveplayerlist,outplayerlist)
        
        # while mafia is lesser than the citzen
        mafiacount = len([x for x in aliveplayerlist if 'MAFIA' in type(x).__name__ ])
        citycount = len([x for x in aliveplayerlist if 'MAFIA' not in type(x).__name__ ])-len([x for x in aliveplayerlist if 'MAFIA' in type(x).__name__ ])

        # updating the screen
        ScreenUpdate(list_val,aliveplayerlist,outplayerlist,game_message = "Total Mafia left = "+str(mafiacount))
        
        # Game Stats
        roundstats.append({"roundNumber": gameround, "Mafiakilled":eliminate.playername, "alive":[x.playername for x in aliveplayerlist], "OutofGame": [x.playername for x in outplayerlist], "votedout":vo.playername})
        
        # Updating the display and setting the frame rate at 10 frames per second.
        pygame.display.update()
        #clock.tick(10)
        
    game_message_display("GAME-OVER",headfont,width)
    pygame.display.update()
    
pygame.quit()


from __future__ import division
import sys
import pygame
import time
import glob

from random import randrange, choice
from math import sqrt,pi,sin,cos,atan
from collections import Counter
from Queue import Queue
from operator import attrgetter

# colour globals
LAV = (100,100,200)
PEA = (100,200,100)
CORAL = (200,100,100)

AQUA = (100,200,200)
ROSE = (200,100,200)
SUN = (200,200,100)

GOOSE = (100,100,100)
CHALK = (200,200,200)

POND = (1,70,54)

c_list_win = [(255,235,225),(225,255,235),(225,235,255)]
c_list = [(0,0,0),(200,200,200)]
c_list1 = [(200,55,35),(35,200,55),(35,55,200),(225,170,150),(150,225,170),(150,170,225)]
c_list2 = [(240,80,55),(255,255,255),(55,80,220)]

factor = 1

class Vertex(object):
    def __init__(self,(x,y)):
        self.xy = (x,y)
        self.win = "-"
        self.parent = 0
        self.child = 0
        self.bp = 0
        self.size = int(9*factor)
        self.counter = 1
        
class PgmeMain(object):
    def __init__(self):

        pygame.init()
        self.width = int(1920*factor)
        self.height = int(1200*factor)
        self.screen = pygame.display.set_mode((self.width, self.height))
    
        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        
        
        #program variables
        #fonts
        fontfile = pygame.font.match_font('helvetica')
        self.control_font = pygame.font.Font(fontfile,20)
        self.msg_font = pygame.font.Font(fontfile,30)
        
        self.colour_msg1 = self.control_font.render("X wins",True, c_list1[2])
        self.colour_msg2 = self.control_font.render("Draw",True, c_list1[1])
        self.colour_msg3 = self.control_font.render("O wins",True, c_list1[0])
        
        
        #State switch: Used to communicate board state to user 
        # 0 for normal; 1 to save, 2 for load screen,
        # 3 for load msg, 4 for force embed
        self.state = 0 
        self.timer = 0
       
        #vertex and edge variables 
        #vertex list 
        self.v_list1 = []
         
        #adjacency list. 
        # First list index corresponds to the vertex at the 
        # same index in the vertex list    
        self.a_list1 = []
        
        self.symbol = []
        self.win = []
        self.row_count = Counter()
        #self.levs = Counter()
        self.levs = [[],[],[],[],[],[],[],[],[],[]]
        #after variable initialization, run the main program loop
        self.event_loop()



    #Methods assisiting with program function
    #
    #
    #returns a list with the number of vertices and edges in g1 and in g2
    # in this order: [v_g1,e_g1,v_g2,e_g2]
    def count_v_and_e(self):
        v1 = len(self.v_list1)
        e1 = len(reduce(lambda x,y: x + y, self.a_list1,[]))
      
        
        return [v1,e1]

    def v_list_coordinates(self,v_list):
        return [i.xy for i in v_list]

    #save the v_list indexes of connected vertices
    def v_list_index(self, v_list, a_list):
        a_list_ind = []
        
        for i in range(len(a_list)):
            a_list_ind.append([])
            for j in a_list[i]:
                a_list_ind[i].append(v_list.index(j))
        return a_list_ind 
 
    def a_list_coordinates(self,a_list):
        a_cord = []
        for i in range(len(a_list)):
            a_cord.append([])
            for j in a_list(i):
                a_cord[i].append(j.xy)
        return a_cord


    def load_data(self,select_file):
        f=open(select_file,"r")
        f1=f.readline()
        self.v_list1 = []
        self.a_list1 = []
  
        #parse the lines and generate v and a lists
        f2 = f.readline() # self.v_list1
        if f2 != '[]\n':
            f2 = f2.rstrip(')]\n')
            f2 = f2.lstrip('[(')
            f2 = f2.split('), (')
            for i in f2:
                if i is not '':
                    j = i.split(', ')
                    if j[0] is not '' and j[1] is not '':
                        self.v_list1.append(Vertex((int(j[0]),int(j[1]))))
        
        
        f3 = f.readline() #self.a_list1
        if f3 != '[]\n':
            f3 = f3.rstrip(']]\n')
            f3 = f3.lstrip('[[')
            f3 = f3.split('], [')
            for i in range(len(f3)):
                self.a_list1.append([])
                l = f3[i].split(', ')
                for j in l:
                    if j is not '':
                        self.a_list1[i].append(self.v_list1[int(j)])
    
   
        f4 = f.readline()

        self.zoom_list=0  
        self.timer = time.time()
        self.state = 3
        
        
        #code specific to tictactoe files
        if len(self.v_list1) == 765:
            f = open('tictactoe.txt')
            symbol = []
            for i in range(765):
                a = f.readline()
                a = a.rstrip('\r\n')
                self.symbol.append(a)
                
                u = self.v_list1[i]
                
                # append parents to adjacentcy list
                for v in self.a_list1[i]:
                    j = self.v_list1.index(v)
                    u.child += 1                    
                    if u not in self.a_list1[j]:
                        self.a_list1[j].append(u)
                        v.parent += 1      

            
            self.win_loose_draw()
            self.minimax(self.v_list1[0], True)           
            self.reorder()
            
    # Main Event handling method      
    def event_loop(self):
         while True:
          
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                sys.exit()
          
            elif event.type == pygame.MOUSEMOTION:
                pos = event.pos
                for i in range(len(self.v_list1)):
                    u = self.v_list1[i]
                    
                    if (u.xy[0]-pos[0])**2 + (u.xy[1]-pos[1])**2 < 9:
                        print "========"
                        print self.symbol[i][0:3]    
                        print self.symbol[i][3:6]
                        print self.symbol[i][6:9]   
                        print "========"
        
                 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
             
                    self.v_list1 = []
                    self.a_list1 = []
                    self.zoom_list=0
         

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                tm = time.localtime(time.time())
                self.timer = time.time()
                
                filename = str(tm.tm_year) + "_" + str(tm.tm_mon) + "_" + \
                                    str(tm.tm_mday) + "_" + str(tm.tm_hour) + \
                                    str(tm.tm_min) + str(tm.tm_sec)+".graph"

                f = open(filename,"w")
                f.write(str(self.count_v_and_e()) + "\n")
                f.write(str(self.v_list_coordinates(self.v_list1)) + "\n")
                f.write(str(self.v_list_index(self.v_list1,self.a_list1)) + "\n")

                f.close()
                self.state = 1

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                #glob to read files into self.load_list
                        #determine number of files, can display 20 per page
                self.state = 2
                self.load_data("tictactoe1.graph")
                #self.load_list = glob.glob("*.graph")
              
            elif event.type == self.REFRESH:
            
                # Draw the interface 
                
                self.draw()
  
                    
            else:
                pass
 
    def deg(self,v):
        return len(self.a_list1[self.v_list1.index(v)])
   

    def win_loose_draw(self):
        #win:
        for i in self.symbol:
        
         
            if i[0:3] == "XXX" or i[3:6] == "XXX" or i[6:9] == "XXX":
                self.win.append("x")
            elif i[0:3] == "OOO" or i[3:6] == "OOO" or i[6:9] == "OOO":     
                self.win.append("o")
           
            elif i[0] == "X" and i[3] == "X" and i[6] == "X":
                    self.win.append("x")
            elif i[0] == "X" and i[4] == "X" and i[8] == "X":
                    self.win.append("x")     
            elif i[2] == "X" and  i[5] == "X" and i[8] == "X":
                    self.win.append("x")
            elif i[2] == "X" and i[4] == "X" and i[6] == "X":
                    self.win.append("x")
            elif i[1] == "X" and i[4] == "X" and i[7] == "X":
                self.win.append("x")
            

            elif i[0] == "O" and i[3] == "O" and i[6] == "O":
                    self.win.append("o")
            elif i[0] == "O" and i[4] == "O" and i[8] == "O":
                    self.win.append("o") 
            elif i[2] == "O" and i[5] == "O" and i[8] == "O":
                    self.win.append("o")
            elif i[2] == "O" and i[4] == "O" and i[6] == "O":
                    self.win.append("o")
            elif i[1] == "O" and i[4] == "O" and i[7] == "O":
                self.win.append("o")                
          
            else:
            
                if "-" not in i:
                    self.win.append("d")
                else:
                    self.win.append("")

     
    def moves(self,vertex):
        index = self.v_list1.index(vertex)
        board = self.symbol[index]
        
        c=Counter()
        for j in board:
            c[j]+=1
        return c['-']
        
        
    #node is V in v_list, start with player X
     
    def minimax(self, node, player):
        index = self.v_list1.index(node)
        if self.win[index] == "x":
            node.win = 1
            return 1
        elif self.win[index] == "o":
            node.win = -1
            return -1
        elif self.win[index] == "d":  
            node.win = 0
            return 0
        else:    
            if player:
                bestvalue = -1
                for i in self.a_list1[index]:
                    if self.moves(i) < self.moves(node):
                        val = self.minimax(i, False)
                        bestvalue = max(bestvalue, val)
                        node.win = bestvalue
                        
            else:
                bestvalue = 1
                for i in self.a_list1[index]:
                    if self.moves(i) < self.moves(node):
                        val = self.minimax(i, True)
                        bestvalue = min(bestvalue, val)
                        node.win = bestvalue
                        
            return bestvalue     
            
                
            
    def reorder(self):
        #some stats
        wins = Counter() #how many ways for each player to win
        fatal = Counter() #how many fatal mistakes each player can make
        
        for m in reversed(range(10)):
            levelm = [v for v in self.v_list1 if self.moves(v) == m]
                 
            for winner in [-1, 0, 1]:
                levelmi = [v for v in levelm if v.win == winner]
                
                if winner == (-1+(m % 2)) or winner == (0+(m %2)):
                    self.row_count[m] +=len(levelmi)
                    self.levs[m] += levelmi
                
                for v in levelmi:
                    i = self.v_list1.index(v) # Ack!
                    parents = [w for w in self.a_list1[i] 
                                if self.moves(w) > self.moves(v) 
                                 and w.win == v.win]
                    v.bp = len([w for w in self.a_list1[i]
                                if self.moves(w) > self.moves(v) and w.win != v.win])
                                
                    children = [w for w in self.a_list1[i] if self.moves(w) < self.moves(v)
                                    and w.win == v.win]             
                    bad_children = [w for w in self.a_list1[i] if self.moves(w) < self.moves(v) 
                                and w.win != 0 and w.win != v.win ]
                    
                    fatal[self.moves(v)%2] += len(bad_children)
                    
                    if parents:
                        
                        v.sortkey = sum([w.xy[0] for w in parents])/len(parents)
                        
                        if not children:
                            v.sortkey = v.sortkey + -v.win*(2**20)
                   
                            wins[v.win]+=1   
                            
                    else:
                        if winner == 0:
 
                           if self.moves(v) % 2 == 0:
                                v.sortkey = 2**20
                           else:
                                v.sortkey = -2**20
                        else:
                            v.sortkey = -v.win * 2**20
                        #    v.sortkey = -v.win * (len(children)+1)**20
                           
                                                        
                            
    
                            
                # Bad - Omega(n^2log n) time algorithm in here.
                # levelmi = sorted(levelmi, key=lambda v: \
                #        -len(self.a_list1[self.v_list1.index(v)])*winner)
                levelmi = sorted(levelmi, key=lambda v: v.sortkey)
                
                #self.lev_list[winner+1].append(levelmi)      
                
                
                xblock = (winner+1)*self.width/3 \
                        + (self.width/3)/(len(levelmi)+1)

                for v in levelmi:

                    v.xy = int(xblock), int(self.height*(10-m)/11)
                    xblock += (self.width/3)/(len(levelmi)+1)
                    v.sortkey = v.xy[0]
                
        print "player wins", wins
        print "fatal moves 1=X, 0=O", fatal  
        
        
        
        
        
        
        
        
        
        for m in range(10):
            levelm = [v for v in self.v_list1 if self.moves(v) == m]
                 
            for winner in [-1, 0, 1]:
                levelmi = [v for v in levelm if v.win == winner]
        
                for v in levelmi:
                     i = self.v_list1.index(v) # Ack!
          
                     children = [w for w in self.a_list1[i] if self.moves(w) < self.moves(v)
                                    and w.win == v.win]
                     
                     if children:
                        
                        v.sortkey += sum([w.xy[0] for w in children])/len(children)
  
                levelmi = sorted(levelmi, key=lambda v: v.sortkey)
                
                xblock = (winner+1)*self.width/3 \
                        + (self.width/3)/(len(levelmi)+1)

                for v in levelmi:

                    v.xy = int(xblock), int(self.height*(10-m)/11)
                    xblock += (self.width/3)/(len(levelmi)+1)
                    v.sortkey = v.xy[0]
       
       
        for m in reversed(range(10)):
            levelm = [v for v in self.v_list1 if self.moves(v) == m]
                 
            for winner in [-1, 0, 1]:
                levelmi = [v for v in levelm if v.win == winner]
        
                for v in levelmi:
                     i = self.v_list1.index(v) # Ack!
                     parents = [w for w in self.a_list1[i] 
                                if self.moves(w) > self.moves(v) 
                                 and w.win == v.win]
                     children = [w for w in self.a_list1[i] if self.moves(w) < self.moves(v)
                                    and w.win == v.win]
                     if parents:
                        v.sortkey += sum([w.xy[0] for w in parents])/len(parents)
                        if not children:
                            v.sortkey = v.sortkey + -v.win*(2**20)
                     else:
                        if winner == 0:
 
                           if self.moves(v) % 2 == 0:
                                v.sortkey = 2**22
                           else:
                                v.sortkey = -2**22
                        else:
                           v.sortkey += (-v.win * 2**20)
                            #v.sortkey = -v.win * (len(children)+1)**20
                    
                levelmi = sorted(levelmi, key=lambda v: v.sortkey)
    
                xblock = (winner+1)*self.width/3 \
                        + (self.width/3)/(len(levelmi)+1)

                for v in levelmi:

                    v.xy = int(xblock), int(self.height*(10-m)/11)
                    xblock += (self.width/3)/(len(levelmi)+1)
                    v.sortkey = v.xy[0]
    
    
                        
                    if v.win == 1 and 1 < self.moves(v) < 6:
                        v.size = v.size/3
                    elif v.win == -1 and 1 < self.moves(v) < 5:
                        v.size = v.size/3
                    elif 0 < self.moves(v) < 7:
                        v.size = int((v.size+(1*factor))/2)
    
    
    
            
    def draw_board(self):
        #draw the primary and secondary view
        rect_g1 = (0,0,self.width/3,self.height)
        rect_g2 = (self.width/3,0,2*self.width/3,self.height)
        rect_g3 = (2*self.width/3,0,3*self.width/3,self.height)
        
        
        pygame.draw.rect(self.screen,c_list_win[0],rect_g1)
        pygame.draw.rect(self.screen,c_list_win[1],rect_g2)
        pygame.draw.rect(self.screen,c_list_win[2],rect_g3)
        
                   
        rect = self.colour_msg1.get_rect()
        rect = rect.move(20,20)
        self.screen.blit(self.colour_msg3,rect)
        rect = rect.move(self.width/3,0)
        self.screen.blit(self.colour_msg2,rect)
        rect = rect.move(self.width/3,0)
        self.screen.blit(self.colour_msg1,rect)
        
        # draw controls
        #msg1 = "mouse left : add/move vertex  |  mouse right : connect vertex    "
        msg = "|  d : delete   |   s : save to file   |   l: load from file   "

        
        controls = self.control_font.render(msg,True, CHALK)
        rect = controls.get_rect()
        rect = rect.move(10,self.height-30)
        self.screen.blit(controls,rect)




    def draw_vertex(self, v):
        i = self.v_list1.index(v)
        col_dict = {"O":0,"-":1,"X":2}
        
        """
        size = self.size
        
        if v.win == 1 and 1 < self.moves(v) < 6:
            size = self.size/3
        elif v.win == -1 and 1 < self.moves(v) < 5:
            size = int(3*factor)
        elif 0 < self.moves(v) < 7:
            size = int(5*factor)
        """
        
        #draw player moves
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                xy = (v.xy[0] + v.size*x, v.xy[1] + v.size*y)
                col = c_list2[col_dict[self.symbol[i][(x+1)+(y+1)*3]]]
                
                rect = (xy[0], xy[1], v.size, v.size)
                
                pygame.draw.rect(self.screen,col,rect)
                #pygame.draw.rect(self.screen,(0,0,0),rect,1)
        
        #draw the board outline        
        x = v.xy[0]
        y = v.xy[1]
        
        pygame.draw.line(self.screen,(0,0,0),(x,y-v.size),(x,y+2*v.size),1)
        pygame.draw.line(self.screen,(0,0,0),(x+v.size,y-v.size),(x+v.size,y+2*v.size),1)
        pygame.draw.line(self.screen,(0,0,0),(x-v.size,y),(x+2*v.size,y),1)
        pygame.draw.line(self.screen,(0,0,0),(x-v.size,y+v.size),(x+2*v.size,y+v.size),1)
        
    
    def draw_bad_edges(self):
       
       
        for m in reversed(range(10)):
            v_step = int(15*factor)
            if m % 2 ==0:
                
                for v in reversed(sorted(self.levs[m], key= lambda w: w.sortkey)):
                    n = len(self.levs[m])
                    j = self.v_list1.index(v)
                    v_step += min((1/n)*(1/15)*self.height,10)
                    for u in self.a_list1[j]:
                        col = c_list1[u.win+4] 
                        if self.moves(u) < self.moves(v) and u.win != v.win:
                            
                            end_x = (u.xy[0]-u.size)+((u.bp-u.counter+(1/max(1,(u.bp-1))))*u.size)
                            u.counter += 1
                                                               
                            #draw the vertical line down the the desired depth        
                            start_p = (v.xy[0]+int(3*v.size/2),v.xy[1])
                            end_p = (v.xy[0]+int(3*v.size/2), int(v.xy[1] + v_step))
                            pygame.draw.line(self.screen,col,start_p,end_p,int(factor))
                            
                            #draw the horizontal line across to the child vertex
                            start_c = end_p
                            end_c = (end_x,end_p[1])
                            pygame.draw.line(self.screen,col,start_c,end_c,int(factor))
                            
                            #draw the vertical line down to the child vertex
                            start_c = end_c
                            end_c = (end_x,u.xy[1])
                            pygame.draw.line(self.screen,col,start_c,end_c,int(factor))
            
            else:
                for v in sorted(self.levs[m], key= lambda w: w.sortkey):
                    n = len(self.levs[m])
                    j = self.v_list1.index(v)
                    
                    v_step += min((1/n)*(1/15)*self.height,10)
                    for u in self.a_list1[j]:
                        
                        col = c_list1[u.win+4] 
                        if self.moves(u) < self.moves(v) and u.win != v.win:
                            
                            #calculate coordinate for edge connecting with child vertex
                            
                            end_x = (u.xy[0]-u.size)+((u.counter-1+(1/max(1,(u.bp-1))))*u.size)
                            u.counter += 1
                                                            
                            #draw the vertical line down the the desired depth        
                            start_p = (v.xy[0]-int(v.size/2),v.xy[1])
                            end_p = (v.xy[0]-int(v.size/2), int(v.xy[1] + v_step))
                            pygame.draw.line(self.screen,col,start_p,end_p,int(factor))
                            
                            #draw the horizontal line across to the child vertex
                            start_c = end_p
                            end_c = (end_x,end_p[1])
                            pygame.draw.line(self.screen,col,start_c,end_c,int(factor))
                            
                            #draw the vertical line down to the child vertex
                            start_c = end_c
                            end_c = (end_x,u.xy[1])
                            pygame.draw.line(self.screen,col,start_c,end_c,int(factor))


    def draw_graphs(self):
 
        self.draw_bad_edges()
        
        #draw the edges perfect plays
        for i in range(len(self.a_list1)):
             v = self.v_list1[i]
             for u in self.a_list1[i]:
                                              
                if self.v_list1[i].win == u.win:
                                                     
                    if self.moves(u) < self.moves(self.v_list1[i]):
                       #col = c_list2[u.win+1]
                       col = c_list[0] 
                       x = v.xy[0]+(v.size)/2
                       y = v.xy[1]+2*v.size 
                       
                       x_u = u.xy[0]+(u.size)/2 
                       y_u = u.xy[1]-u.size    
                       pygame.draw.line(self.screen,col,(x_u,y_u),(x,y), 1)


        
        #draw the vertices,
        for v in self.v_list1:
                                
            #pygame.draw.circle(self.screen,c_list[0],v.xy,3)
            self.draw_vertex(v)                 
            v.counter = 1


	
    def draw(self):
        self.screen.fill((255,255,255))
        self.draw_board()
       
        self.draw_graphs()        

        pygame.display.flip()




PgmeMain()

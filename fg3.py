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

c_list_win = [(235,235,255),(255,235,235),(235,255,235)]

c_list = [(0,0,0),(200,200,200)]


c_list1 = [(43,140,190),(222,45,38),(49,163,84),(166,189,219),(252,146,114),(173,221,142)]

#c_list2 = [(141,160,203),(252,141,98),(102,194,165)]

#c_list1= [(100,226,240),(80,209,230),(60,189,219),\
#            (40,169,207),(20,144,192),(10,129,138),(5,100,80),(1,70,54)]

class Vertex(object):
    def __init__(self,(x,y)):
        self.xy = (x,y)
        self.win = "-"
        self.locate = False
        self.parent = 0
        self.child = 0
        
        
class PgmeMain(object):
    def __init__(self):

        pygame.init()
        self.width = 1700
        self.height = 1080
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
        lev_list=[[],[],[]]
        
        for m in reversed(range(10)):
            levelm = [v for v in self.v_list1 if self.moves(v) == m]
            
            
            for winner in [-1, 0, 1]:
                levelmi = [v for v in levelm if v.win == winner]
                for v in levelmi:
                    i = self.v_list1.index(v) # Ack!
                    parents = [w for w in self.a_list1[i] 
                                if self.moves(w) > self.moves(v) 
                                 and w.win == v.win]
                    if parents:
                        v.sortkey = sum([w.xy[0] for w in parents])/len(parents)
                    else:
                        # FIXME: Be smarter with draws
                        if winner == 0:
                            lp = len([w for w in self.a_list1[i] 
                                if self.moves(w) > self.moves(v) 
                                 and w.win == -1])
                            rp = len([w for w in self.a_list1[i] 
                                if self.moves(w) > self.moves(v) 
                                 and w.win == 1])
                            if lp > rp:
                                v.sortkey = -2**20
                            elif rp < lp:
                                v.sortkey = 2**20
                            else:
                                v.sortkey = choice([2**20, -2**20])
                        else:
                            v.sortkey = -v.win* 2**20
                # Bad - Omega(n^2log n) time algorithm in here.
                # levelmi = sorted(levelmi, key=lambda v: \
                #        -len(self.a_list1[self.v_list1.index(v)])*winner)
                levelmi = sorted(levelmi, key=lambda v: v.sortkey)
                
                lev_list[winner+1].append(levelmi)      
                xblock = (winner+1)*self.width/3 \
                        + (self.width/3)/(len(levelmi)+1)

                for v in levelmi:
                    v.xy = int(xblock), int(self.height*(10-m)/11)
                    xblock += (self.width/3)/(len(levelmi)+1)
        
        
        """for l in [0,1,2]:
           
            q = Queue()
            current_moves = 9           
            
            
            #for i in reversed(range(10)):
            #    if lev_list[l] != None:
            #        a = max(a,i) 
            #    print "size at ",i," :", len(lev_list[l][i])
                 
            i = 9
            while len(lev_list[l][i]) == 0:
               i -= 1
               print i
            
            for j in range(len(lev_list[l][i])):
            
                print j,len(lev_list[l][i])
                print lev_list[l][i][j].xy
                q.put(lev_list[l][i][j])
            
            
                while q.qsize() > 0:
                    u = q.get()
                    i = self.v_list1.index(u)
                
                    if u.locate == False:   
                        if self.moves(u) < current_moves:
                            current_moves = self.moves(u) 
                            xblock = l*self.width/3
                               
                            
                        xblock +=  ((self.width/3)/ (len(lev_list[l][current_moves])+1))
                        print xblock, 1*self.width/3, current_moves, len(lev_list[l][current_moves])
                        
                        u.xy = (int(xblock),int(self.height*(10-current_moves)/11))
                            
                        u.locate = True
                        
                        
                    for w in self.a_list1[i]:
                        q.put(w)
                        
              
        
        q = Queue()
        q.put(self.v_list1[0])
        
        
        
        xblock = 80
        level = 1/11
        #theta = 0
        
        #set the counters

        c_a=Counter()
      
        for i in range(len(self.v_list1)):
            u = self.v_list1[i]
            c_a[self.moves(u)] += 1
         
            
        for i in range(10):
            print "moves: ", i, "vertices: ", c_a[i]   
            
            
               
        
            
        while q.qsize() > 0:
            
            
            u = q.get()
            i = self.v_list1.index(u)
            
                                 
            new_level = (10-self.moves(u))/11
              
            if u.locate == False: #and u.counter == 0:    

                if new_level > level:
                    level = new_level
                    #theta = 0
                    #xblock = 80
                    xblock = (self.width-80)/(c_a[self.moves(u)]+1)+40
                    
                    
                else:
                    #xblock += 7
                    xblock += (self.width-80)/(c_a[self.moves(u)]+1)
                    #theta -= (pi/(c_a[self.moves(u)]+1))
                    
                    
                    
               #r = (level*(self.height))
                
                u.xy = (int(xblock), int(level*self.height))
               
               
                #if i == 0:
                #    u.xy = (self.width/2,self.height-100)
                #u.xy = (int(r*cos(theta)+self.width/2),int(r*sin(theta)+self.height/2))
                
                u.locate = True
             

            #print i, q.qsize()
            
            
            #sorted(self.a_list1[i], key=attrgetter('win') )
            
                       
            for v in (self.a_list1[i]):
                
                
                if v.locate == False and self.moves(v) < self.moves(u):
                    
                    q.put(v)
                
                    
                
        
        for i in range(len(self.v_list1)):
            c=Counter()
            
            for j in self.symbol[i]:
                c[j]+=1
            
            block = (10-c['-'])/10
            
            if (10-c['-']) not in self.wells:
                self.wells[10-c['-']] = 1
            else:
                self.wells[10-c['-']] += 1
                
                 
            y = int((self.height-50)*(block)-(self.height-50)/20)
            x = randrange(int(15*self.width/31),int(16*self.width/31))
            
            
            self.v_list1[i].xy=(x,y) 
            
        """ 
   
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




    def draw_graphs(self):
       
       #draw the edges
        for i in range(len(self.a_list1)):
             for j in self.a_list1[i]:
                    
                    # pygame.draw.line(self.screen,LAV,self.v_list1[\
                                               # i].xy,j.xy, 1)
                                                
                                               
                if self.v_list1[i].win != j.win:
                                                     
                    if self.moves(j) < self.moves(self.v_list1[i]):
                       
                       col = c_list1[j.win+4] 
                            
                       pygame.draw.line(self.screen,col,j.xy,self.v_list1[i].xy, 1)





        #draw the edges
        for i in range(len(self.a_list1)):
             for j in self.a_list1[i]:
                    
                    # pygame.draw.line(self.screen,LAV,self.v_list1[\
                                               # i].xy,j.xy, 1)
                                                
                                               
                if self.v_list1[i].win == j.win:
                                                     
                    if self.moves(j) < self.moves(self.v_list1[i]):
                       #col = c_list2[j.win+1]
                       col = c_list[0] 
                            
                       pygame.draw.line(self.screen,col,j.xy,self.v_list1[i].xy, 1)


        
        #draw the vertices,
        for i in self.v_list1:
            deg = self.deg(i)
                    
            pygame.draw.circle(self.screen,c_list[0],i.xy,3)
                               



	
    def draw(self):
        self.screen.fill((255,255,255))
        self.draw_board()
       
        self.draw_graphs()        

        pygame.display.flip()




PgmeMain()
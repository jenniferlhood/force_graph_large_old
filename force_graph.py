from __future__ import division
import sys
import pygame
import time
import glob

from random import randrange
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

c_list2 = [(141,160,203),(252,141,98),(102,194,165)]

c_list= [(100,226,240),(80,209,230),(60,189,219),\
            (40,169,207),(20,144,192),(10,129,138),(5,100,80),(1,70,54)]

class Vertex(object):
    def __init__(self,(x,y)):
        self.xy = (x,y)
        self.win = "-"
        self.locate = False
        self.counter = 0
        
        
class PgmeMain(object):
    def __init__(self):

        pygame.init()
        self.width = 1700
        self.height = 1100
        self.screen = pygame.display.set_mode((self.width, self.height))
    
        self.FPS = 5
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        
        
        #program variables
        #fonts
        fontfile = pygame.font.match_font('helvetica')
        self.control_font = pygame.font.Font(fontfile,20)
        self.msg_font = pygame.font.Font(fontfile,30)
            
        self.save_msg = self.msg_font.render("saved",True,CHALK)
        self.load_msg = self.msg_font.render("loaded",True,CHALK)
        
        self.spring_msg = self.msg_font.render("Force embed",True,CHALK)
        
        self.colour_msg1 = self.control_font.render("X wins",True, c_list2[2])
        self.colour_msg2 = self.control_font.render("Draw",True, c_list2[1])
        self.colour_msg3 = self.control_font.render("O wins",True, c_list2[0])
        
        
        #State switch: Used to communicate board state to user 
        # 0 for normal; 1 to save, 2 for load screen,
        # 3 for load msg, 4 for force embed
        self.state = 0 
        self.timer = 0
        
        # save load varables
        # displaying messages
        self.load_list = []
        self.pg_num = 0

        
        
        #vertex and edge variables 
        #vertex list 
        self.v_list1 = []
         
        #adjacency list. 
        # First list index corresponds to the vertex at the 
        # same index in the vertex list    
        self.a_list1 = []
        

        self.selected_index = None
        self.move_vertex = False

        
        self.symbol = []
        self.wells = {}
        self.win = []
        
        self.zoom_list=0

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
                        print "-----"
                        print self.symbol[i][0:3]    
                        print self.symbol[i][3:6]
                        print self.symbol[i][6:9]   
                        print "-----"
                        print u.win
                        print "====="
                        for v in self.a_list1[i]:
                            print v.win,
                        print "====="     
                    
                           
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                #for a left click, 
                # add a vertex at the clicked coordinate (in the primary window)
                # (and only when the loadfile screen isn't displayed)                
                if event.button ==  1 and 10 < pos[0] < \
                                (self.width-10) and 0 < pos[1] < self.height-20\
                                 and (self.state == 0 or self.state == 4):
                    
                    
                    """        
                    #add vertex 
                    if self.selected_index is None:  
                        add = True

                        # when a space without a vertex is clicked, a new vertex is 
                        # created. Otherwise, the vertex can be moved.    
                        for i in self.v_list1:
                            if ((i.xy[0] - 10) < pos[0] < (i.xy[0] + 10)) and \
                                ((i.xy[1] - 10) < pos[1] < (i.xy[1] + 10)):
                                add = False
                                self.move_vertex = True
                                self.selected_index = self.v_list1.index(i)
                                

                        if add:
                        
                            self.v_list1.append(Vertex(pos))
                            self.a_list1.append([])
                    
                         
                    """
                elif event.button == 3 and 10 < pos[0] < \
                                (self.width-10) and 0 < pos[1] < self.height-20\
                                and self.state == 0:
                                
                    if self.selected_index is not None:
                        add = False
                        for i in self.v_list1:
                        
                            if ((i.xy[0]-10) < pos[0] < (i.xy[0]+10)) and \
                                ((i.xy[1]-10) < pos[1] < (i.xy[1]+10)):                
                                add = True
                        if add == False:
                            self.selected_index = None
                            
                            
                elif event.button == 1 and self.state == 2:
                    
                    select_file = None
                
                    while select_file == None:
                        #if there are more than 20 entries, click the down button
                        if len(self.load_list) // 20 > 0:
                    
                    
                            if 2*self.width/3 -8 < pos[0] < \
                                    2*self.width/3 + 8 and 2*self.height/3 - 8 <\
                                    pos[1] < 2*self.height/3 + 8:
                                self.pg_num += 1
                        
                            
                        #click on the desired file
                        if self.width/4 < pos[0] < self.width/2 \
                                and self.height/3 < pos[1] < 2*self.height/3:
                    
                            if int(self.pg_num+(pos[1]-40-self.height/3)//20)\
                                                             < len(self.load_list):
                               
                      
                                select_file = self.load_list[int(self.pg_num+\
                                        (pos[1]-40-self.height/3)//20)]
                                self.load_data(select_file)
                            
                        elif self.width/2 < pos[0] < 3*self.width/4    \
                                and self.height/3 < pos[1] < 2*self.height/3:
                    
                            if 10+int(self.pg_num+(pos[1]-40-self.height/3)//20)\
                                                                 < len(self.load_list):
                                   

                                select_file = self.load_list[10+int(self.pg_num+\
                                        (pos[1]-40-self.height/3)//20)]
                                self.load_data(select_file)
                        else:
                            select_file = 0
                            self.state = 0    
                        #elif len(self.load_list) == 0:
        
            


            elif event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                #when a moved vertex is "dropped", 
                #  update the vertex list and adjacency list
                if event.button == 1 and self.move_vertex and \
                        10 < pos[0] < (self.width-10) and \
                        0 < pos[1] < self.height-40:
                    
                    self.v_list1[self.selected_index].xy = pos
                    self.selected_index = None
                    self.move_vertex = False
                    
                """
                # connecting two vertices with an edge    
                elif event.button == 3\
                     and 10 < pos[0] < (self.width-10) and \
                     0 < pos[1] < self.height-20:
                    

                    for i in self.v_list1:
                        if (i.xy[0] - 10) < pos[0] < (i.xy[0] + 10) and \
                                (i.xy[1] - 10) < pos[1] < (i.xy[1] + 10):
                            
                            if self.selected_index is None:
                                self.selected_index = self.v_list1.index(i)

                            elif self.selected_index is not None and \
                                    self.v_list1[self.selected_index] != i\
                                    and i not in self.a_list1[self.selected_index]:
                                
                                #join two different selected vertices with an edge in g1
                                self.a_list1[self.selected_index].append(i)
                                self.a_list1[self.v_list1.index(i)].append(\
                                        self.v_list1[self.selected_index])
                           
                                
                                
                                self.selected_index = None
                                           
                            
                            else:
                                self.selected_index = None
                                self.move_vertex = None
                    
                else:
                    self.selected_index = None
                    self.move_vertex = None
                """
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                
                if self.state == 0:           
                    self.timer = time.time()
                    self.state = 4
                    
                elif self.state == 4:
                    self.state = 0
                   
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
             
                    self.v_list1 = []
                    self.a_list1 = []
                    self.zoom_list=0
                    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    
                    if self.zoom_list < 2:
                        for i in self.v_list1:
                            x= i.xy[0]
                            y= i.xy[1]
                            m_x = self.width/2
                            m_y = (self.height-50)/2
                            
                            i.xy = (int(x+(x-m_x)*2),int(y+(y-m_y)*2))
                        self.zoom_list +=1
                            
                            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                   
                    if self.zoom_list > -2:
                        for i in self.v_list1:
                            x= i.xy[0]
                            y= i.xy[1]
                            m_x = self.width/2
                            m_y = (self.height-50)/2
                            
                            i.xy= (int(x-(x-m_x)/1.5),int(y-(y-m_y)/1.5))
                            
                        self.zoom_list -=1

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
                self.load_list = glob.glob("*.graph")
              
            elif event.type == self.REFRESH:
            
                # Draw the interface 
                
                self.draw()
               
                
                if self.state == 4:
                    self.force()
                    
            else:
                pass
 
    def deg(self,v):
        return len(self.a_list1[self.v_list1.index(v)])
   
    def win_loose_draw(self):
        #win:
        for i in self.symbol:
        
            #if "-" not in i:
            #    self.win.append("d")
            
            
            #else:    
            
            
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
        q = Queue()
        q.put(self.v_list1[0])
        xblock = 80
        level = 1/11
        
        theta = 0
        
        
        #set the counters
        c=Counter()
        c_a=Counter()
        
        for i in range(len(self.v_list1)):
            u = self.v_list1[i]
            c_a[self.moves(u)] += 1
            
            for v in self.a_list1[i]:
                if self.moves(v) > self.moves(u):
                    c[u] +=1
                    
            u.counter = int(c[u]/2)
            
            
            
            
        while q.qsize() > 0:
            
            
            u = q.get()
            i = self.v_list1.index(u)
            
                                 
            new_level = (10-self.moves(u))/11
              
            if u.locate == False: #and u.counter == 0:    

                if new_level > level:
                    level = new_level
                    #theta = 0
                    #xblock = 80
                    xblock = (self.width-50)/(c_a[self.moves(u)]+1)
                    
                    
                else:
                    #xblock += 7
                    xblock += (self.width-50)/(c_a[self.moves(u)]+1)
                    #theta -= (pi/(c_a[self.moves(u)]+1))
                    
                    
                    
                r = (level*(self.height))
                
                u.xy = (int(xblock), int(level*self.height))
               
               
                #if i == 0:
                #    u.xy = (self.width/2,self.height-100)
                #u.xy = (int(r*cos(theta)+self.width/2),int(r*sin(theta)+self.height/2))
                
                u.locate = True
             
            if u.counter > 0:
                u.counter - 1
            
            #print i, q.qsize()
            
            
            #sorted(self.a_list1[i], key=attrgetter('win'))
            
            for v in sorted(self.a_list1[i], key=attrgetter('win')):
                if v.locate == False and self.moves(v) < self.moves(u):
                    
                    q.put(v)
                
                    
                
        """
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
        
            
    def force(self):
        print  time.time() - self.timer            
        if time.time() - self.timer > 50:
                self.state = 0
                
                
        n = max(1,len(self.v_list1))
        K = int((sqrt((self.width*self.height)/n)))
        K=self.height/18  
       
        spring = 1/30
        temp = 1/200 #the "temperature" of the repulsive force. 
        temp = 1/1000
        
        disp_list = []
        vx = vy = d = 0
        
        for i in self.v_list1:
            fx_a = fy_a = 0
                         
          
            #spring force for adjacent vertices
            for j in self.a_list1[self.v_list1.index(i)]:
                if i is not j and self.moves(j) <7:
                    # vector from j to i
                    (vx, vy) = (i.xy[0]-j.xy[0]), (i.xy[1]-j.xy[1])
                    d = sqrt(vx**2 + vy**2)

                    disp = int(K - d)

                    # unit vector from j to i  
                    if d != 0:
                        (nx, ny) = (vx/d, vy/d)
                    else:
                        (nx, ny) = (0,0)
                    
                    #print "disp = {}".format(disp)
                    # disp_y = K - abs(i.xy[1]-j.xy[1])

                    fx_a += int(spring*(nx*disp**2/K)*(disp/max(1,abs(disp))))
                    fy_a += int(spring*(ny*disp**2/K)*(disp/max(1,abs(disp))))
                    
                                       
                    #print "(vx,vy) = ({},{}), disp = {}, fx={}".format(vx, vy,disp,fx_a)
                    #get the direction of the vector (+ or -)
            
            
            
            """
            ####
            ## angular motion 1
            n= 0
            (ux,uy) = (0,0)
            nf_a = 0
            (f_ux,f_uy) = (0,0)
            
            (vx,vy) = (i.xy[0] - self.width/2),(i.xy[1]-self.height-100)
            
            #orthogonal vector:
            if fx_a >0:
                if fx_a/abs(fx_a) > 0:
                    (ox,oy) = (-vx,vy)
                else:
                    (ox,oy) = (vx,-vy)
            
                n = sqrt(ox**2 + oy**2)


                #unit vector
                (ux, uy) = (ox/n, oy/n)
            
            else:
                (ox,oy) = (0,0)
                (ux,uy) = (0,0) 
               
           
            
            nf_a = sqrt(fx_a**2+fy_a**2)/5

            (f_ux,f_uy) = (nf_a*f_ux,nf_a*uy)

            ###
            
            
            #angular motion 2
            
            (vx,vy) = (i.xy[0] - self.width/2),(i.xy[1]-self.height/2)
            r = sqrt(vx**2 + vy**2)
                
                
            if i.xy[0]+fx_a*(1/self.FPS)-self.width/2 != 0:
                theta = atan((i.xy[1]+fy_a*(1/self.FPS)-(self.height/2))/(i.xy[0]+fx_a*(1/self.FPS)-self.width/2))
                
                
                fx_a = int(r*cos(theta))
                fy_a = int(r*sin(theta))
                
            else:
                fx_a = 0
                fx_y = 0
    
            """
            
            #proximity to other vertices
            (fx_r,fy_r) = (0,0)
            
            for j in self.v_list1:
                if i is not j and self.moves(j) <7:
                    (vx, vy) = (i.xy[0]-j.xy[0]), (i.xy[1]-j.xy[1])
                    d = sqrt(vx**2 + vy**2)
                  
                    if d != 0:
                        (nx, ny) = (vx/d, vy/d)
                        fx_r += temp*int(nx * ((K)**2)/d)
                        fy_r += (1/5)*temp*int(ny * ((K)**2)/d)
     
            
            # wall repusion (similar to vertices repulsion)
            nx = 1
            fx_w = fy_w = 0
                       
            # left direction
            d = vx = i.xy[0]-10
                        
            if d != 0:
               
                fx_w +=  int(nx * (K**2)/d)
                        
            # right direction
            d = vx = i.xy[0]-(self.width-10)
                        
            if d != 0:
                fx_w +=  int(nx * (K**2)/d)

            # top 
            d = vy = i.xy[1] - 10
                        
            if d != 0:
                fy_w +=  temp*int(ny * (K**2)/d)
            
            # bottom 
            d = vy = i.xy[1]-(self.height-50)
                        
            if d != 0:
                fy_w +=  temp*int(ny * (K**2)/d)
            
           
            (fx_w,fy_w) = self.walls1(i,temp,K)
               
#           disp_list.append((int(i.xy[0]+fx_a*(2/self.FPS)+fx_r*(2/self.FPS)\
#                            +fx_w*(2/self.FPS)),\
#                    int(i.xy[1]+fy_a*(2/self.FPS)+fy_r*(2/self.FPS)\
#                            +fy_w*(2/self.FPS))))
            
            
            
            disp_list.append((int(i.xy[0]+fx_a*(2/self.FPS)+fx_r*(2/self.FPS)\
                            +fx_w*(2/self.FPS)), i.xy[1]))
            
            
            #disp_list.append((fx_a,fy_a))
                            
                            
            
            
             
        #update vertex positions
        for i in range(len(self.v_list1)):
            self.v_list1[i].xy = disp_list[i]
            
            
    def walls2(self,v,temp,K):
        fx_w = 0
        
        for i in self.wells:
            for j in range(self.wells[i]):
                block = (self.width*j/self.wells[i], self.width*(j+1)/self.wells[i])
                # left direction
                d = vx = v.xy[0]-block[0]
                    
                if d != 0:
                    fx_w +=  temp*int(K**2*log(abs(d)))
                        
                # right direction
                d = vx = v.xy[0]-block[1]
                        
                if d != 0:
                    fx_w +=  temp*int(K**2*log(abs(d)))
        return fx_w
      
    
    
    
    def walls1(self,v,temp,K):
        fx_w = 0
        fy_w = 0
        
        if len(self.v_list1) >= 765:
            walls = 10
        else:
            wall = 1 
       
        
        for i in range(walls):
            block = (i/walls*(self.height-50), (i+1)/walls*(self.height-50))
        
            # left direction
            d = vx = v.xy[0]-10
                        
            if d != 0:
                fx_w +=  10*temp*int(K**2/d)
                        
            # right direction
            d = vx = v.xy[0]-(self.width-10)
                        
            if d != 0:
                fx_w +=  10*temp*int(K**2/d)

            # top 
            d = vy = v.xy[1] - (block[0]+10)
                        
            if d != 0:
                fy_w +=  10*temp*int(K**2/d)
            
            # bottom 
            d = vy = v.xy[1]- (block[1]-10)
                        
            if d != 0:
                fy_w +=  10*temp*int(K**2/d)
      
        return (fx_w,fy_w)













        
    def state_msg(self,msg):
        #messages to user regarding program state
            
        rect = self.save_msg.get_rect()
        rect = rect.move(10,self.height-80)
        self.screen.blit(msg,rect)
        
        if self.state != 4:
            if time.time() - self.timer > 2:
                self.state = 0
        

    def load_files(self):
        #load file window
        rect_load = (self.width/4,self.height/3,2*(self.width/4),self.height/3)
        pygame.draw.rect(self.screen,(0,0,0),rect_load)        
        pygame.draw.rect(self.screen,AQUA,rect_load,4)    

        loadmsg = self.control_font.render("select a file",True, AQUA)
        rect = loadmsg.get_rect()
        rect = rect.move(self.width/4+10, self.height/3 + 10)
        self.screen.blit(loadmsg,rect)
        page = len(self.load_list)

        if self.pg_num > page:
            self.pg_num = 0
        move_pos = 40        
        for i in self.load_list[self.pg_num+0:self.pg_num+9]:
                 # list the files under each other
                files = self.control_font.render(i,True, CHALK)
                rect = files.get_rect()
                rect = rect.move(self.width/4+10,self.height/3+move_pos)
                self.screen.blit(files,rect)
                move_pos += 20

        move_pos = 40    
        for i in self.load_list[self.pg_num+10:self.pg_num+19]:
                 # list the files under each other
                files = self.control_font.render(i,True, CHALK)
                rect = files.get_rect()
                rect = rect.move(self.width/2+10,self.height/3+move_pos)
                self.screen.blit(files,rect)
                move_pos += 20

        if page // 20 > 0:
            self.next_pg_button()

        #if there are more than 20 files to diplay, do next screen
    
    def next_pg_button(self):
        x = 3*(self.width/4)
        y = self.height/3

        pygame.draw.circle(self.screen,PEA,(int(2*x),int(2*y)),10)
        pygame.draw.polygon(self.screen,(0,0,0),\
                                ((2*x-6,2*y-5),(2*x+6,2*y-5),(2*x,2*y+6)))
    
    def draw_board(self):
        #draw the primary and secondary view
        rect_g1 = (0,0,self.width-2,self.height-40)
        
        pygame.draw.rect(self.screen,CHALK,rect_g1,4)
        
                    
        rect = self.colour_msg1.get_rect()
        rect = rect.move(25,25)
        self.screen.blit(self.colour_msg1,rect)
        rect = rect.move(0,30)
        self.screen.blit(self.colour_msg2,rect)
        rect = rect.move(0,30)
        self.screen.blit(self.colour_msg3,rect)
        
        # draw controls
        msg1 = "mouse left : add/move vertex  |  mouse right : connect vertex    "
        msg2 = "|  d : delete   |   s : save to file   |   l: load from file   "
        msg3 =    "|  f : force embed   |   i: zoom in  |   o: zoom out "
        
        controls = self.control_font.render(msg1+msg2+msg3,True, CHALK)
        rect = controls.get_rect()
        rect = rect.move(10,self.height-30)
        self.screen.blit(controls,rect)
    
        
        #messages regarding board state
    def draw_messages(self):
        if self.state == 1:
            self.state_msg(self.save_msg)
        
        elif self.state == 2:
            self.load_files()
            
        elif self.state == 3:
            self.state_msg(self.load_msg)

        elif self.state == 4:
            self.state_msg(self.spring_msg)

        

    def draw_graphs(self):
        pos = pygame.mouse.get_pos()

        #extract the selected vertex
        if self.selected_index is not None:
            selected_vertex = self.v_list1[self.selected_index]
       
        else:
            selected_vertex = None
        
        

        # Draw the edges of adjacent vertecies:
        # Draw a line from the i,jth vertex in the a_list 
        # to each of the vertexes listed in the corresponding
        # ith vertex in the v_list
        
        # when one vertex is being moved, make sure not to draw the edges
        # until it reaches its final destination
       
        
        if self.move_vertex:
            for i in range(len(self.a_list1)):
                deg = self.deg(self.v_list1[i])
                col = c_list[7-min(deg,7)]
                
                for j in self.a_list1[i]:
                    if j is not selected_vertex and self.v_list1[i]\
                                                          is not selected_vertex:

                            pygame.draw.line(self.screen,LAV,self.v_list1[i].xy,j.xy, 1)

                    else:
                        for j in self.a_list1[self.selected_index]:
                            pygame.draw.line(self.screen,LAV,pos,j.xy, 1)
            
                            
    
    
    
    
        else:

            for i in range(len(self.a_list1)):
                deg = self.deg(self.v_list1[i])
                col = c_list[7-min(deg,7)]
                for j in self.a_list1[i]:
                   # pygame.draw.line(self.screen,LAV,self.v_list1[\
                                               # i].xy,j.xy, 1)
                                                
                                                
                                                
                                                
                    if self.moves(j) < self.moves(self.v_list1[i]):
                        col = c_list2[j.win+1]
                        
                        pygame.draw.line(self.screen,col,\
                            j.xy,self.v_list1[i].xy, 1)




        
        #draw the vertices,
        # if one in the list is the selected vertex, draw it a different colour,
        # or draw it moving with the cursor.
        for i in self.v_list1:
            deg = self.deg(i)
            col = c_list2[i.win+1]
            
            if i is not selected_vertex:
                pygame.draw.circle(self.screen,col,i.xy,4)
            else:
                if self.move_vertex:
                    pygame.draw.circle(self.screen,LAV,pos,4)
                else:
                    pygame.draw.circle(self.screen,colh,i.xy,4)
                    pygame.draw.line(self.screen,CORAL,i.xy,pos,1)
                    

	
    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_board()
       
        self.draw_graphs()        
        
        self.draw_messages()
    
                
        pygame.display.flip()





PgmeMain()

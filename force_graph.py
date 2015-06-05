from __future__ import division
import sys
#import math 
import pygame
import time
import glob

from random import randrange
from math import sqrt
from math import log
from collections import Counter


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

c_list= [(100,226,240),(80,209,230),(60,189,219),\
            (40,169,207),(20,144,192),(10,129,138),(5,100,80),(1,70,54)]

class Vertex(object):
    def __init__(self,(x,y)):
        self.xy = (x,y)
        self.symbol = []
        
class PgmeMain(object):
    def __init__(self):

        pygame.init()
        self.width = 1700
        self.height = 1100
        self.screen = pygame.display.set_mode((self.width, self.height))
    
        self.FPS = 30
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
                a= a.rstrip('\r\n')
                self.symbol.append(a)
        
            self.reorder()
    

    # Main Event handling method
    #
    #
    def event_loop(self):
        
        while True:
          
            event = pygame.event.wait()



            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                #for a left click, 
                # add a vertex at the clicked coordinate (in the primary window)
                # (and only when the loadfile screen isn't displayed)                
                if event.button ==  1 and 10 < pos[0] < \
                                (self.width-10) and 0 < pos[1] < self.height-20\
                                 and (self.state == 0 or self.state == 4):

                    #add move vertex 
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
                                #######
                      
                                select_file = self.load_list[int(self.pg_num+\
                                        (pos[1]-40-self.height/3)//20)]
                                self.load_data(select_file)
                            
                        elif self.width/2 < pos[0] < 3*self.width/4    \
                                and self.height/3 < pos[1] < 2*self.height/3:
                    
                            if 10+int(self.pg_num+(pos[1]-40-self.height/3)//20)\
                                                                 < len(self.load_list):
                                    #######

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
            
                    print self.zoom_list
                    if self.zoom_list < 2:
                        for i in self.v_list1:
                            x= i.xy[0]
                            y= i.xy[1]
                            m_x = self.width/2
                            m_y = (self.height-50)/2
                            
                            i.xy = (int(x+(x-m_x)*2),int(y+(y-m_y)*2))
                        self.zoom_list +=1
                            
                            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                    print self.zoom_list
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
                print "ok"
                
                if self.state == 4:
                    self.force()

            else:
                pass
    
    
   

    def deg(self,v):
        return len(self.a_list1[self.v_list1.index(v)])
        
    def reorder(self):

        for i in range(len(self.v_list1)):
            c=Counter()
            
            for j in self.symbol[i]:
                c[j]+=1
            
            block = (10-c['-'])/10
            
            if (10-c['-']) not in self.wells:
                self.wells[10-c['-']] = 1
            else:
                self.wells[10-c['-']] += 1
                
            print self.wells         
            y = int((self.height-50)*(block)-(self.height-50)/20)
            x = int(randrange(self.width/4,3*self.width/4))
            
            
            self.v_list1[i].xy=(x,y) 
               
    def force(self):
        print  time.time() - self.timer            
        if time.time() - self.timer > 60:
                self.state = 0
                
                
        n = max(1,len(self.v_list1))
        K = int((sqrt((self.width*self.height)/n))*(1/2))
            
       
        spring = 1/20
        temp = 2 #the "temperature" of the repulsive force. 
        
        disp_list = []
        vx = 0
        vy = 0
        d = 0
        

        for i in self.v_list1:
            fx_a = 0
            fy_a = 0
            
          
            #spring force for adjacent vertices
            for j in self.a_list1[self.v_list1.index(i)]:
                if i is not j:
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
                    #fy_a += int(spring*(ny*disp**2/K)*(disp/max(1,abs(disp))))
                    
                                       
                    #print "(vx,vy) = ({},{}), disp = {}, fx={}".format(vx, vy,disp,fx_a)
                    #get the direction of the vector (+ or -)
         
            fx_r = 0
            fy_r = 0 
            
            #proximity to other vertices
            
            
             
            for j in self.v_list1:
                if i is not j:
                    (vx, vy) = (i.xy[0]-j.xy[0]), (i.xy[1]-j.xy[1])
                    d = sqrt(vx**2 + vy**2)
                    
                    #disp = int(K - d)
                    # unit vector from j to i  
                    
                    
                    if d != 0:
                        (nx, ny) = (vx/d, vy/d)
                        fx_r += temp*int(nx * (K**2)/d)
                        fy_r += temp*int(ny * (K**2)/d)
               # print "(vx,vy) = ({},{}), disp = {}, fx={}".format(vx, vy,d,fx_r)
       
            
            # wall repusion (similar to vertices repulsion)
            
            
            
            fx_w = 0
            fy_w = 0
            
            # left direction
            d = vx = i.xy[0]-10
                        
            if d != 0:
                nx = 1
                fx_w +=  int(nx * (K**2)/d)
                        
            # right direction
            d = vx = i.xy[0]-(self.width-10)
                        
            if d != 0:
                nx = 1
                fx_w +=  int(nx * (K**2)/d)

            """
            # top 
            d = vy = i.xy[1] - 10
                        
            if d != 0:
                ny = 1
                fy_w +=  temp*int(ny * (K**2)/d)
            
            # bottom 
            d = vy = i.xy[1]-(self.height-50)
                        
            if d != 0:
                ny = 1
                fy_w +=  temp*int(ny * (K**2)/d)
            
           
            """
            
               
#            disp_list.append((int(i.xy[0]+fx_a*(2/self.FPS)+fx_r*(2/self.FPS)\
#                            +fx_w*(2/self.FPS)),\
#                    int(i.xy[1]+fy_a*(2/self.FPS)+fy_r*(2/self.FPS)\
#                            +fy_w*(2/self.FPS))))
            
            
            fx_r=0
            
            disp_list.append((int(i.xy[0]+fx_a*(2/self.FPS)+fx_r*(2/self.FPS)\
                            +fx_w*(2/self.FPS)), i.xy[1]))
             
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
        
        if len(self.v_list1) == 765:
            walls = 10
        else:
            wall = 1 
       
        
        for i in range(walls):
            block = (i/walls*(self.height-50), (i+1)/walls*(self.height-50))
        
            # left direction
            d = vx = v.xy[0]-10
                        
            if d != 0:
                fx_w +=  2*temp*int(K**2/d)
                        
            # right direction
            d = vx = v.xy[0]-(self.width-10)
                        
            if d != 0:
                fx_w +=  2*temp*int(K**2/d)

            # top 
            d = vy = v.xy[1] - (block[0]+10)
                        
            if d != 0:
                fy_w +=  2*temp*int(K**2/d)
            
            # bottom 
            d = vy = v.xy[1]- (block[1]-10)
                        
            if d != 0:
                fy_w +=  2*temp*int(K**2/d)
      
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
        
        pygame.draw.rect(self.screen,SUN,rect_g1,4)
       
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
                    pygame.draw.line(self.screen,LAV,self.v_list1[\
                                                i].xy,j.xy, 1)



        #draw the vertices,
        # if one in the list is the selected vertex, draw it a different colour,
        # or draw it moving with the cursor.
        for i in self.v_list1:
            deg = self.deg(i)
            col = c_list[7-min(deg,7)]
            colh = (col[0]+50,col[1]+20,col[2]+10)
            
            if i is not selected_vertex:
                pygame.draw.circle(self.screen,col,i.xy,4)
            else:
                if self.move_vertex:
                    pygame.draw.circle(self.screen,colh,pos,4)
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

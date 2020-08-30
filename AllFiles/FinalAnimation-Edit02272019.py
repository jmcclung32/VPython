
# coding: utf-8

# In[1]:


import csv #used for reading and parsing data from a text file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


#get the empty rows
filename='clean_cmj.txt'
datafile = csv.reader(open(filename, 'r'), delimiter='\t')

counter = 0 #counter for number of rows
empty_rows = []
for row in datafile:
    if len(row)==0: #test for an empty row
        empty_rows.append(counter)    
    counter += 1
print(empty_rows)


# In[3]:


datafile = csv.reader(open(filename, 'r'), delimiter='\t')

# get position data
counter = 0 #counter for number of rows
pos_header = []
pos_units = []
pos_direction = []
pos_data = []
for row in datafile:
    if counter==empty_rows[0]+1:
        pos_header.append(row)
    elif counter==empty_rows[0]+2:
        pos_units.append(row)
    elif counter==empty_rows[0]+3:
        pos_direction.append(row)
    elif counter>empty_rows[0]+3 and counter<empty_rows[1] :
        pos_data.append(row)
    elif counter>=empty_rows[1]:
        break
    counter = counter + 1
    
    
    
    
datafile = csv.reader(open(filename, 'r'), delimiter='\t')


# get force data
counter1 = 0 #counter for number of rows
force_header = []
force_units = []
force_direction = []
force_data = []
for row in datafile:
    if counter1==empty_rows[1]+1:
        force_header.append(row)
    elif counter1==empty_rows[1]+2:
        force_units.append(row)
    elif counter1==empty_rows[1]+3:
        force_direction.append(row)
    elif counter1>empty_rows[1]+3 and counter1<empty_rows[2] :
        force_data.append(row)
    elif counter1>=empty_rows[2]:
        break
    counter1 = counter1 + 1
    


# In[4]:


#make headers
pos_head_unit = []
counter = 0
i = 0
for i in range(len(pos_header[0])):
    if i == 0:
        head_plus_unit = pos_header[0][i]
        pos_head_unit.append(head_plus_unit)
    else:
        if counter == 0:
            head_plus_unit = pos_header[0][i] +  '_'  +   pos_direction[0][i]
            pos_head_unit.append(head_plus_unit) 
        else:
            head_plus_unit = pos_header[0][i-counter] +  '_'  + pos_direction[0][i] 
            pos_head_unit.append(head_plus_unit)    
            
        counter += 1
        if counter == 3:
            counter = 0
            
force_head_unit = []
counter1 = 0

for j in range(len(force_header[0])):
    if j == 0:
        fhead_plus_unit = force_header[0][j]
        force_head_unit.append(fhead_plus_unit)
    else:
        if counter1 == 0:
            fhead_plus_unit = force_header[0][j] +  '_'  +   force_direction[0][j]
            force_head_unit.append(fhead_plus_unit) 
        else:
            fhead_plus_unit = force_header[0][j-counter1] +  '_'  + force_direction[0][j] 
            force_head_unit.append(fhead_plus_unit)    
            
        counter1 += 1
        if counter1 == 3:
            counter1 = 0


# In[5]:


df = pd.DataFrame(pos_data, columns=pos_head_unit)
#df

df1 = pd.DataFrame(force_data, columns=force_head_unit)
#df1

#make all floats

df = df.astype(float)
df1 = df1.astype(float)

#make array

df.shape[1]
data = df.values
pos_data=data[:,1:-1]

df1.shape[1]
data1 = df1.values
force_data=data1[:,1:-1]
#print(pos_data.shape, force_data.shape)


# In[6]:


times = data1[:,0]
# len(time)


# In[7]:


forcepos = np.zeros((force_data.shape[0], 3))
i = 6
for row in range(force_data.shape[0]):
    i = 6
    k = 0
    while i < 9:
        forcepos[row, k] = force_data[row,i]
        i = i + 1
        k = k + 1

forcepos2 = np.zeros((force_data.shape[0], 3))
i = 18
for row in range(force_data.shape[0]):
    i = 18
    k = 0
    while i < 21:
        forcepos2[row, k] = force_data[row,i]
        i = i + 1
        k = k + 1        
        
        
#forcepos2


# In[8]:


#df1


# In[9]:


from vpython import *


# In[10]:


def animate(row0): #row0 is first row of animation
    global rowPaused
    for row in range(row0,pos_data.shape[0]):
        rate(40)
        j=0
        l = 0
        for k in range(pos_data.shape[1]-2):
            if k % 3==0:
                if pos_data[row,k] != 0:
                    balls[j].pos = vec(pos_data[row,k],pos_data[row,k+2], pos_data[row,k+1])
                    balls[j].visible = True
                    if k % 4==0 and l < 2:
                        forces[l].axis = 1.5*vector(force_data[row,k],force_data[row,k+2],force_data[row,k+1])
                        forces[l].pos = vector(forcepos[row,0],forcepos[row,2],forcepos[row,1])
                        forces[l].visible = True
                        #updategraph(times[row],forces[1].axis.y)
                        if l == 1:
                            forces[l].pos = vector(forcepos2[row,0],forcepos2[row,2],forcepos2[row,1])
                        updatefgraph(times[row],forces[0].axis.y,times[row],forces[1].axis.y)
                        l = l+1

                else:
                    balls[j].visible = False

                j = j+1
        update()
        
        

        if running==False:
            rowPaused = row
            return row
    fcurve.delete()
    fcurve2.delete()
   
    
    rowPaused = 0
    return row


# In[13]:


def join():
    global pipe, pairs, name, anglepair
    
    name= {
    "L_Trunk":balls[0],
    "R_Trunk":balls[1],
    "D_Trunk":balls[2],
    "R_Shoulder":balls[3],
    "R_Elbow":balls[4],
    "R_Wrist":balls[5],
    "L_Shoulder":balls[6],
    "L_Elbow":balls[7],
    "L_Wrist":balls[8],
    "R_Crest":balls[9],
    "R_ASIS":balls[10],
    "Sacrum":balls[11],
    "Offset":balls[12],
    "L_ASIS":balls[13],
    "L_Crest":balls[14],
    "R_Hip":balls[15],
    "R_Thigh":balls[16],
    "R_Knee":balls[17],
    "R_Tib":balls[18],
    "R_MidShank":balls[19],
    "R_DistShank":balls[20],
    "R_Heel":balls[21],
    "R_DistHeel":balls[22],
    "R_PostFoot":balls[23],
    "R_LatToe":balls[24],
    "R_Toe":balls[25],
    "R_MedToe":balls[26],
    "L_Hip":balls[27],
    "L_Thigh":balls[28],
    "L_Knee":balls[29],
    "L_Tib":balls[30],
    "L_MidShank":balls[31],
    "L_DistShank":balls[32],
    "L_Heel":balls[33],
    "L_DistHeel":balls[34],
    "L_PostFoot":balls[35],
    "L_LatToe":balls[36],
    "L_Toe":balls[37],
    "L_MedToe":balls[38]}


    pairs = [["R_Trunk", "L_Trunk"], ["R_Trunk", "D_Trunk"], ["R_Trunk", "R_Shoulder"], ["R_Shoulder", "L_Trunk"], #4
         ["R_Shoulder", "D_Trunk"], ["R_Shoulder","R_Elbow"], ["R_Elbow", "R_Wrist"], ["L_Trunk", "D_Trunk"], #8
         ["L_Trunk", "L_Shoulder"], ["L_Shoulder", "R_Trunk"], ["L_Shoulder", "D_Trunk"], ["L_Shoulder", "L_Elbow"], #12
         ["L_Elbow", "L_Wrist"], ["R_Crest", "Sacrum"], ["R_Crest", "R_Hip"], ["R_ASIS", "R_Crest"], #16
         ["R_ASIS", "Sacrum"], ["R_ASIS", "D_Trunk"], ["R_ASIS", "R_Hip"], ["R_ASIS", "L_ASIS"], #20
         ["R_ASIS", "Offset"], ["Sacrum", "Offset"], ["Sacrum", "D_Trunk"], ["L_ASIS", "L_Crest"], #24
         ["L_ASIS", "Sacrum"], ["L_ASIS", "D_Trunk"], ["L_ASIS", "L_Hip"], ["L_ASIS", "Offset"], #28
         ["L_Crest", "Offset"], ["L_Crest", "L_Hip"],  #30
         #Legs;  
         ["R_Hip", "R_Thigh"], ["R_Hip", "R_Knee"],["R_Hip", "R_Tib"], ["R_Knee", "R_Tib"], #34
         ["R_Knee", "R_MidShank"], ["R_Knee", "R_DistShank"],["R_Tib", "R_Thigh"], ["R_Tib", "R_DistShank"], #38
         ["R_Tib", "R_MidShank"], ["R_MidShank", "R_DistShank"],["R_DistShank", "R_Heel"], ["R_Heel", "R_DistHeel"], #42
         ["R_Heel", "R_Toe"], ["R_DistHeel", "R_PostFoot"],["R_DistHeel", "R_DistShank"], ["R_PostFoot", "R_LatToe"], #46
         ["R_PostFoot", "R_Toe"], ["R_PostFoot", "R_DistShank"], ["R_LatToe", "R_Toe"], ["R_Toe", "R_MedToe"], #50
         ["R_MedToe", "R_DistHeel"],  #51
      
         ["L_Hip", "L_Thigh"], ["L_Hip", "L_Knee"], ["L_Hip", "L_Tib"], ["L_Knee", "L_Tib"], #55
         ["L_Knee", "L_MidShank"], ["L_Knee", "L_DistShank"],["L_Tib", "L_Thigh"], ["L_Tib", "L_DistShank"], #59
         ["L_Tib", "L_MidShank"], ["L_MidShank", "L_DistShank"],["L_DistShank", "L_Heel"], ["L_Heel", "L_DistHeel"], #63
         ["L_Heel", "L_Toe"], ["L_DistHeel", "L_PostFoot"],["L_DistHeel", "L_DistShank"], ["L_PostFoot", "L_LatToe"], #67
         ["L_PostFoot", "L_Toe"], ["L_PostFoot", "L_DistShank"], ["L_LatToe", "L_Toe"], ["L_Toe", "L_MedToe"], #71
         ["L_MedToe", "L_DistHeel"]]  #72
    
    
    anglepair = [["R_Crest", "R_Hip"], ["R_Knee", "R_Hip"],
                 ["R_Hip", "R_Knee"],["R_MidShank", "R_Knee"],
                ["R_DistShank", "R_DistHeel"],["R_MedToe", "R_DistHeel"],
                 
                ["L_Crest", "L_Hip"], ["L_Knee", "L_Hip"],
                 ["L_Hip", "L_Knee"],["L_MidShank", "L_Knee"],
                ["L_DistShank", "L_DistHeel"],["L_MedToe", "L_DistHeel"]]
    

    pipe = []
    
    for pair in pairs:
        cylinders = cylinder(pos=name[pair[0]].pos, axis=name[pair[1]].pos - name[pair[0]].pos, color=(vec(1,1,1)+vec.random())/2, radius=4)    
        pipe.append(cylinders)

   
    return ()



#     jointvec = []
#     for pair in anglepair:
#         jointvec.append(name[pair[1]].pos - name[pair[0]].pos)


def update ():
    m = 0
    for pair in pairs:
        if name[pair[0]].visible == True:
            pipe[m].visible = True	


        else:
            pipe[m].visible = False
    
        pipe[m].pos = name[pair[0]].pos
        pipe[m].axis = name[pair[1]].pos - name[pair[0]].pos
        m = m + 1
            
            
    
    
    


# In[14]:


def makegraph():
    global fcurve, fcurve2, g
    g = graph(width=600, height=150, 
      title='<b>Force (z)</b>',
      xtitle='<i>Time (s)</i>', ytitle='<i>Force (N)<i>', 
      foreground=color.black, background=color.white, 
      xmin=1.75,xmax=3.5,  ymin=0)
    fcurve = gcurve(color = color.red, label = 'Right') 
    fcurve2 = gcurve(color = color.blue, label = 'Left')
    
    return ()

def updatefgraph(x,y,x1,y1):
    fcurve.plot(pos=(x,y))
    fcurve2.plot(pos=(x1,y1))            
    return ()
    


# In[ ]:


scene=canvas()
scene.width = 400
scene.height = 400
scene.background = color.white

if filename == 'clean_cmj.txt':
	scene.title = "Countermovement Jump \n"
if filename == 'clean_cut.txt':
	scene.title = "Cut Task \n"
if filename == 'clean_prowler.txt':
	scene.title = "Prowler Push \n"

x = 500
y = 1000
z = 1000

scene.camera.pos = vector(x, y ,0)

running = True
def Run(b):
    global running
    running = not running 
    if running: 
        b.text = "Pause"
    else: 
        b.text = "Run"

def rotscene(s):
#    rotate(scene.up, angle=s, axis=vector(1,0,0) )
    scene.forward = vector(-np.cos(pi/2-s.value),0,-np.cos(s.value))
#    stext.text = '{:1.2f}'.format(s.value)

button(text="Pause", bind=Run)
sl = slider(min=0, max=pi/2, value=0, length=200, bind=rotscene, right=15)

# draw axes
arrow(pos=vec(0,0,0), axis = vec(500,0,0), color=color.gray(0.5))
arrow(pos=vec(0,0,0), axis = vec(0,500,0), color=color.gray(0.5)) ## Transformed z plane
arrow(pos=vec(0,0,0), axis = vec(0,0,500), color=color.gray(0.5)) ## Transformed y plane



#initialize markers
balls = []

i = 0
for i in range(pos_data.shape[1]-2):
    
    if i % 3==0:
        ball = sphere(pos=vec(pos_data[0,i],pos_data[0,i+2],pos_data[0,i+1]), radius=20, color=(vec(1,1,1)+vec.random())/2 , make_trail = False, visible = True)
        balls.append(ball)

    i = i +1
    
  

#initialize pipes

join() 

makegraph()


#initialize forces
forces = []

force1 = arrow(pos=vector(forcepos[0,0],forcepos[0,2],forcepos[0,1]), axis=1.5*vector(force_data[0,0],force_data[0,2],force_data[0,1]), shaftwidth=50, color=color.red ,  visible = True)
forces.append(force1)

force2 = arrow(pos=vector(forcepos2[0,0],forcepos2[0,2],forcepos2[0,1]), axis=1.5*vector(force_data[12,0],force_data[12,2],force_data[12,1]), shaftwidth=50, color=color.blue ,  visible = True)
forces.append(force2)



rowPaused = 0
while True:
    rate(100)
    if not running: continue
    animate(rowPaused)


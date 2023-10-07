# Author: Fang K.
# Contact Me : kongf21@mails.tsinghua.edu.cn
import numpy as np

import os


def cmd_exec(cmd,mode=0):
  if mode:
    return os.popen(cmd).read()
  else:
    print(cmd)

'''
default find strings like:
_rlnImageName #1 
_rlnMicrographName #2 
_rlnCoordinateX #3 
_rlnCoordinateY #4 
_rlnAngleRot #5 
_rlnAngleTilt #6 
_rlnAnglePsi #7 

'''

def find_string(query_string,head_file='tmp_head'):
  find_cmd=" awk '{if ($1==\""+query_string+"\") print $2} ' "+head_file+" "
  return int(cmd_exec(find_cmd,1).split('#')[-1])



def make_head(filename):
  #starfile = open(filename)
  #print(filename)
 # sr = starfile.readline()
  star_head_cmd = "head -n 100 " + filename + " |grep -v mrc > tmp_head"

  cmd_exec(star_head_cmd, 1)
  start_line_cmd = 'head -n 100 ' + filename + ' |grep -v mrc |wc -l'
  start_line = int(cmd_exec(start_line_cmd, 1))
  #starfile.close()
  #print(start_line)
  return start_line


def get_content(filename):
  pass

def read_starfile(filename):
  start_line=make_head(filename)
  #print('start line index:',start_line)
  ang_rot=find_string('_rlnAngleRot')
  ang_tilt=find_string('_rlnAngleTilt')
 # print(ang_rot,ang_tilt)
 #  current_line=0
 #  starfile=open(filename)
 #  sr=starfile.read()
 #  lines=0
 #  while sr:
 #    if current_line<start_line:
 #      sr = starfile.readline()
 #      current_line+=1
 #      continue
 #    lines+=1
 #    sr = starfile.readline()
 #  print('total particles lines:',lines)
 #  starfile.close()
  starfile = open(filename)
  cd=[]

  sr = starfile.readline()
  coord_index=0
  current_line=0
  while sr:
    sp = sr.split(' ')
    if current_line<start_line:
      sr = starfile.readline()
      current_line+=1
      continue
    else:
      if (len(sp)>2):
        rot=float(sp[ang_rot-1])
        tilt=float(sp[ang_tilt-1])
        #print(rot,tilt)
        cd.append([rot,tilt,coord_index])
        #cd[coord_index]=[rot,tilt,coord_index]
        coord_index+=1
    sr = starfile.readline()

  starfile.close()
  return np.array(cd)


def make_groups(coords,group_size=60):
  groups=[]
  heads=[]
  Lrange=int(360/group_size)
  Srange=int(180/group_size)
  total_groups=Lrange*Srange
  for gi in range(total_groups):
    groups.append([])

  for line_index in range(len(coords)):
    coord=coords[line_index]
    L_index=int((coord[0]+180)/group_size)
    S_index=int(coord[1]/group_size)
    group_index=L_index*Srange+S_index
    groups[group_index].append((line_index,coord[0],coord[1]))

  return groups
  #
  # for groupi in range(len(groups)):
  #   print(len(groups[groupi]),'partiles in group',groupi)
  # print(groups)





"""
Command line tool to create tasks.txt, the description of how individual tracks are combined into tasks.
First argument is the number of tracks per task.
Second argument the number of tasks to include.
third argument is obj_data.txt. If omitted, it is assumed to lie in ./simulation/gazebo/skript_world/world/obj_data.txt
Example calls:
python3 create_tasks.py 4 5 > tasks.txt
python3 create_tasks.py 1 150 > tasks.txt
python3 create_tasks.py 1 150 ./test/obj_data.txt > tasks.txt
"""

import itertools ;
import sys ;

tracks_per_task = int(sys.argv[1]) ;
nr_tasks = int(sys.argv[2]) ;
datafile = "./simulation/gazebo/skript_world/world/obj_data.txt" if len(sys.argv) <= 3 else sys.argv[3] ;

# irrelevant now
colors = ["white","pink","red","green","blue"] ;
forms  = ["Sphere", "Cube", "D8", "Pyramide","Cylinder"] ;
symbols = ["X","A","O", "H", "Hash","plain"] ;

track_names = [l.strip().split(" ")[0].strip() for l in open(datafile,"r").readlines()]

tracks = [] ;
tasks_done = 0 ;

for i,new_track in enumerate(track_names):
  tracks.append(new_track) ;
  if i >= tracks_per_task:
    tracks = tracks[1:] ;
  if i >= tracks_per_task-1:
    loops = 1 ;
    for l in range(loops):
      for t in tracks: print(t, end = " ") ;
      print() ;
    tasks_done += 1 ;
    if tasks_done >= nr_tasks: break ;
 

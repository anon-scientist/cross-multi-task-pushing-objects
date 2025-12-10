"""
CRoSS benchmark suite, MLF  benchmarkExample for standalone use of provided
robot manager, without environment or RL framework
"""

import sys, numpy as np ;
from different_forms import define_robot_actions ;
from gazebo_sim.simulation import ThreePiManager ;
from gz.msgs10.color_pb2 import Color

world_name = 'Forschungsprojekt_world' ;
robot_name = '3pi_robot_with_front_cam' ;

actions = define_robot_actions() ;

env_config = {"observation_shape":[2,50,3],"tasks":None,"actions":actions,"robot_name": robot_name, "vehicle_prefix":'/vehicle',
                                       "lidar":'/vehicle/lidar',"world_name":"/world/" + world_name,"camera_topic":'/vehicle/camera', 
                                        "contact_topic":"/vehicle/contact_sensor"} ;

manager = ThreePiManager(env_config) ;

for i in range(0,10):
  print("Executing action", i%3) ;
  manager.gz_perform_action(actions[i%3]) ;


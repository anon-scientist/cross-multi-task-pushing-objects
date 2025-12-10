from gazebo_sim.learner import DQNLearner ;
import sys ;
import numpy as np ;

"""
This class allows some "hacks" for faster and more continual experiments for the Different-Forms-Scenario:
- the fake_inputs flag means that instead of the camera image, the environment creates population-coded arrays 
  for symbol, colro, form, distance to object, and viewing angle
- the external_steering flag ensures that the DNN only processes two actions: stop(0) and  "determine forward direction by external steering"(1).
  Basically, in the latter case the DNN can decide whether we stop, or we continue. The idrecition is not determined byt he DNN but by a 
  non-adaptive controller. Upshot is that a) properties of the object are available directly and invariantzly, without processing vision input
  and b) steering towards the object will happen automatically for all tasks, making the problem much simpler
- we can have three valid combinations: fake_inputs == "yes", external_steering == "yes"|"no" and fake_input =="no", external_steering=="no"
  The latter case is the case with no manipulations whatsoeverm so just full DNN control based on plain camera image
- if we have external steering, we assume that only a few of the DNN outputs are meaningful, the oethers are ignored and receive target values of 0 in learning.
"""

def handle_fake_input_and_external_control_for_block_pushing(observation, randomly_chosen, model):
      # erase angle popcode from observation
      # in this case, the DNN can just output two actions: stop(0) and continue(1). Just call the superclass method for exploration!
      # if this action is chosen by exploratrion --> create a 50/50 choice between stop and go
      # returns  full action idx, simplied action  idx, explorationFlag, q_pred (simplified)

      observation, steering_guide = erase_angle_information(observation) ;
      print("!Angle steering_guide", steering_guide) ;
      simplified_action = None ;
      q_pred = (model(np.array([observation]))[0][0:2]) ;
      if randomly_chosen == True:
        simplified_action = np.random.choice([0,1]) ;
      # Otherwise, it was chosen by the model, and the relevant part needs to be cut out of the model output
      else:
        simplified_action = np.argmax(q_pred) ;

      full_action = transform_simplified_to_full_action(simplified_action, steering_guide) ;
      return full_action, simplified_action, randomly_chosen, q_pred ;


class ModifiedDQNLearner(DQNLearner):

  def __init__(self, n_actions, obs_space, config, **kwargs):
    self.config, _ = self.parse_args(**kwargs) ;
    print("EXTERNAL!", self.config.external_steering) ;
    if self.config.external_steering == "yes":
      DQNLearner.__init__(self, 2, obs_space, config, **kwargs) ;
    else:
      DQNLearner.__init__(self, n_actions, obs_space, config, **kwargs) ;    

    if self.config.external_steering == "yes" and self.config.output_size != 2:
      print("External steering xannot be used with output_size != 2") ;
      sys.exit(0) ;

    if self.config.external_steering == "no" and self.config.output_size == 2:
      print("Normal steering cannot be used with output_size == 2") ;
      sys.exit(0) ;


    # do consistency checks for new params
    # see error message!
    if self.config.external_steering == "yes" and self.config.fake_inputs == "no":
      print("External steering xannot be used with real inputs!!") ;
      sys.exit(0) ;


  # new steering option: extrinsic --> left/right/straight steering is done by non-learning controller
  # only stop/continue decision is taken by trainable system based on color, form, symbol + dist popcodes
  def choose_action(self, observation):
    if self.config.external_steering == "yes": # in that case, self.fake_inputs == "yes" is assured by the constructor
      randomly_chosen = self.get_exploration_controller().query() ;
      full_action, simplified_action, randomly_chosen, q_pred = handle_fake_input_and_external_control_for_block_pushing(observation, randomly_chosen, self.model)
      return full_action, randomly_chosen ;
    else:
      return DQNLearner.choose_action(self, observation) ;

  def store_transition(self, state, action, reward, new_state, done):
    if self.config.external_steering == "yes":
      DQNLearner.store_transition(self, state, transform_full_to_simplified_action(action), reward, new_state, done) ;
    else:
      DQNLearner.store_transition(self, state, action, reward, new_state, done) ;


  def define_base_args(self, parser):
    DQNLearner.define_base_args(self, parser) ;
    parser.add_argument("--fake_inputs", type = str, required = False, default = "no") ;
    parser.add_argument("--external_steering", type = str, required = False, default = "no") ;

  # This is called during learning, after having drawn a batch of transitions from the replay buffer
  # Here, we post-process these transitions: 1) erase angle representation from fake inputs (taken care of by automatic steering)
  # and 2) re-code targets to 0 (stop) and 1(continue)
  """
  def post_process_buffer(self, states, actions, rewards, states_, terminal):
    if self.config.fake_inputs == "yes":
      if self.config.external_steering == "yes":
        #states[:,2,:] = 0.0 ; # erase angle popcode, do we need to do that really?
        # re-code actions so as to give the right popcodes target values for DNN
        actions[:] = np.array([(0 if a == 0 else 1) for a in actions]) ;
  """





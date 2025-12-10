#!/bin/bash
# first parameter: base path
# Typically, start with 
# source main.bash $(pwd)/.. 
#
PROCESSES=(
    "gz.*sim"
    "different_forms.sdf"
    "gazebo_simulator"
    "Experiment.py"
    "ruby"
    "gz"
)



function print_message {
    echo ${3}
}

function print_info { print_message "BLUE"   "INFO" "${*}" ; }
function print_warn { print_message "YELLOW" "WARN" "${*}" ; }
function print_ok   { print_message "GREEN"  "OK"   "${*}" ; }
function print_err  { print_message "RED"    "ERR"  "${*}" ; }
function print_part { print_message "CYAN"   "PART" "${*}" ; }
function print_unk  { print_message "PURPLE" "UNK"  "${*}" ; }


function check_process {
    pgrep -f "${1}"
}


function eval_state {
    local state=$?

    if (( $state == 0 ))
        then print_ok "success ${1}"
        else print_err "failed ${1}"
    fi

    return $state
}


function kill_process {
    pkill -9 -f "${1}"
}


function execute_check {
    print_info "check process ${entry}"
    eval_state $(check_process "${entry}")
}

function execute_kill {
    print_info "try to kill ${entry}"
    eval_state $(kill_process "${entry}")
}

function execute_watchout {
    print_info "watchout for possible zombies"
    for entry in ${PROCESSES[@]}
    do
        execute_check &&
        execute_kill
    done
}

function execute_state {
    state=$?
    if (( $state == 0 ))
        then print_ok "success (${1})"
        else print_err "failed (${1})"
    fi
    return $state
}

# *------------ COMMON DEFINITIONS ----------------------

if [ "$#" == "1" ] ; then
SRC_PATH=${1} ;
else
SRC_PATH="./../" ;
fi
PROJECT_DIR=different-forms-scenario


WORLD_DIR="/simulation/gazebo/skript_world/world"
ROOT_PATH="${SRC_PATH}/${PROJECT_DIR}"
WORLD_PATH="${SRC_PATH}/${PROJECT_DIR}/${WORLD_DIR}"
OBJ_DATA="${WORLD_PATH}/obj_data.txt"
ICRL_PATH="${SRC_PATH}/icrl"
# *-------------------------------------------------------

# PYTHONPATH - PYTHONPATH - PYTHONPATH --------------------------------
export PYTHONPATH=$PYTHONPATH:${ROOT_PATH}/src
export PYTHONPATH=$PYTHONPATH:${SRC_PATH}/cl_experiment/src
export PYTHONPATH=$PYTHONPATH:${SRC_PATH}/icrl/src
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/lib/x86_64-linux-gnu/
# *--------------------------------------------------------------------

# GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ
export GZ_VERSION="8"
export GZ_DISTRO="harmonic"
export GZ_IP="127.0.0.1"
export GZ_PARTITION="$(hostname)"
export GZ_TRANSPORT_RCVHWM=10
export GZ_TRANSPORT_SNDHWM=10
export GZ_TRANSPORT_LOG_SQL_PATH="~/.gz/"
export GZ_SIM_RESOURCE_PATH="${GZ_SIM_RESOURCE_PATH}:${ROOT_PATH}/models:${WORLD_PATH}:${ICRL_PATH}/models"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ - GZ

# kill zombies
execute_watchout

# start gazebo without GUI
sim_options=" -v 4 -r -s --headless-rendering --render-engine ogre2"
# start Gazebo with GUI
#sim_options=" -v 4 -r --render-engine ogre2"
gz sim ${sim_options} "${WORLD_PATH}/different_forms.sdf"  &

# +++
python3 -m different_forms.Experiment                                                                                         \
        --benchmark mydf \
        --debug_port                                        11001                                                           \
        --seed                                              42                                                              \
        --exp_id                                            DF-DQN                                                          \
        --root_dir                                          "${ROOT_PATH}"                                                  \
        --obs_per_sec_sim_time                              15                                                              \
        --task_list                                         0,0 \
        --training_duration                                 5000                                                             \
        --evaluation_duration                               20                                                              \
        --training_duration_unit                            timesteps                                                        \
        --evaluation_duration_unit                          episodes                                                        \
        --max_steps_per_episode                             30                                                            \
        --start_task                                        0                                                               \
        --eval_start_task                                   0                                                               \
        --exploration_start_task                            0 \
        --training_duration_task_0                          5000                                                           \
        --fake_inputs                                       yes \
        --external_steering                                 yes \
        --gamma                                             0.9                                                             \
        --train_batch_size                                  100                                                              \
        --learner_params ............................................................................................ \
        --algorithm                                         DQN                                                             \
        --dqn_fc1_dims                                      128                                                             \
        --dqn_fc2_dims                                      64                                                              \
        --dqn_adam_lr                                       1e-4                                                            \
        --dqn_dueling                                       no                                                              \
        --dqn_target_network                                yes                                                             \
        --dqn_target_network_update_freq                    200                                                             \
        --output_size                                       2                                                                \
        --exploration                                       eps-greedy                                                      \
        --initial_epsilon                                   1.0                                                             \
        --final_epsilon                                     0.2                                                           \
        --epsilon_delta                                     0.0002                                                          \
        --eps_replay_factor                                 0.8                                                             \
        --replay_buffer                                     default                                                         \
        --capacity                                          3000                                                            \
        --debug no \
        ; execute_state "Experiment"
# ---

echo DONE

# kill zombies
execute_watchout

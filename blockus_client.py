import numpy as np
import random
from sys import stdout
from spacetimerl.client_network_env import ClientNetworkEnv
from blockus_env import BlockusEnv, start_gui, display_board, terminate_gui, action_to_string
import gui
import ai

params = {
    "hostname": 'localhost',
    "port": 7777,
    "player_name_base": "best+plaer"
}

# Blocks until game starts
env = ClientNetworkEnv(server_hostname=params["hostname"],
                       port=params['port'],
                       player_name="{}_{}".format(params['player_name_base'], random.randint(0, 1024)))

# Wait for first obervation to be ready
obs = env.get_first_observation()

print("obs: {}".format(obs))

print("hi")
start_gui()

print("bye")

while True:
    player_number = obs['player'][0]
    state = env.get_server_state()[-1]
    _, state = BlockusEnv.unserialize_state(state)
    board, round_count, players = state

    display_board(state, player_number, None)  # change none later to winners
    display_board(state, player_number, None)  # change none later to winners

    player = players[player_number]

    print("round count: {}".format(round_count))
    all_valid_moves = player.collect_moves(board, round_count)
    print("All possible moves for you: {}".format(all_valid_moves))
    # input('press enter to play random move:')

    if len(all_valid_moves.keys()) != 0:
        random_indexes = random.sample(all_valid_moves.items(), 1)
        piece_type = random_indexes[0][0]
        index = list(all_valid_moves[piece_type].keys())[0]
        orientation = all_valid_moves[piece_type][index][0]

        string_action = action_to_string(piece_type, index, orientation)
    else:
        string_action = ""

    print("action: {}".format(string_action))

    obs, reward, terminal, winners = env.step(string_action)
    if terminal:
        print("done")
        break

# all_valid_moves = ai.collect_moves(round_count)
terminate_gui()

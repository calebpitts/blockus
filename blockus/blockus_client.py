from .blockus_env import BlockusEnv, BlockusClientEnv, start_gui, terminate_gui, action_to_string
from spacetimerl.rl_logging import init_logging
from spacetimerl.client_environment import RLApp, ClientEnv
import random

import time
import numpy as np


@RLApp("localhost", 7777, client_environment=BlockusClientEnv, server_environment=BlockusEnv)
def main(ce: BlockusClientEnv):
    logger = init_logging()

    player_num = ce.connect("player_{}".format(np.random.randint(0, 1024)))
    logger.debug("First observation: {}".format(ce.wait_for_turn()))
    winners = None

    while True:
        ce.render(ce.full_state, player_num, winners)

        action = BlockusClientEnv.random_valid_action_string(state=ce.full_state, player_num=player_num)

        new_obs, reward, terminal, winners = ce.step(str(action))


        logger.debug("Took step with action {}, got: {}".format(action, (new_obs, reward, terminal, winners)))
        if terminal:
            logger.info("Game is over. Players {} won".format(winners))
            break


if __name__ == '__main__':
    main()

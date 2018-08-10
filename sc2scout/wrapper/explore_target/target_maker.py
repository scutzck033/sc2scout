from sc2scout.wrapper.explore_enemy.zerg_scout_wrapper import ZergScoutWrapper
from sc2scout.wrapper.evade_enemy.evade_act_wrapper import EvadeActWrapper
from sc2scout.wrapper.explore_target.target_terminal_wrapper import TargetTerminalWrapper
from sc2scout.wrapper.explore_target.target_rwd_wrapper import ExploreTargetRwdWrapper
from sc2scout.wrapper.explore_target.target_obs_wrapper import TargetObsWrapper
from sc2scout.wrapper.wrapper_factory import WrapperMaker

from baselines import deepq

class TargetMakerV1(WrapperMaker):
    def __init__(self):
        super(TargetMakerV1, self).__init__('target_v1')

    def make_wrapper(self, env):
        if env is None:
            raise Exception('input env is None')
        env = EvadeActWrapper(env)
        env = TargetTerminalWrapper(env, 128, 48, 100)
        env = ExploreTargetRwdWrapper(env, 128, 48, 100)
        env = TargetObsWrapper(env, 128, 48, 100)
        env = ZergScoutWrapper(env)
        return env

    def model_wrapper(self):
        return deepq.models.cnn_to_mlp(
            convs=[(32, 8, 4), (64, 4, 2), (64, 3, 1)],
            hiddens=[256, 128])


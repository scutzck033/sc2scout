from sc2scout.wrapper.explore_enemy.zerg_scout_wrapper import ZergScoutWrapper
from sc2scout.wrapper.evade_enemy.evade_act_wrapper import EvadeActWrapper
from sc2scout.wrapper.explore_target_curran.target_terminal_curran_wrapper import TargetTerminalWrapperC1
from sc2scout.wrapper.explore_target_curran.target_rwd_curran_wrapper import ExploreTargetRwdWrapperC1
from sc2scout.wrapper.explore_target_curran.target_obs_curran_wrapper import TargetObsWrapperC1
from sc2scout.wrapper.wrapper_factory import WrapperMaker

from baselines import deepq

class TargetMakerC1(WrapperMaker):
    def __init__(self):
        super(TargetMakerC1, self).__init__('target_c1')

    def make_wrapper(self, env):
        if env is None:
            raise Exception('input env is None')
        env = EvadeActWrapper(env)
        env = TargetTerminalWrapperC1(env, 32, 12, 400)
        env = ExploreTargetRwdWrapperC1(env, 32, 12, 400)
        env = TargetObsWrapperC1(env, 32, 12, 400)
        env = ZergScoutWrapper(env)
        return env

    def model_wrapper(self):
        pass



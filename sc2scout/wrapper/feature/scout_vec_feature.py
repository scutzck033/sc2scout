from gym.spaces import Box
from sc2scout.wrapper.feature.feature_extractor import FeatureExtractor

SCOUT_IN_RANGE = 1
SCOUT_OUT_RANGE = 0

class ScoutVecFeature(FeatureExtractor):
    def __init__(self):
        super(ScoutAvoidImgFeature, self).__init__()
        self._dest = None
        self._src = None
        self._reverse = False
        self._map_size = None

    def reset(self, env):
        self._dest = DestRange(env.unwrapped.enemy_base())
        self._src = DestRange(env.unwrapped.owner_base())
        self._map_size = self.env.unwrapped.map_size()
        self._reverse = self.judge_reverse(env)

    def obs_space(self):
        low = np.zeros(8)
        high = np.ones(8)
        return Box(low, high)

    def extract(self, env, obs):
        scout = env.unwrapped.scout()
        scout_raw_pos = (scout.float_attr.pos_x, scout.float_attr.pos_y)
        scout_pos = self._pos_transfer(scout_raw_pos)
        home_pos = self._pos_transfer(env.unwrapped.owner_base())
        enemy_pos = self._pos_transfer(env.unwrapped.enemy_base())

        features = []
        features.append(float(scout_pos[0]) / self._map_size[0])
        features.append(float(scout_pos[1]) / self._map_size[1])
        features.append(float(home_pos[0]) / self._map_size[0])
        features.append(float(home_pos[1]) / self._map_size[1])
        features.append(float(enemy_pos[0]) / self._map_size[0])
        features.append(float(enemy_pos[1]) / self._map_size[1])

        if self._dest.in_range(scout_raw_pos):
            features.append(float(1))
        else:
            features.append(float(0))

        if self._src.in_range(scout_raw_pos):
            features.append(float(1))
        else:
            features.append(float(0))

        return features

    def _judge_reverse(self, env):
        scout = self.env.unwrapped.scout()
        if scout.float_attr.pos_x < scout.float_attr.pos_y:
            return False
        else:
            return True

    def _pos_transfer(self, x, y):
        if not self._reverse:
            return (x, y)
        cx = self._map_size[0] / 2
        cy = self._map_size[1] / 2
        pos_x = 0.0
        pos_y = 0.0
        if x > cx:
            pos_x = cx - abs(x - cx)
        else:
            pos_x = cx + abs(x - cx)

        if y > cy:
            pos_y = cy - abs(y - cy)
        else:
            pos_y = cy + abs(y - cy)

        return (pos_x, pos_y)

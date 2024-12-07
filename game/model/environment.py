import numpy as np
from scipy.signal import convolve2d

class Environment:
    def __init__(self, dim: tuple[int, int]) -> None:
        self.dim = dim
        self.state = np.zeros((dim[0], dim[1]))
        self.rows = np.zeros(dim[0], dtype=int)
        self.count = 0
        self.turns = [1 if _%2==0 else 2 for _ in range(42)]
        self.last_play = {1:None, 2:None}
        self.kernels = [np.array([[ 1, 1, 1, 1]]), np.array([[ 1, 1, 1, 1]]).T, np.eye(4), np.fliplr(np.eye(4))]

    def get_rows(self) -> np.ndarray:
        return self.rows.copy()
    
    def get_turn(self) -> int:
        return self.turns.copy()[self.count]

    def get_last(self) -> dict:
        return self.last_play.copy()

    def get_state(self) -> np.ndarray:
        return self.state.copy()
    
    def update_state(self, new_state: np.ndarray) -> None:
        self.state = new_state

    def get_possible_actions(self) -> np.ndarray:
        actions = np.where(self.rows<self.dim[1], True, False)
        return actions
    
    def preview_action(self, action: int) -> np.ndarray:
        state = self.get_state()
        actions = self.get_possible_actions()

        if actions[action]:
            state[action, self.rows[action]] = self.get_turn()
        else:
            return None

        return state
    
    def do_action(self, action: int) -> bool:
        state = self.preview_action(action)

        if type(state) == np.ndarray:
            self.update_state(state)

            player = self.get_turn()
            reward = self.reward(state)
            self.last_play.update({player: (state, action, reward)})
            
            self.rows[action] += 1
            self.count +=1

            return False
        return True

    def reset(self) -> None:
        self.count = 0
        self.state = np.zeros((self.dim[0], self.dim[1]))
        self.rows = np.zeros(self.dim[0], dtype=int)
        self.last_play = {1:None, 2:None}

    def filter_player_state(self, state: np.ndarray, player: int) -> np.ndarray:
        filtered = np.where(state==player, 1, 0)
        return filtered
    
    def reward(self, state: np.ndarray) -> float:
        
        if type(state) != type(None):
            player_state = self.filter_player_state(state, self.turns[self.count])
            reward = 0
            for kernel in self.kernels:
                filtered = convolve2d(player_state, kernel, mode="valid")
                reward += np.sum(filtered)
        else:
            return None
        return reward

    def check_win(self, player: int) -> bool:
        state = self.filter_player_state(self.state, player)

        for kernel in self.kernels:
            if (convolve2d(state, kernel, mode="valid") == 4).any():
                return True
        return False

    def is_terminal(self) -> int:
        if self.check_win(1):
            return "Winner Player 1"
        elif self.check_win(2):
            return "Winner Player 2"
        elif self.count==41:
            return "Tie"
        return False

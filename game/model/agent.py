import numpy as np
from random import random, choice
from game.database import DataBase

class Agent:
    TABLE = None

    def __init__(self, qtable: DataBase, epsilon:float=0.9, gamma:float=0.9, alpha:float=0.5) -> None:
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.table = qtable
    
    def state_to_key(self, state: np.ndarray) -> str:
        key = "".join(str(box) for box in state.flatten())
        return key
    
    def get_value(self, state: np.ndarray, action: int) -> float:
        state = self.state_to_key(state)

        request = {"table": self.TABLE,
                   "state": state,
                   "action": str(action)}
        
        row = self.table.get_value(request)
        value = row[0][2] if row else 0
        return value
    
    def set_value(self, state: np.ndarray, action: int, reward: float) -> None:
        state = self.state_to_key(state)

        request = {"table": self.TABLE,
                   "state": state,
                   "action": str(action),
                   "reward": str(reward)}
        
        if not self.table.get_value(request):
            self.table.update(request)
        else:
            self.table.insert(request)
    
    def choose_action(self, state: np.ndarray, actions: list[int]) -> int:
        if random() < self.epsilon:
            return choice(actions)
        return self.best_action(state, actions)
    
    def update_values(self, state: np.ndarray, action: int, reward: float, next: dict) -> None:
        pass

    def best_action(self, state: np.ndarray, actions: list[int]) -> int:
        values = [self.get_value(state, action) for action in actions]

        max_q = max(values)
        actions_with_max_q = [a for a, q in enumerate(values) if q == max_q]
        return choice(actions_with_max_q)

from game.model.agent import *

class QLearning(Agent):
    TABLE = "qlearning"
    
    def update_values(self, state:np.ndarray, action: int, reward: float, next: dict) -> None:

        """
        Compute and update the q-values for the current state, action following the bellman equation for the q-learning algorithm.

        Parameters:
            - state (np.ndarray):
                Board current state as numpy array.

            - action (int):
                Selected action by the agent.

            - reward (float):
                Reward obtained from doing the action in the current state.

            - next (dict):
                Dictionary storing the state after making the action and the possible action in that state.

        Returns:
            - None 
        
        """

        action_p = self.best_action(next["state"], next["actions"])
        Q_p = self.get_value(next["state"], action_p)
        
        Q = self.get_value(state, action)
        Q += self.alpha*(reward + self.gamma*Q_p - Q)
        
        self.set_value(state, action, Q)
from game.model.environment import *

class Board:
    def __init__(self, dim: tuple[int, int] = (7, 6)) -> None:
        self.env = Environment(dim)
        self.players = None

    def set_players(self, players):
        self.players = players

    def get_rows(self):
        return self.env.get_rows()

    def get_turn(self):
        return self.env.get_turn()
    
    def is_human(self):
        if self.players:
            return self.players[self.get_turn()] == "Human"
    
    def get_possible_actions(self) -> list[int]:
        return self.env.get_possible_actions()    

    def do_player_action(self, action) -> bool:
        return self.env.do_action(action)

    def do_agent_action(self, player: int, agents: dict) -> None:
        actions = self.get_possible_actions()
        next = {"state": self.env.get_state()}
        next["actions"] = [action for action in range(self.env.dim[0]) if actions[action]]
        next["action"] = agents[self.players[player]].choose_action(next["state"], next["actions"])

        last_play = self.env.get_last()
        if last_play[player]:
            state = last_play[player][0]
            action = last_play[player][1]
            reward = last_play[player][2]
 
            agents[self.players[player]].update_values(state, action, reward, next)
        
        self.env.do_action(next["action"])
        return next["action"]

    def is_terminal(self):
        return self.env.is_terminal()

class QTable:
    def __init__(self, dim: tuple[int, int]=(7, 6)):
        self.env = Environment(dim)
        self.dim = dim

    def get_rows(self):
        return self.env.get_rows()
    
    def get_turn(self):
        return self.env.get_turn()

    def get_possible_actions(self) -> list[int]:
        return self.env.get_possible_actions()

    def get_values(self, agent):
        actions = self.env.get_possible_actions()
        actions = [action for action in range(self.dim[0]) if actions[action]]

        state = self.env.get_state()
        values = {}

        rows = self.env.get_rows()

        if not (agent is None):
            values = {action: (rows[action], agent.get_value(state, action)) for action in actions}
        else:
            values = {action: (rows[action], 0) for action in range(7)}
        return values

    def do_action(self, action: int):
        return self.env.do_action(action)

    def is_terminal(self):
        return self.env.is_terminal()

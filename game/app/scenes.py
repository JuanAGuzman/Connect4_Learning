from game.app.elements import *
from game.board import Board, QTable

from game.agents.sarsa import SARSA
from game.agents.qlearning import QLearning

from game.database import DataBase

white = (255, 255, 255)

qtable = DataBase("game//agents//qtable//qtable.db")
agents = {"SARSA": SARSA(qtable),
          "Q-Learning": QLearning(qtable)}

class Scene:
    def __init__(self):
        self.running = True

    def read_event(self, event: pygame.event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def get(self) -> str:
        return self.__class__.__name__

    def get_players(self):
        pass

    def set_players(self, players):
        pass

    def get_winner(self):
        pass

    def set_winner(self, winner):
        pass

class MenuScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.params = {}

    def draw(self) -> None:
        self.screen.fill(pygame.Color("black"))
        texts = {"PLAY": (480, 128),
                 "Q-TABLES": (480, 256),
                 "CREDITS": (480, 384),
                 "QUIT": (480, 512)}
        
        for text, pos in texts.items():
            self.params.update({text: [pos, Text(text, 32, pos).draw(self.screen)]})


    def run(self, events: list) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for scene in self.params:
                    self.game_manager.set_state(MenuButton(self.params, scene).action(event))


class CreditScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.test = None

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        Text("Developed by:", 48, (480, 160)).draw(self.screen)
        Text("Juan Andres Guzman Pineda", 58, (480, 360)).draw(self.screen)

    def run(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_manager.set_state("Menu")
            

class QtableScene(Scene):
    COLORS = {1: "red", 2: "blue"}
    COLUMNS = [(374,432), (452,512), (532,590), (610,670), (690,748), (770,828), (848, 904)]

    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.board = QTable()
        self.board_image = BoardImage()
        self.counters = []
        self.winner = None
        self.params = {}
        self.selected = [None, None]
        self.tempText = ""
        self.values = {}
        self.agent = None

    def get_turn(self) -> int:
        return self.board.get_turn()
    
    def get_row(self, column: int) -> int:
        return self.board.get_rows()[column]

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        self.screen.blit(self.board_image.image, self.board_image.rect)
        for counter in self.counters:
            counter.draw(self.screen)

        texts = {"SARSA": 240, "Q-Learning": 360}

        for text, pos in texts.items():
            self.params.update({text: [(150, pos), Text(text, 24, (150, pos)).draw(self.screen)]})

        for action, values in self.values.items():
            row, value = values
            if row<5:
                pos = (CounterImage.COLUMN_CENTER[action], CounterImage.ROW_CENTER[5-row])
                ValueText(str(value), 20, pos).draw(self.screen)

        Text(self.tempText, 24, (150, 160)).draw(self.screen)
        Text("Export CSV", 24, (150, 500)).draw(self.screen)
        PlayerButton(*self.selected).draw(self.screen)

    def run(self, events):
        check = lambda event, pos, size, i: pos[i] - size[i]/2 <= event.pos[i] <= pos[i] + size[i]/2
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, value in self.params.items():
                    pos, size = value
                    if check(event, pos, size, 0) and check(event, pos, size, 1):
                        self.selected = [(pos[0] - size[0]/2 - 5, pos[1]-size[1]/2 + 2), (size[0]+8, size[1])]
                        self.agent = key
                if check(event, (150, 500), (160, 60), 0) and check(event, (150, 500), (160, 60), 1):
                    if self.agent:
                        self.export_csv()

                self.play(event)
                if self.agent:
                    self.values = self.board.get_values(agents[self.agent])
        
        if self.board.is_terminal():
                self.winner = self.board.is_terminal()
                self.game_manager.set_state("QTableEnd", winner = self.winner)
                self.reset()

    def play(self, event):
        check = lambda pos: [index for index in range(7) if self.COLUMNS[index][0]<=pos[0]<=self.COLUMNS[index][1]]
        
        if check(event.pos):
            column = check(event.pos)[0]
            row = self.get_row(column)

            if self.board.do_action(column):
                self.tempText = "Invalid Action"
            else:
                self.counters.append(CounterImage(self.COLORS[self.get_turn()], column, row))
                self.tempText = "Played Successfully"

    def reset(self):
        self.board = QTable()
        self.board_image = BoardImage()
        self.counters = []
        self.winner = None
        self.params = {}
        self.selected = [None, None]
        self.tempText = ""
        self.values = {}

    def export_csv(self):
        pd = __import__("pandas")
        agent = {"SARSA":"sarsa",
                 "Q-Learning": "qlearning"}
        qvalues = pd.read_sql_query(f"SELECT * FROM {agent[self.agent]}", qtable.connection)
        qvalues.to_csv(f'game//agents//qtable//{agent[self.agent]}.csv', index=False)

class QTableEndScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.winner = None
        self.params = {}
        
    def draw(self):
        self.screen.fill(pygame.Color("black"))
        texts = {"MENU": (480, 300),
                 "TRY AGAIN": (480, 400),
                 "QUIT": (480, 500)}
        if self.winner:
            Text(self.winner, 60, (480, 180)).draw(self.screen)

        for text, pos in texts.items():
            self.params.update({text: [pos, Text(text, 24, pos).draw(self.screen)]})

    def run(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for scene in self.params:
                    self.game_manager.set_state(MenuButton(self.params, scene).action(event))

    def set_winner(self, winner):
        self.winner = winner


class PlayerScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.params = {}
        self.selected = {320: [None, None], 640: [None, None]}
        self.next = None
        self.players = {}

    def draw(self) -> None:
        self.screen.fill(pygame.Color("black"))
        columns = [320, 640]
        texts = {"Human": 256, "SARSA": 384, "Q-Learning": 512}

        Text("PLAYER 1", 40, (320, 128)).draw(self.screen)
        Text("PLAYER 2", 40, (640, 128)).draw(self.screen)

        for column in columns:
            for text, pos in texts.items():
                self.params.update({(text, column): [(column, pos), Text(text, 24, (column, pos)).draw(self.screen)]})

        for param in self.selected.values():
            PlayerButton(*param).draw(self.screen)

        if all(self.selected[320]) and all(self.selected[640]):
            self.next = Text("NEXT", 20, (900, 600)).draw(self.screen)

    def run(self, events) -> None:
        check = lambda event, pos, size, i: pos[i] - size[i]/2 <= event.pos[i] <= pos[i] + size[i]/2

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, value in self.params.items():
                    pos, size = value
                    if check(event, pos, size, 0) and check(event, pos, size, 1):
                        self.selected[key[1]] = [(pos[0] - size[0]/2 - 5, pos[1]-size[1]/2 + 2), (size[0]+8, size[1])]
                        if key[1]==320:
                            self.players[1] = key[0]
                        elif key[1]==640:
                            self.players[2] = key[0]
            
                pos = (900, 600)
                size = self.next
                if size:
                    if check(event, pos, size, 0) and check(event, pos, size, 1):
                        self.game_manager.set_state("Play", players = self.get_players())
                        self.reset()

    def get_players(self) -> dict:
        return self.players.copy()
    
    def reset(self):
        self.params = {}
        self.selected = {320: [None, None], 640: [None, None]}
        self.next = None
        self.players = {}

class PlayScene(Scene):
    COLORS = {1: "red", 2: "blue"}
    COLUMNS = [(374,432), (452,512), (532,590), (610,670), (690,748), (770,828), (848, 904)]

    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.board = Board()
        self.board_image = BoardImage()
        self.counters = []
        self.turnText = "Welcome"
        self.winner = None

    def get_turn(self) -> int:
        return self.board.get_turn()
    
    def get_row(self, column: int) -> int:
        return self.board.get_rows()[column]

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        self.screen.blit(self.board_image.image, self.board_image.rect)
        for counter in self.counters:
            counter.draw(self.screen)

        Text(self.turnText, 24, (120, 240)).draw(self.screen)

    def run(self, events):
        for event in events:
            if self.board.is_human():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.play(event)

        if not self.board.is_human():
            column = self.board.do_agent_action(self.get_turn(), agents)
            row = self.get_row(column)-1
            self.counters.append(CounterImage(self.COLORS[self.get_turn()], column, row))
            self.turnText = f"Player {self.get_turn()} turn"
            
        if self.board.is_terminal():
                self.winner = self.board.is_terminal()
                self.game_manager.set_state("End", winner = self.winner)
                self.reset()

    def play(self, event):
        check = lambda pos: [index for index in range(7) if self.COLUMNS[index][0]<=pos[0]<=self.COLUMNS[index][1]]
        
        if check(event.pos):
            column = check(event.pos)[0]
            row = self.get_row(column)            

            if self.board.do_player_action(column):
                self.turnText = "Try again"

            else:
                self.counters.append(CounterImage(self.COLORS[self.get_turn()], column, row))
                self.turnText = f"Player {self.get_turn()} turn"

    def set_players(self, players):
        self.board.set_players(players)

    def change_turn(self, turn):
        self.turn = turn

    def reset(self):
        self.counters = []
        self.board = Board()
        self.turnText = "Welcome"

class EndScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.winner = None
        self.params = {}
        

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        texts = {"MENU": (480, 300),
                 "PLAY AGAIN": (480, 400),
                 "QUIT": (480, 500)}
        if self.winner:
            Text(self.winner, 60, (480, 180)).draw(self.screen)

        for text, pos in texts.items():
            self.params.update({text: [pos, Text(text, 24, pos).draw(self.screen)]})

    def run(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for scene in self.params:
                    self.game_manager.set_state(MenuButton(self.params, scene).action(event))

    def set_winner(self, winner):
        self.winner = winner

class QuitScene(Scene):
    def __init__(self, screen, game_manager):
        Scene.__init__(self)
        self.screen = screen
        self.game_manager = game_manager
        self.running = False

    def run(self, events):
        qtable.commit()
        qtable.close()


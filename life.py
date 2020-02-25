from world import World
from cell import Cell
import time
import toolbox

class Life(object):

    def __init__(self):
        self.__world = World(34, 66)
        self.__fillrate = 25
        self.__delay = 0.5
        self.random()

    def main(self):
        """Main event loop for store."""
        command = 'help'
        parameter = None
        while command != 'quit':
            #if command == 'help':
             #   self.help('help.txt', 'Press <return> to continue.')
              #  print(self.__world, end="")
               # print(self.status() + '\n' + self.menu(), end=' ')
            if command == 'next generation':
                self.next_generation(parameter)
            elif command == 'run simulation':
                self.run_simulation(parameter)
            elif command == 'skip generations':
                self.skip_generations(parameter)
            elif command == 'random world':
                self.random()
            elif command == 'change fillrate':
                self.change_fillrate(parameter)
            elif command == 'change delay':
                self.change_delay(parameter)
            elif command == 'change size':
                self.change_size(parameter)
            elif command == 'change display':
                self.change_display(parameter)
            elif command == 'long l world':
                self.long_l_world()
            elif command == 'acorn world':
                self.acorn_world()
            command, parameter = self.get_command()
            print("I'm gay")
        print('goodbye')

    def menu(self):
        """returns a string containing the menu."""
        return '[N]ext  [R]un   s[K]ip   n[E]w   [F]illrate   [D]elay   [S]ize   d[I]splay   [L]ong l   [A]corn   [H]elp   [Q]uit'

    def get_command(self):
        """Get a valid command from the user."""
        commands = {'n': 'next generation',
                    'r': 'run simulation',
                    'k': 'skip generations',
                    'e': 'random world',
                    'f': 'change fillrate',
                    'd': 'change delay',
                    's': 'change size',
                    'i': 'change display',
                    'l': 'long l world',
                    'a': 'acorn world',
                    'h': 'help',
                    '?': 'help',
                    'q': 'quit'}

        validCommands = commands.keys()

        userInput = '&'
        parameter = None
        while userInput[0].lower() not in validCommands:
            userInput = input()
            if userInput == '':
                userInput = 'n'
                parameter = 1
        command = commands[userInput[0].lower()]
        if len(userInput) > 1:
            parameter = userInput[1:].strip()
        return command, parameter

    def status(self):
        """Returns a string representing the status of the world."""
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        percentAlive = (self.__world.get_living_cell_count() / (rows * columns)) * 100
        string = 'Status:   '
        string += f'size:[{rows}x{columns}]   '
        string += f'alive: {percentAlive:0.0f}%   '
        return string

    def help(self, filename, prompt = None):
        """Displays instructions."""
        with open(filename, 'r') as file:
            help = file.read()
        print(help, end='')
        if prompt:
            input('\n'+prompt)

    def next_generation(self, parameter):
        """Displays the next generation of the world"""
        self.__world.next_generation()
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end = ' ')

    def run_simulation(self, parameter):
        """Displays the next generation of the world"""
        if toolbox.is_integer(parameter) and int(parameter) > 0:
            generations = int(parameter)
        else:
            prompt = 'How many generations would you like to simulate?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        for generation in range(generations):
            self.__world.next_generation()
            string = self.__world.__str__()
            string += self.status()
            string += f'left: {generations - generation}'
            print(string)
            time.sleep(self.__delay)
        print(self.menu(), end=' ')

    def skip_generations(self, parameter):
        """Displays the next generation of the world"""
        if toolbox.is_integer(parameter) and int(parameter) > 0:
            generations = int(parameter)
        else:
            prompt = 'How many generations would you like to skip?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        print(f'Skipping {generations} generations.', end='')
        for generation in range(generations):
            self.__world.next_generation()
            if generation % 100 == 0:
                print('.', end='')
        print(' done!')
        time.sleep(2)
        string = self.__world.__str__()
        string += self.status()
        print(string)
        print(self.menu(), end=' ')

    def change_fillrate(self, parameter):
        """Change the fillrate for the simulation."""
        if toolbox.is_number(parameter) and 0 <= float(parameter) <= 100:
            fillrate = float(parameter)
        else:
            prompt = 'What percent of cells should be alive?'
            fillrate = toolbox.get_integer_between(0,100,prompt)
        self.__fillrate = fillrate
        self.random()

    def change_delay(self, parameter):
        """Change the delay betwen generations of the simulation."""
        if toolbox.is_number(parameter):
            delay = float(parameter)
        else:
            prompt = 'Seconds of delay between generations?'
            delay = toolbox.get_number(prompt)
        self.__delay = delay

    def change_display(self, parameter):
        """Change the live and dead characters for the cells."""
        if toolbox.is_integer(parameter) and \
           1 <= int(parameter) <= len(Cell.displaySets.keys()):
            setNumber = int(parameter)
        else:
            print('**************************************')
            for number, set in enumerate(Cell.displaySets):
                liveChar = Cell.displaySets[set]['liveChar']
                deadChar = Cell.displaySets[set]['deadChar']
                print(f'{number+1}: living cells: {liveChar} dead cells: {deadChar}')
            print('**************************************')
            prompt = 'What character set would you like to use?'
            setNumber = toolbox.get_integer_between(1, number + 1, prompt)
        setString = list(Cell.displaySets.keys())[setNumber - 1]
        Cell.set_display(setString)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end = ' ')

    def random(self):
        """Create a random world"""
        self.__world.randomize(self.__fillrate)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end = ' ')

    def change_size(self, parameter):
        if parameter:
            rows, columns = parameter.split('x',2)
            if toolbox.is_integer(rows) and toolbox.is_integer(columns):
                rows = int(rows)
                columns = int(columns)
        else:
            prompt = 'How many rows of cells?'
            rows = toolbox.get_integer_between(1,40,prompt)
            prompt = 'How many cells in each row?'
            columns = toolbox.get_integer_between(1,120,prompt)
        self.__world = World(rows, columns)
        self.random()

    def long_l_world(self):
        """Create a blank world and put this pattern in the middle:
        ....
        .x..
        .x..
        .x..
        .xx.
        .... """
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        self.__world = World(rows, columns)

        middleRow = int(rows / 2)
        middleColumn = int(columns / 2)

        self.__world.set_cell(middleRow - 2, middleColumn, True)
        self.__world.set_cell(middleRow - 1, middleColumn, True)
        self.__world.set_cell(middleRow - 0, middleColumn, True)
        self.__world.set_cell(middleRow + 1, middleColumn, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 1, True)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end = ' ')


    def acorn_world(self):
        """Create a blank world and put this pattern in the middle:
         .........
         ..x......
         ....x....
         .xx..xxx.
         .........
         """
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        self.__world = World(rows, columns)

        middleRow = int(rows / 2)
        middleColumn = int(columns / 2)

        self.__world.set_cell(middleRow - 1, middleColumn - 2, True)
        self.__world.set_cell(middleRow - 0, middleColumn - 0, True)
        self.__world.set_cell(middleRow + 1, middleColumn - 3, True)
        self.__world.set_cell(middleRow + 1, middleColumn - 2, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 1, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 2, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 3, True)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end = ' ')


if __name__ =='__main__':
    simulation = Life()
    simulation.main()
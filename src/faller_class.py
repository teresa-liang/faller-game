COLORS = ('R', 'O', 'Y', 'G', 'B', 'I', 'P')

class Faller:
    def __init__(self, colors: str, col_num: int):
        '''Initializes variables'''
        faller = []
        colors = colors.split()

        for color in colors:
            faller.append(f'[{color}]')

        faller.reverse() # first element should be the first block that shows up in the field
        
        self.faller = faller
        self.faller_num = 0 # keeps track of how many squares of the faller has entered the field
        self.faller_spot = 0 # keeps track of the index position of the front of the faller
        self.faller_col = col_num # keeps track of which column the faller is in
        self.landed = False
        self.frozen = False
    def add_to_faller_num(self):
        '''Adds 1 to the faller num'''
        self.faller_num += 1
    def add_to_faller_spot(self):
        '''Adds 1 to the faller index position'''
        self.faller_spot += 1
    def change_faller_col(self, col_num: int):
        '''Changes the column index of the faller'''
        self.faller_col = col_num
    def rotate(self):
        '''Rotates the faller'''
        faller = self.faller[:]
        for square in range(len(faller)):
            faller[square - 1] = self.faller[square]
        self.faller = faller
    def fall(self):
        '''Changes the faller to a falling state'''
        self.landed = False
        for square in range(len(self.faller)):
            self.faller[square] = f'[{self.faller[square][1]}]'
    def land(self):
        '''Changes the faller to a landing state'''
        self.landed = True
        for square in range(len(self.faller)):
            self.faller[square] = f'|{self.faller[square][1]}|'
    def freeze(self):
        '''Changes the faller to a frozen state'''
        self.frozen = True
        for square in range(len(self.faller)):
            self.faller[square] = f' {self.faller[square][1]} '
    
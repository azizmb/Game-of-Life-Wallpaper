class Cell(object):
    def __init__(self,row,col,state):
        self.row = row
        self.col = col
        self.neighbours = {}
        self.state = state
        self.marked = False
        
    def set_neighbour(self,c):
        neighbour = self.neighbours.get((c.row,c.col),None)
        if not neighbour :
            self.neighbours[(c.row,c.col)] = c
    def live_neighbours(self):
        live = 0
        for cell in self.neighbours.values() :
            if cell.state :
                live += 1
        return live

    def cycle(self):
        live = self.live_neighbours()
        if self.state :
            if live < 2 : self.marked = False
            elif live > 3 : self.marked = False
            else : self.marked = True
        elif live == 3 :
            self.marked = True
        else :
            self.marked = False

    def switch(self):
        self.state = self.marked

class Board(object):
    def __init__(self, **kwargs):
        self.cells = []
        self.step = 0
        self.rows = kwargs.pop('rows')
        self.cols = kwargs.pop('cols')
                
        try:
            if kwargs.has_key('filename'):
                fname = kwargs.pop('filename')
                f = open(fname,"r")
                yindex = 0
                live = set()
                line = f.readline()
                while line!="":
                    line = f.readline()
                    if line == "":
                        break
                    line = line.split()
                    c = lambda a:(int(a[0])+(self.cols/2), int(a[1])+(self.rows/2))
                    live.add(c(line))
                    
            else:
                live = kwargs.pop('live')

        except Exception as e:
            raise e
        
        else:
            for row_nbr in range(self.rows):
                row = []
                self.cells.append(row)
                for col_nbr in range(self.cols) :
                    if (col_nbr,row_nbr) in live :
                        row.append(Cell(col_nbr,row_nbr,True))
                    else :
                        row.append(Cell(col_nbr,row_nbr,False))
            for row_nbr in range(self.rows) :
                for col_nbr in range(self.cols) :
                    for row_offset in (-1,0,1) :
                        for col_offset in (-1,0,1) :
                            self.set_neighbours(
                                row_nbr,col_nbr,
                                row_offset,col_offset)
                                
    def set_neighbours(self,row_nbr,col_nbr, row_offset,col_offset):
        n_row = row_nbr + row_offset
        n_col = col_nbr + col_offset
        if 0 <= n_row < self.rows :
            if 0 <= n_col < self.cols :
                if (n_row != row_nbr) or \
                    (n_col != col_nbr) :
                    self.cells[row_nbr][col_nbr]\
                        .set_neighbour(
                            self.cells[n_row][n_col])

    def show(self):
        buffer = []
        for row in range(self.rows) :
            row_buffer = []
            for col in range(self.cols) :
                if self.cells[row][col].state == True :
                    row_buffer.append('*')
                else :
                    row_buffer.append('-')
            buffer.append("".join(row_buffer))
        return "\n".join(buffer)

    def cycle(self):
        self.step += 1
        for row in range(self.rows) :
            for col in range(self.cols) :
                self.cells[row][col].cycle()
        for row in range(self.rows) :
            for col in range(self.cols) :
                self.cells[row][col].switch()
                
    def execute(self, cycles):
        for i in range(cycles):
            self.cycle()
    
    def save(self, filename):
        f = file(filename, 'w')
        f.write("%s\n%s\n%s\n"%(self.step, self.cols, self.rows))
        
        for row in self.cells:
            for cell in row:
                if cell.state:
                    f.write("*")
                else:
                    f.write(".")
            f.write("\n")
        f.close()
                
    def get_size(self):
        return (self.cols, self.rows)
    
    def get_array(self):
        from numpy import array, empty
        l = list()
        for row in self.cells:
            l.append([cell.state for cell in row])
        return array(l)

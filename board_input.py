from tkinter import *
DEFAULT_FONT = ('Helvetica', 14)

class InputDialog:

    def __init__(self, rows, columns):
        self._input_window =  Toplevel()

        self.rows = rows
        self.columns = columns
        
        self.visual_board = Canvas(master=self._input_window, width=500, height=500, background = 'green')
        self.visual_board.grid(column = 0, row = 1, columnspan=2 , sticky=N+S+E+W)


        self.visual_board.rowconfigure(1, weight=1)
        self.visual_board.columnconfigure(0, weight = 1)

        self._input_window.rowconfigure(1, weight = 1)
        self._input_window.columnconfigure(0, weight = 1)

        self.visual_board.update()
        
        self.explanation_label = Message(master=self._input_window,width=450,
                 text = 'To add a black chip double-left click the desired cell \n'
                        'To add a white chip right click the desired cell \n'
                        'To remove a chip left click the desired cell\n'
                        'When finished press done to play the game \n')
        
        self.explanation_label.grid(row = 0, column = 0)

        self.done_button = Button(master= self._input_window, text = 'DONE', width = 20,
                height = 5, command = self._on_done_button)
        self.done_button.grid(row = 0, column = 1)

        self.done = False

        self.cell_width = self.visual_board.winfo_width() / self.columns
        self.cell_height = self.visual_board.winfo_height() / self.rows

        self.black_chips = []
        self.white_chips = []

        self.create_grid()

        self.board = []

        for x in range(self.rows):
            self.board.append([])
        for y in range(self.columns):
            for x in self.board:
                x.append('.')
        
        self.visual_board.bind('<Configure>', self.on_resize)
        self.visual_board.bind('<Double-Button-1>', self.place_black_chip)
        self.visual_board.bind('<Button-3>', self.place_white_chip)
        self.visual_board.bind('<Button-1>', self.remove)
        self.done_button.bind('<Button-1>', self.update_and_pass_internal_board)

    def fraction_comparison(self, xfraction, yfraction):
        x_result = NONE
        y_result = NONE

        for x in range(self.columns):
            if xfraction >= (x-1)/self.columns and xfraction <= x/self.columns:
                x_result = x
            if xfraction >= (self.columns - 1)/self.columns and xfraction <= 1:
                x_result = self.columns

        for y in range(self.rows):
            if yfraction >= (y-1)/self.rows and yfraction <= y/self.rows:
                y_result = y
            if yfraction >= (self.rows - 1)/self.rows and yfraction <= 1:
                y_result = self.rows
        return (y_result , x_result)

    def draw_chips(self,coordinate, color):
        self.visual_board.update()

        self.cell_width = self.visual_board.winfo_width() / self.columns
        self.cell_height = self.visual_board.winfo_height() / self.rows

        upper_x = ((int(coordinate[1])-1) * self.cell_width) + 2
        upper_y = ((int(coordinate[0])-1) * self.cell_height) + 3
        lower_x = int(coordinate[1]) * self.cell_width - 2
        lower_y = int(coordinate[0]) * self.cell_height - 3

        self.visual_board.create_oval(upper_x,upper_y,lower_x,lower_y, fill=color)

    def on_chip_update(self):
        self.visual_board.delete(ALL)
        for x in self.black_chips:
            self.draw_chips(x, 'black')
        for x in self.white_chips:
            self.draw_chips(x, 'white')
        self.create_grid()

    def on_resize(self, event):
        self.visual_board.update()
        self.cell_width = self.visual_board.winfo_width() / self.columns
        self.cell_height = self.visual_board.winfo_height() / self.rows
        self.visual_board.delete(ALL)

        for x in self.black_chips:
            self.draw_chips(x, 'black')
        for x in self.white_chips:
            self.draw_chips(x, 'white')
        self.create_grid()

    def place_black_chip(self, event):
        self.visual_board.update()

        xfraction = (event.x / self.visual_board.winfo_width())
        yfraction = (event.y / self.visual_board.winfo_height())
        chip_coordinate = self.fraction_comparison(xfraction,yfraction)

        if chip_coordinate in self.white_chips:
            self.white_chips.remove(chip_coordinate)
            if chip_coordinate not in self.black_chips:
                self.black_chips.append(chip_coordinate)
        else:
            if chip_coordinate not in self.black_chips:
                self.black_chips.append(chip_coordinate)
        self.on_chip_update()

    def create_grid(self):
        for x in range(self.columns):
            self.visual_board.create_line(x*self.cell_width, 0, x*self.cell_width, self.visual_board.winfo_height())
        for x in range(self.rows):
            self.visual_board.create_line(0,x*self.cell_height, self.visual_board.winfo_width(), x*self.cell_height)

    def place_white_chip(self, event):
        self.visual_board.update()

        xfraction = (event.x / self.visual_board.winfo_width())
        yfraction = (event.y / self.visual_board.winfo_height())
        chip_coordinate = self.fraction_comparison(xfraction, yfraction)

        if chip_coordinate in self.black_chips:
            self.black_chips.remove(chip_coordinate)
            if chip_coordinate not in self.white_chips:
                self.white_chips.append(chip_coordinate)
        else:
            if chip_coordinate not in self.white_chips:
                self.white_chips.append(chip_coordinate)
        self.on_chip_update()

    def remove(self, event):
        self.visual_board.update()

        xfraction = (event.x / self.visual_board.winfo_width())
        yfraction = (event.y / self.visual_board.winfo_height())
        chip_coordinate = self.fraction_comparison(xfraction, yfraction)

        for x in self.white_chips:
            if chip_coordinate == x:
                self.white_chips.remove(x)

        for x in self.black_chips:
            if chip_coordinate == x:
                self.black_chips.remove(x)

        self.on_chip_update()

    def update_and_pass_internal_board(self, event):
        for x in self.black_chips:
            self.board[x[0]-1][x[1]-1] = 'B'
        for x in self.white_chips:
            self.board[x[0]-1][x[1]-1] = 'W'

    def show(self) -> None:
        self._input_window.grab_set()
        self._input_window.wait_window()

    def was_done_clicked(self) -> bool:
        return self._done_clicked

    def _on_done_button(self) -> None:
        self._done_clicked = True
        self._input_window.destroy()



import simplified_logic
from tkinter import *

class GUI_game:
    def __init__(self, board, turn, win_condition, rows, columns):
        self.root_window = Toplevel()
        self.game_state = simplified_logic.Game_state(board, turn, win_condition, rows, columns)

        self.board = board

        self.chip_count_variable = StringVar()
        self.chip_count_variable.set('Black chips: {}  White Chips: {}'.format(self.chip_count()[0],self.chip_count()[1]))
        self.chip_label = Label(master = self.root_window,textvariable = self.chip_count_variable, font = ('Helvetica', 18)).grid(row = 0, column = 0, sticky= N+S+E+W)

        self.turn_variable = StringVar()
        self.turn_variable.set('Current turn: {}'.format(self.game_state.turn))
        self.turn_label = Label(master= self.root_window, textvariable = self.turn_variable, font = ('Helvetica', 18)).grid(row = 0, column = 1, sticky= N+S+E+W)

        self.mode_label = Label(master= self.root_window, text = ' MODE: Simple', font = ('Helvetica', 20)).grid(row=0, column = 2, sticky= N+S+E+W)

        self.valid_variable = StringVar()
        self.valid_variable.set('Left click a valid tile to place your chip')
        self.valid_label = Label(master = self.root_window, textvariable = self.valid_variable, font = ('Helvetica', 18)).grid(row = 2, columnspan = 3, sticky = N+S+W+E)

        self.visual_game_board = Canvas(master=self.root_window, height = 500, width = 500, background = 'green')
        self.visual_game_board.grid(row = 1, column = 0, sticky= N+S+E+W, columnspan= 3)


        self.root_window.rowconfigure(1, weight=1)
        self.root_window.columnconfigure(0, weight = 1)
        self.root_window.columnconfigure(1, weight=1)

        self.visual_game_board.columnconfigure(0, weight = 1)
        self.visual_game_board.columnconfigure(1, weight=1)
        self.visual_game_board.columnconfigure(2, weight=1)

        self.visual_game_board.rowconfigure(1, weight=1)

        self.visual_game_board.update()

        self.rows = rows
        self.columns = columns

        self.cell_width = self.visual_game_board.winfo_width() / self.columns
        self.cell_height = self.visual_game_board.winfo_height() / self.rows

        self.on_chip_update()

        if self.game_state.board_empty_or_full():
            self.warning = Toplevel()
            self.warning.geometry('150x100')
            self.warning_message = Label(master= self.warning, text = 'The winner is : {}'.format(self.game_state.determine_winner_name())).grid(row = 0, padx = 20, pady = 20)
            self.warning_button = Button(master= self.warning, text = 'Exit game', command=self.exit).grid(row = 1, padx = 5, pady = 5)

        if self.game_state.check_single_valid_move() == False:
            self.game_state.turn = self.game_state.opposite_turn()
            self.update_label_variable()

        self.visual_game_board.bind('<Button-1>', self.on_board_click)
        self.visual_game_board.bind('<Configure>', self.on_resize)

    def exit(self):
        self.warning.destroy()
        self.root_window.destroy()

    def create_grid(self):
        self.visual_game_board.update()
        self.cell_width = self.visual_game_board.winfo_width() / self.columns
        self.cell_height = self.visual_game_board.winfo_height() / self.rows

        for x in range(self.columns):
            self.visual_game_board.create_line(x*self.cell_width, 0, x*self.cell_width, self.visual_game_board.winfo_height())
        for x in range(self.rows):
            self.visual_game_board.create_line(0,x*self.cell_height, self.visual_game_board.winfo_width(), x*self.cell_height)

    def draw_chips(self,coordinate, color):
        self.visual_game_board.update()
        self.cell_width = self.visual_game_board.winfo_width() / self.columns
        self.cell_height = self.visual_game_board.winfo_height() / self.rows

        upper_x = ((int(coordinate[1])-1) * self.cell_width) + 2
        upper_y = ((int(coordinate[0])-1) * self.cell_height) + 3
        lower_x = int(coordinate[1]) * self.cell_width - 2
        lower_y = int(coordinate[0]) * self.cell_height - 3

        self.visual_game_board.create_oval(upper_x,upper_y,lower_x,lower_y, fill=color)

    def on_chip_update(self):
        self.visual_game_board.update()
        self.visual_game_board.delete(ALL)

        for x in range(self.rows):
            for y in range(self.columns):
                if self.game_state.board_state[x][y] == 'W':
                    self.draw_chips([x+1,y+1], 'white')
                if self.game_state.board_state[x][y] == 'B':
                    self.draw_chips([x+1,y+1], 'black')
        self.create_grid()

    def on_resize(self, event):
        self.visual_game_board.update()
        self.visual_game_board.delete(ALL)

        for x in range(self.rows):
            for y in range(self.columns):
                if self.game_state.board_state[x][y] == 'W':
                    self.draw_chips([x+1,y+1], 'white')
                if self.game_state.board_state[x][y] == 'B':
                    self.draw_chips([x+1,y+1], 'black')
        self.create_grid()

    def fraction_comparison(self, xfraction, yfraction):
        x_result = NONE
        y_result = NONE

        for x in range(self.rows):
            if xfraction >= (x-1)/self.rows and xfraction <= x/self.rows:
                x_result = x
            if xfraction >= (self.rows - 1)/self.rows and xfraction <= 1:
                x_result = self.rows

        for y in range(self.columns):
            if yfraction >= (y-1)/self.columns and yfraction <= y/self.columns:
                y_result = y
            if yfraction >= (self.columns - 1)/self.columns and yfraction <= 1:
                y_result = self.columns
        return (y_result - 1 , x_result - 1)

    def on_board_click(self, event):

        xfraction = (event.x / self.visual_game_board.winfo_width())
        yfraction = (event.y / self.visual_game_board.winfo_height())
        chip_coordinate = self.fraction_comparison(xfraction, yfraction)

        if self.game_state.check_single_valid_move():
            if self.game_state.check_all_directions(chip_coordinate, self.game_state.turn)[0] == True:
                self.valid_variable.set('Valid')
                self.game_state.flip_all_valids([chip_coordinate[0], chip_coordinate[1]])
                self.on_chip_update()
                self.game_state.turn = self.game_state.opposite_turn()
                self.update_label_variable()
                if self.game_state.board_full():
                    self.warning = Toplevel()
                    self.warning.geometry('150x100')
                    self.warning_message = Label(master=self.warning, text='The winner is : {}'.format(
                        self.game_state.determine_winner_name())).grid(row=0, padx=20, pady=20)
                    self.warning_button = Button(master=self.warning, text='Exit game', command=self.exit).grid(row=1,
                                                                                                                padx=5,
                                                                                                                pady=5)
            else:
                self.valid_variable.set('Invalid')
        else:
            self.game_state.turn = self.game_state.opposite_turn()
            if self.game_state.check_both_possible_move() == False:
                self.warning = Toplevel()
                self.warning.geometry('150x100')
                self.warning_message = Label(master=self.warning, text='The winner is : {}'.format(
                    self.game_state.determine_winner_name())).grid(row=0, padx=20, pady=20)
                self.warning_button = Button(master=self.warning, text='Exit game', command=self.exit).grid(row=1,
                                                                                                            padx=5,
                                                                                                            pady=5)

    def chip_count(self):
        blacks = 0
        whites = 0

        for x in self.board:
            for y in x:
                if y == 'W':
                    whites += 1
                if y == 'B':
                    blacks += 1

        return (blacks, whites)

    def update_label_variable(self):
        self.chip_count_variable.set('Black chips: {}  White Chips: {}'.format(self.chip_count()[0],self.chip_count()[1]))
        self.turn_variable.set('Current turn: {}'.format(self.game_state.turn))

    def run(self):
        self.root_window.mainloop()

#GUI_game([['.', '.', '.', '.'], ['.', 'W', 'W', '.'], ['.', 'B', 'W', '.'], ['.', '.', '.', '.']], 'W', '>', 4, 4).run()
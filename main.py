from tkinter import *
from simplified_logic import *

class Option_popup:
    def __init__(self):

        self.row_selection = 0
        self.column_selection = 0
        self.first_turn_selection = ''
        self.win_lose_selection = ''

        self.options_pop_up = Toplevel()
        self.options_pop_up.title('Options')
        self. row_column_choices = ['4','6','8','10','12','14','16']

        self.row_frame = Frame(master=self.options_pop_up).grid(column=0, row=0)
        self.column_frame = Frame(master=self.options_pop_up).grid(column=1, row=0)

        self.row_label = Label(self.row_frame, text='How Many Rows?').grid(row=0,column=0, padx=5, pady=5)
        self.column_label = Label(self.column_frame, text='How Many Columns?').grid(row=0, column=1, padx=5)

        # ROW AND COLUMN RADIO BUTTON SETUP

        self.row = StringVar()
        self.row.set('Row Choice')

        self.column = StringVar()
        self.column.set('Column Choice')

        for row in self.row_column_choices:
            Radiobutton(self.row_frame,text=row,variable=self.row,value=int(row))\
            .grid(row=self.row_column_choices.index(row)+1,column = 0, sticky=W)

        for column in self.row_column_choices:
            Radiobutton(self.column_frame,text=column,variable=self.column,value=int(column))\
            .grid(row=self.row_column_choices.index(column)+1,column = 1, sticky=W)

        # INITIAL TURN SELECTION SETUP

        self.turn_frame = Frame(master=self.options_pop_up).grid(column=0, row=9)
        self.turn_label = Label(self.turn_frame, text='Who starts first?').grid(row=9, column=0, pady=5, columnspan=2)
        self.turn = StringVar()

        self.white_button = Radiobutton(self.turn_frame, text='WHITE', variable=self.turn, )
        self.white_button.config(indicatoron=0, width=12, value=WHITE)
        self.white_button.grid(column=0,row=10)

        self.black_button = Radiobutton(self.turn_frame, text='Black', variable=self.turn, )
        self.black_button.config(indicatoron=0, width=12, value=BLACK)
        self.black_button.grid(column=1, row=10)

        # INITIAL WIN CONDITION SETUP

        self.win_frame = Frame(master=self.options_pop_up).grid(column=0, row=12)

        self.turn_label = Label(self.win_frame, text='How will the game be scored?').grid(row=11, column=0, pady=5, columnspan=2)

        self.win = StringVar()
        self.white_button = Radiobutton(self.turn_frame, text='More chips win', variable=self.win, )
        self.white_button.config(indicatoron=0, width=12, value= '>')
        self.white_button.grid(column=0, row=12)

        self.black_button = Radiobutton(self.turn_frame, text='Fewer chips win', variable=self.win, )
        self.black_button.config(indicatoron=0, width=12, value='<')
        self.black_button.grid(column=1, row=12, pady=5)

        # DONE BUTTON SETUP

        self.done = Button(text='Done')
        self.done.config(width=20)
        self.done.grid(column=0,row=13, columnspan = 2, pady = 10)
        self.done.bind('<Button-1>',self.return_values)

        self.options_pop_up.grid()

    def return_values(self, event):

        self.row_selection = int(self.row.get())
        self.column_selection = int(self.column.get())
        self.win_lose_selection = self.win.get()
        self.first_turn_selection = self.turn.get()

        return(self.row.get(), self.column.get(),self.win.get(),self.turn.get())

    def run(self) -> None:
        self.options_pop_up.mainloop()

if __name__ == '__main__':
    app = Option_popup()
    app.run()
    print(app.row_selection, app.column_selection, app.first_turn_selection, app.win_lose_selection)

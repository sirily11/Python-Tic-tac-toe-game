import tkinter as tk
from PIL import Image, ImageTk


class TicTacToe(tk.Frame):
    def __init__(self, master):
        self.env = Game_Logic()
        tk.Frame.__init__(self, master, width=130, height=80)
        size = (100, 100)
        # This is the way that how python would read the
        # icon from the directory and would resize the
        # Image to the size we want
        self.tic = Image.open("Tick.jpg")
        self.tic.thumbnail(size, Image.ANTIALIAS)
        self.tic = ImageTk.PhotoImage(self.tic)
        # Add circle picture
        self.circle = Image.open("circle.jpg")
        self.circle.thumbnail(size, Image.ANTIALIAS)
        self.circle = ImageTk.PhotoImage(self.circle)
        # Add Blank space image
        self.blank = Image.open(("blank.jpg"))
        self.blank.thumbnail(size, Image.ANTIALIAS)
        self.blank = ImageTk.PhotoImage(self.blank)
        # Set the player's info
        self.infoOne = tk.Label(master, text='Player One', foreground="red")
        self.infoOne.grid(column=0, row=0)
        self.infoTwo = tk.Label(master, text='Player Two')
        self.infoTwo.grid(column=2, row=0)
        # Setting the windows's name
        self.player = 0
        self.master.title("Tic-Tac-Toe")
        self.b1 = tk.Button(command=lambda: self.click_on_map(self.b1, 0, 0),
                            width=size[0], height=size[1], image=self.blank)
        self.b1.grid(column=0, row=1)

        self.b2 = tk.Button(command=lambda: self.click_on_map(self.b2, 1, 0),
                            width=size[0], height=size[1], image=self.blank)
        self.b2.grid(column=1, row=1)

        self.b3 = tk.Button(command=lambda: self.click_on_map(self.b3, 2, 0),
                            width=size[0], height=size[1], image=self.blank)
        self.b3.grid(column=2, row=1)

        self.b4 = tk.Button(command=lambda: self.click_on_map(self.b4, 0, 1),
                            width=size[0], height=size[1], image=self.blank)
        self.b4.grid(column=0, row=2)

        self.b5 = tk.Button(command=lambda: self.click_on_map(self.b5, 1, 1),
                            width=size[0], height=size[1], image=self.blank)
        self.b5.grid(column=1, row=2)

        self.b6 = tk.Button(command=lambda: self.click_on_map(self.b6, 2, 1),
                            width=size[0], height=size[1], image=self.blank)
        self.b6.grid(column=2, row=2)

        self.b7 = tk.Button(command=lambda: self.click_on_map(self.b7, 0, 2),
                            width=size[0], height=size[1], image=self.blank)
        self.b7.grid(column=0, row=3)

        self.b8 = tk.Button(command=lambda: self.click_on_map(self.b8, 1, 2),
                            width=size[0], height=size[1], image=self.blank)
        self.b8.grid(column=1, row=3)

        self.b9 = tk.Button(command=lambda: self.click_on_map(self.b9, 2, 2),
                            width=size[0], height=size[1], image=self.blank)
        self.b9.grid(column=2, row=3)

        self.buttons = [self.b1, self.b2, self.b3, self.b4, self.b5,
                        self.b6, self.b7, self.b8, self.b9]

    def click_on_map(self, button, col, row):
        winner = self.env.act(row=row, col=col, player=(self.player % 2) + 1)
        if self.player % 2 == 0:
            button.configure(image=self.circle, state="disable")
            if winner == None or self.env.__isDone__() != True:
                self.infoOne.configure(foreground="black")
                self.infoTwo.configure(foreground="red")

        else:
            button.configure(image=self.tic, state="disable")
            if winner == None or self.env.__isDone__() != True:
                self.infoOne.configure(foreground="red")
                self.infoTwo.configure(foreground="black")

        if winner != None:
            winner = "Player " + str(winner) + " Wins"
            self.__disable_all_buttons__()
            top = tk.Toplevel()
            tk.Label(top, text=winner, width=20, height=10).grid(column=0, row=0)
            tk.Button(top, text="restart", command=
            lambda: self.click_on_restart(top)).grid(column=0, row=1)
            return None

        if self.env.__isDone__() == True and winner == None:
            top = tk.Toplevel()
            self.__disable_all_buttons__()
            tk.Label(top, text="Draw", width=20, height=10).grid(column=0, row=0)
            tk.Button(top, text="restart", command=
            lambda: self.click_on_restart(top)).grid(column=0, row=1)
            return None

        self.player = self.player + 1

    def __disable_all_buttons__(self):
        for b in self.buttons:
            b.configure(state='disable')

    def click_on_restart(self, windows):
        for b in self.buttons:
            b.configure(state='active', image=self.blank)
        self.env.reset()
        self.player = 0
        self.infoOne.configure(foreground="red")
        self.infoTwo.configure(foreground="black")
        windows.destroy()

class Game_Logic():
    def __init__(self):
        # initial game. 0 stands for empty space
        # 1 stands for player one
        # 2 stands for player two
        self.game_map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = None

    '''
    We can use this method to get what is the current
    status of the game.If the game is done, it will return
    who is the winner or draw. It will take the column and
    row to play the game
    '''

    def act(self, row, col, player):
        if self.game_map[row][col] == 0:
            self.game_map[row][col] = player
            self.check_winner()
        else:
            print("It has already been occupied")
        return self.winner

    def show_game(self):
        for l in self.game_map:
            for e in l:
                print(e + " ")
            print()
        print()

    def reset(self):
        self.game_map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = None


    def __isDone__(self):
        count = 0
        for l in self.game_map:
            for e in l:
                if e != 0:
                    count = count + 1
            if count == 9:
                return True

        if self.check_winner() != None:
            return True
        return False

    def check_winner(self):
        game_map = self.game_map
        if game_map[0][0] == game_map[0][1] == game_map[0][2] != 0:
            self.winner = game_map[0][0]

        if game_map[0][0] == game_map[1][0] == game_map[2][0] != 0:
            self.winner = game_map[0][0]

        if game_map[0][0] == game_map[1][1] == game_map[2][2] != 0:
            self.winner = game_map[0][0]

        if game_map[0][1] == game_map[1][1] == game_map[2][1] != 0:
            self.winner = game_map[0][1]

        if game_map[0][2] == game_map[1][2] == game_map[2][2] != 0:
            self.winner = game_map[0][2]

        if game_map[1][0] == game_map[1][1] == game_map[1][2] != 0:
            self.winner = game_map[1][0]

        if game_map[2][0] == game_map[2][1] == game_map[2][2] != 0:
            self.winner = game_map[2][0]

        if game_map[2][0] == game_map[1][1] == game_map[0][2] != 0:
            self.winner = game_map[2][0]

        return self.winner


root = tk.Tk()
game = TicTacToe(root)
game.mainloop()
# game = Game_Logic()
# print(game.check_winner())

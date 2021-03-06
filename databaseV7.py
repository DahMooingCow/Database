import sqlite3, time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import hello

startTime = time.time()
columnList = []
testList = []
conn = sqlite3.connect('data.db')

cur = conn.cursor()
cur.execute('''SELECT * FROM Games ORDER BY priority DESC;''')
# TRY USING MAP

def tableCreate():
    cur.execute("""CREATE TABLE Videos(
                id INTEGER PRIMARY KEY,
                name TEXT,
                score TEXT,
                priority TEXT,
                type TEXT,
                genre TEXT,
                platform TEXT,
                completed TEXT,
                description TEXT
                )""")


def time():
    endTime = time.time()
    file = open("times.txt","a")
    timeTaken = str(endTime-startTime)
    info = "This script took "+timeTaken+" seconds"
    print(info)
    file.write(timeTaken+"\n")
    messagebox.showinfo("Info", info)
    file.close()


def addEntry():
    addCount = int(input("How many Games do you want to add?"))
    for i in range(0,addCount):
        newName = input("What is the name of the new Game:")
        newScore = input("What is the Score of the new Game[0-10]:")
        newPriority = input("What is the priority of the new Game[1-5]:")
        # newMulitplayer = input("What is the multiplayer of the new Game:")

        cur.execute("""INSERT INTO Videos(name, score, priority)
                    VALUES(?,?,?)""", (newName, newScore, newPriority))
        conn.commit()


def columnCount():
    cur.execute('''pragma table_info(Games);''')
    numberOfColumns = len(cur.fetchall())
    return numberOfColumns


def columnNames(table):
    cur.execute('PRAGMA table_info('+table+')')
    for col in cur.fetchall():
        columnList.append(col[1])
    return columnList


def rowCount():
    cur.execute('''SELECT * FROM Games''')
    numberOfRows = len(cur.fetchall())
    return numberOfRows


def update():
    all_rows = cur.fetchall()
    rowList = []
    for row in all_rows:
        rowList.append(row)
        for item in row:
            testList.append(item)


class App:
    def __init__(self, master):
        self.varLabel, self.input = StringVar(), StringVar()
        self.frame1, self.frame2 = Frame(master), Frame(master)
        self.frame1.pack(side=TOP)
        self.frame2.pack(side=BOTTOM)
        self.currentOption = StringVar()
        self.tree()


        self.games()

    def update(self):
        self.varLabel.set("Done!")
        self.tree.pack_forget()
        self.but4.pack_forget()
        self.menu.pack_forget()
        self.entry.pack_forget()
        self.infoLabel.pack_forget()
        global columnList
        columnList = []
        self.videos()
        if self.table == "Games":
            self.videos()
        if self.table == "Videos":
            self.games()

    def games(self):
        self.table = 'Games'
        self.optionList = columnNames(self.table)
        cur.execute('''SELECT * FROM Games ORDER BY priority DESC;''')
        self.varLabel.set("Ready!")
        # cur.execute('''SELECT * FROM Games ORDER BY priority DESC;''')
        self.all_rows = cur.fetchall()
        self.rowList = []
        for self.row in self.all_rows:
            self.rowList.append(self.row)
        self.menu = OptionMenu(self.frame1, self.currentOption, *self.optionList)
        self.menu.pack(side=LEFT, anchor=N)
        self.entry = Entry(self.frame1, textvariable=self.input)
        self.entry.pack(side=LEFT, anchor=N)
        self.infoLabel = Label(self.frame1, textvariable=self.varLabel)
        self.infoLabel.pack(side=LEFT, anchor=N)
        self.but4 = Button(self.frame2, text="Confirm", command=self.update)
        self.but4.pack(side=TOP, fill=X, expand=YES)
        self.tree = ttk.Treeview(self.frame2, columns=columnList, show='headings', height="400",
                                 style='Custom.Treeview')
        self.tree.pack(side=BOTTOM)
        self.tree.tag_configure('row', background='#1A5276')
        for col in columnNames(self.table):
            self.tree.column(col, width=80)
            self.tree.heading(col, text=col)
        for index, row in enumerate(self.rowList):
            self.tree.insert('', index, values=row, tags="row")
            # if index == 2:
            #     break

    def videos(self):
        self.table = 'Videos'
        self.optionList = columnNames(self.table)
        cur.execute('''SELECT * FROM Videos ORDER BY priority DESC;''')
        self.varLabel.set("Ready!")
        self.all_rows = cur.fetchall()
        self.rowList = []
        for self.row in self.all_rows:
            self.rowList.append(self.row)
        self.menu = OptionMenu(self.frame1, self.currentOption, *self.optionList).pack(side=LEFT, anchor=N)
        self.entry = Entry(self.frame1, textvariable=self.input).pack(side=LEFT, anchor=N)
        self.infoLabel = Label(self.frame1, textvariable=self.varLabel).pack(side=LEFT, anchor=N)
        self.but4 = Button(self.frame2, text="Confirm", command=self.nothing).pack(side=TOP, fill=X, expand=YES)
        self.tree = ttk.Treeview(self.frame2, columns=columnList, show='headings', height="400",
                                 style='Custom.Treeview')
        self.tree.pack(side=BOTTOM)
        self.tree.tag_configure('row', background='#1A5276')
        for col in columnNames(self.table):
            self.tree.column(col, width=108)
            self.tree.heading(col, text=col)
        for index, row in enumerate(self.rowList):
            self.tree.insert('', index, values=row, tags="row")
        pass

    def tree(self):
        self.style = ttk.Style()
        self.style.element_create("Custom.Treeheading.border", "from", "default")
        self.style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        self.style.configure("Custom.Treeview.Heading",
                        background="#154360", foreground="white", relief="flat")
        self.style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

    def nothing(self):
        print('here')
        pass

class Menu:
    def __init__(self, master):
        self.frame3 = master
        Button(self.frame3, text="Database APP", command=self.create).pack()

    def create(self):
        top()


def top():
    menu.frame3.destroy()
    top = Toplevel()
    windowGeometry = (str(80 * columnCount())+"x800")
    print(windowGeometry)
    top.geometry(windowGeometry)
    top.resizable(True, True)
    App(top)

root = Tk()
root.withdraw()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Everything")
menu = Menu(Toplevel())
root.mainloop()
conn.close()

# cur.execute("ALTER TABLE Games ADD COLUMN Description")


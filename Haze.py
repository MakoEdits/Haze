import json, sys, os, time
import tkinter as tk
from tkinter import font as tkfont

class DS():
    def __init__(self):
        #Stores "Design Styles" to be easily accessed
        self.startupBG = "#00141c"
        self.startupFG = "#09adec"
        self.startupD = "#00090d"
        self.mainBG = "#00141c"
        self.mainFG = "#09adec"
        self.mainHover = "#086b92"

class CurrentUser:
    def __init__(self, username, password, email, DOB, currency):
        #Current user data
        global path
        self.username = username
        self.password = password
        self.email = email
        self.DOB = DOB
        self.gamesLibrary = DictionaryReader(str(path)+"/users/"+str(username)+"/gamesLibrary")
        self.gamesList = []
        self.sortedPlayed = self.gamesInfo()
        self.currentlyPlaying = False
        self.currency = currency
        self.shoppingCart = ["", ""]
        self.cartIndexes = ["",""]

    #Sorts the users game library by the time played descending to be used in quick access tab
    def gamesInfo(self):
        gamesList = []
        for x in self.gamesLibrary.items():
            gamesList.append(list(x))
        self.gamesList = gamesList
        sortedPlayed = self.sortPlayed(gamesList)
        if len(sortedPlayed) < 3:
            return "Empty"
        else:
            return list(reversed(sortedPlayed))

    #Quicksort algorithm to sort by time played
    def sortPlayed(self, List):
        less = []
        equal = []
        greater = []
        if len(List) > 1:
            pivot = List[0][1]["timePlayed"]
            for x in List:
                if x[1]["timePlayed"] < pivot:
                    less.append(x)
                if x[1]["timePlayed"] == pivot:
                    equal.append(x)
                if x[1]["timePlayed"] > pivot:
                    greater.append(x)
            return self.sortPlayed(less)+equal+self.sortPlayed(greater)
        else:
            return List

class HazeMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        #Draws frames to be displayed
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("{}x{}".format(600, 400))
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self, bg=DS.mainBG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.config(bg=DS.mainBG)
        self.frames = {}
        for F in (Haze_Main, Haze_Library, Haze_Store, Haze_Settings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg=DS.mainBG)
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Haze_Main")

    #Raises selected frame to the front to be visible
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HazeStartup(tk.Tk):
    def __init__(self, *args, **kwargs):
        #Draws frames to be displayed
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self, bg=DS.mainBG)
        container.config(bg=DS.mainBG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Haze_Login, Haze_Create):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg=DS.mainBG)
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Haze_Login")

    #Raises selected frame to the front to be visible
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Haze_Login(tk.Frame):
    def __init__(self, parent, controller):
        #This class draws the Login frame for the startup window. 
        #This frame allows the user to enter their username, password and keep them logged in
        tk.Frame.__init__(self, parent, bg=DS.startupBG)
        self.controller = controller
        #Main frame
        frameLogin = tk.Frame(self, bg=DS.startupBG)
        #Title
        frameTitle = tk.Frame(frameLogin, bg=DS.startupBG)
        labelTitle = tk.Label(frameTitle, text="Login", font=controller.title_font,  bg=DS.startupBG, fg=DS.startupFG)
        labelTitle.pack(side="top", fill="x", pady=10)
        #Create account entries
        frameEntries = tk.Frame(frameLogin, bg=DS.startupBG)
        #Username login entry and label
        frameUsername = tk.Frame(frameEntries, bg=DS.startupBG)
        labelUsername = tk.Label(frameUsername, text="Username:", bg=DS.startupBG, fg=DS.startupFG)
        labelUsername.pack(padx=7, side="left")
        self.entryTraceUsername = tk.StringVar()
        self.entryTraceUsername.set("")
        self.entryTraceUsername.trace("w", lambda name, index, mode, entryTraceUsername=self.entryTraceUsername: 
            self.testEntry(self.entryTraceUsername, 0))
        entryUsername = tk.Entry(frameUsername, borderwidth=0, bg=DS.startupD, insertbackground=DS.startupFG, fg=DS.startupFG, textvariable=self.entryTraceUsername)
        entryUsername.pack(padx=(3,12), side="right")
        #Password login entry and label
        framePassword = tk.Frame(frameEntries, bg=DS.startupBG)
        labelPassword = tk.Label(framePassword, text="Password:", bg=DS.startupBG, fg=DS.startupFG)
        labelPassword.pack(padx=7, side="left")
        self.entryTracePassword = tk.StringVar()
        self.entryTracePassword.set("")
        self.entryTracePassword.trace("w", lambda name, index, mode, entryTracePassword=self.entryTracePassword: 
            self.testEntry(self.entryTracePassword, 1))
        entryPassword = tk.Entry(framePassword, borderwidth=0, show="*", insertbackground=DS.startupFG, fg=DS.startupFG, bg=DS.startupD, textvariable=self.entryTracePassword)
        entryPassword.pack(padx=(3,12), side="right")
        frameRemember = tk.Frame(frameEntries, bg=DS.startupBG)
        labelRemember = tk.Label(frameRemember, text="Remember login", bg=DS.startupBG, fg=DS.startupFG)
        labelRemember.pack(padx=7, side="left")
        checkTraceRemember = tk.IntVar()
        checkTraceRemember.set(0)
        checkButtonRemember = tk.Checkbutton(frameRemember, borderwidth=0, variable=checkTraceRemember, bg=DS.startupBG, fg=DS.startupFG, onvalue=True, offvalue=False).pack(side="left")
        #Buttons to submit entyry boxes
        frameButtons = tk.Frame(frameLogin, bg=DS.startupBG)
        buttonLogin = tk.Button(frameButtons, borderwidth=0, text="Login", width=12, bg=DS.startupD, fg=DS.startupFG, command=lambda: 
            self.login(self.entryTraceUsername.get(), self.entryTracePassword.get(), checkTraceRemember.get(), controller))
        buttonLogin.bind('<Return>', lambda: self.login(lambda: self.entryTraceUsername.get(), lambda: self.entryTracePassword.get(), checkTraceRemember.get(), controller))
        buttonLogin.pack(padx=5, side="left")
        buttonCreateAccount = tk.Button(frameButtons, borderwidth=0, bg=DS.startupD, fg=DS.startupFG, text="Create Account", width=12,
            command=lambda: controller.show_frame("Haze_Create"))
        buttonCreateAccount.pack(padx=5, side="left")
        self.prevList = ["", ""]
        #Logo
        frameLogo = tk.Frame(frameLogin)
        imageW = 114
        imageH = 64
        self.canvasLogo = tk.Canvas(frameLogo, width=imageW, height=imageH, bg=DS.startupBG, bd=0, highlightthickness=0)
        self.canvasLogo.pack()
        self.imageLogo = tk.PhotoImage(file="Haze.gif")
        self.canvasLogo.create_image(imageW/2, imageH/2, image=self.imageLogo)
        #Packing
        frameTitle.grid(row=0)
        frameUsername.grid(row=0, pady=3, sticky="e")
        framePassword.grid(row=1, pady=3, sticky="e")
        frameRemember.grid(row=2, pady=3, sticky="s")
        frameEntries.grid(row=1, pady=(8,12), sticky="e")
        frameButtons.grid(row=2, pady=(0, 20))
        frameLogo.grid(row=3)
        frameLogin.pack(fill="x", padx=10)

    #Tests if submitted user exists and if the password is correct, if yes destroy the login window and draw the main window
    def login(self, username, password, checkTraceRemember, controller):
        global path, app
        try:
            user = DictionaryReader(str(path) + "/users/" + str(username) + "/config")
        except Exception as e:
            print(e)
            raiseError("Username or Password is incorrect")
            print("username")
        else:
            if password != user["password"]:
                print("Password")
                raiseError("Username or Password is incorrect")
            else:
                with open(path+"/config/config.txt", "w") as config:
                    print()
                    if checkTraceRemember:
                        config.write('{\n\t"logged": "True",\n\t"currentUser": "' + str(username) + '",\n\t"currency": "' + str(user["currency"]) + '"\n}')
                    else:
                        config.write('{\n\t"logged": "False",\n\t"currentUser": "None"\n}')
                    config.close()
                app.destroy()
                app = HazeMain()
                app.resizable(False, False)
                app.geometry("{}x{}".format(600, 400))
                app.mainloop()

    #Disallows space character
    def testEntry(self, entry, index):
        userInput = entry.get()
        if " " in userInput:
            entry.set(self.prevList[index])
        else:
            self.prevList[index] = userInput

class Haze_Create(tk.Frame):
    def __init__(self, parent, controller):
        #This class draws the create an account frame for the startup window
        #The frame allows the user to create an account locally
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #Main frame
        frameCreate = tk.Frame(self, bg=DS.startupBG)
        #Title
        frameTitle = tk.Frame(frameCreate, bg=DS.startupBG)
        labelTitle = tk.Label(frameTitle, text="Create Account", font=controller.title_font, bg=DS.startupBG, fg=DS.startupFG)
        labelTitle.pack(side="top", fill="x", pady=10)
        #Create account entries
        frameEntries = tk.Frame(frameCreate, bg=DS.startupBG)
        #Username entry and label
        frameUsername = tk.Frame(frameEntries, bg=DS.startupBG)
        labelUsername = tk.Label(frameUsername, text="Username:", bg=DS.startupBG, fg=DS.startupFG)
        labelUsername.pack(padx=(20,7), side="left")
        self.entryTraceUsername = tk.StringVar()
        self.entryTraceUsername.set("")
        self.entryTraceUsername.trace("w", lambda name, index, mode, entryTraceUsername=self.entryTraceUsername: 
            self.testSpace(self.entryTraceUsername, 3))
        entryUsername = tk.Entry(frameUsername, borderwidth=0, textvariable=self.entryTraceUsername, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryUsername.pack(padx=3, side="right")
        #Email entry and label
        frameEmail = tk.Frame(frameEntries, bg=DS.startupBG)
        labelEmail = tk.Label(frameEmail, text="Email:", bg=DS.startupBG, fg=DS.startupFG)
        labelEmail.pack(padx=7, side="left")
        self.entryTraceEmail = tk.StringVar()
        self.entryTraceEmail.set("")
        self.entryTraceEmail.trace("w", lambda name, index, mode, entryTraceEmail=self.entryTraceEmail: 
            self.testSpace(self.entryTraceEmail, 4))
        entryEmail = tk.Entry(frameEmail, borderwidth=0, textvariable=self.entryTraceEmail, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryEmail.pack(padx=3, side="right")
        #Password entry and label
        framePassword = tk.Frame(frameEntries, bg=DS.startupBG)
        labelPassword = tk.Label(framePassword, text="Password:", bg=DS.startupBG, fg=DS.startupFG)
        labelPassword.pack(padx=7, side="left")
        self.entryTracePassword = tk.StringVar()
        self.entryTracePassword.set("")
        self.entryTracePassword.trace("w", lambda name, index, mode, entryTracePassword=self.entryTracePassword: 
            self.testSpace(self.entryTracePassword, 5))
        entryPassword = tk.Entry(framePassword, borderwidth=0, textvariable=self.entryTracePassword, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryPassword.pack(padx=3, side="right")
        #DOB title
        frameDOB = tk.Frame(frameEntries, bg=DS.startupBG)
        labelDOBTitle = tk.Label(frameDOB, text="Date of birth:", bg=DS.startupBG, fg=DS.startupFG)
        labelDOBTitle.pack(padx=(20,7), pady=5, side="top")
        #Day entry and label
        labelD = tk.Label(frameDOB, text="DD:", bg=DS.startupBG, fg=DS.startupFG)
        labelD.pack(padx=(7, 0), side="left")
        self.entryTraceD = tk.StringVar()
        self.entryTraceD.set("")
        self.entryTraceD.trace("w", lambda name, index, mode, entryTracePassword=self.entryTraceD: 
            self.testDate(self.entryTraceD.get(), self.entryTraceD, 2, 0))
        entryD = tk.Entry(frameDOB, borderwidth=0, textvariable=self.entryTraceD, width=3, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryD.pack(padx=1, side="left",)
        #Month entry and label
        labelM = tk.Label(frameDOB, text="MM:", bg=DS.startupBG, fg=DS.startupFG)
        labelM.pack(padx=1, side="left")
        self.entryTraceM = tk.StringVar()
        self.entryTraceM.set("")
        self.entryTraceM.trace("w", lambda name, index, mode, entryTraceM=self.entryTraceM: 
            self.testDate(self.entryTraceM.get(), self.entryTraceM, 2, 1))
        entryM = tk.Entry(frameDOB, borderwidth=0, textvariable=self.entryTraceM, width=3, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryM.pack(padx=1, side="left")
        #Year entry and lbel
        labelY = tk.Label(frameDOB, text="YYYY:", bg=DS.startupBG, fg=DS.startupFG)
        labelY.pack(padx=1, side="left")
        self.entryTraceY = tk.StringVar()
        self.entryTraceY.set("")
        self.entryTraceY.trace("w", lambda name, index, mode, entryTraceY=self.entryTraceY: 
            self.testDate(self.entryTraceY.get(), self.entryTraceY, 4, 2))
        entryY = tk.Entry(frameDOB, borderwidth=0, textvariable=self.entryTraceY, width=6, insertbackground=DS.startupFG, bg=DS.startupD, fg=DS.startupFG)
        entryY.pack(padx=(1, 11), side="left")
        self.prevList = ["", "", "", "", "", ""]
        #Submit buttons
        frameButtons = tk.Frame(frameCreate, bg=DS.startupBG)
        buttonCreateAccount = tk.Button(frameButtons, borderwidth=0, text="Create Account", bg=DS.startupD, fg=DS.startupFG, command=lambda: 
            self.createAccount(self.entryTraceUsername.get(), self.entryTraceEmail.get(), self.entryTracePassword.get(),
                self.formatDOB(entryD.get(), entryM.get(), entryY.get())))
        buttonCreateAccount.pack(side="left", padx=10)
        buttonLogin = tk.Button(frameButtons, borderwidth=0, text="Back to login", bg=DS.startupD, fg=DS.startupFG, command=lambda: self.resetCreate(controller))
        buttonLogin.pack(side="left", padx=(10,4))
        #Error Message
        frameError = tk.Frame(frameCreate, bg=DS.startupBG)
        self.labelErrorVar = tk.StringVar()
        labelError = tk.Label(frameError, bg=DS.startupBG, fg=DS.startupFG, textvariable=self.labelErrorVar)
        labelError.pack(anchor="center")
        self.labelErrorVar.set("")
        #Packing
        frameTitle.grid(row=0)
        frameList = [frameUsername, frameEmail, framePassword, frameDOB]
        for frame in range(0, len(frameList)):
            frameList[frame].grid(row=frame, pady=3, sticky="e")
        frameEntries.grid(row=1, pady=(8, 12), sticky="e")
        frameButtons.grid(row=2, pady=(0, 20))
        frameError.grid(row=3)
        frameCreate.pack(fill="x")

    #Tests for space character in entry
    def testSpace(self, entry, index):
        userInput = entry.get()
        if " " in userInput:
            entry.set(self.prevList[index])
        else:
            self.prevList[index] = entry

    #Resets user inputs 
    def resetCreate(self, controller):
        for entry in [self.entryTraceUsername, self.entryTracePassword, self.entryTraceEmail,
        self.entryTraceD, self.entryTraceM, self.entryTraceY, self.labelErrorVar]:
            entry.set("")
        controller.show_frame("Haze_Login")

    #Validates users input
    def testDate(self, userInput, label, labelMax, index):
        if len(userInput) <= labelMax and userInput.isnumeric() or userInput == "":
            label.set(userInput)
            self.prevList[index] = userInput
        else:
            label.set(self.prevList[index])

    #Validates entered info
    def formatDate(self, date):  
        if date == "":
            return int(99999)
        if date[0] == "0":
            return int(date[1])
        else:
            return int(date)

    #Tests for Errors in DOB
    def formatDOB(self, day, month, year):
        Return = []
        day = self.formatDate(day)
        month = self.formatDate(month)
        if month > 12:
            Return += ["Day and Month"]
        elif not (day<=29 and month==2) and not (day<=30 and month in [4,7,9,11]) and not (day<=31 and month in [1,3,5,6,8,10,12]):
            Return += ["Day"]
        if year == "":
            Return += ["Year"]
        else:
            if int(year) < 1920 or int(year) > 2018:
                Return += ["Year"]
        if Return == []:
            Return = str("(" + str(day) + "/" + str(month) + "/" + str(year) + ")")
        return Return
    
    #Validates entered info based on determined rules
    def createAccount(self, username, email, password, dob, controller):
        global app, path
        errorList = ""
        if username in userList:
            errorList += "Username is already taken\n"
        elif username == "":
            errorList += "Enter a username\n"
        elif len(username) > 25:
            errorList += "Username must be less than 25 characters\n"
        if password == "":
            errorList += "Enter a password\n"
        if email in emailList:
            errorList += "Email is already in use\n"
        elif email == "" or "@" not in email:
            errorList += "Enter an Email\n"
        if type(dob) is list:
            for error in dob:
                errorList += str(str(error) + " is incorrect\n")
        if errorList == "":
            CreatorPath = str(path) + "/users/" + str(username)
            try:
                os.makedirs(CreatorPath)
            except:
                pass
            with open(CreatorPath+str("/config.txt"), "w+") as newUser:
                newUser.write('{\n\t"username": "'+str(username)+'",\n\t"password": "'+str(password)+'",\n\t"email": "'+str(email)+'",\n\t"DOB": "'+str(dob)+'"\n\t"currency": "NZD"\n}')
            gamesLibraryPath = str(CreatorPath+"/gamesLibrary.txt")   
            with open(gamesLibraryPath, "w+") as newGameLib:
                newGameLib.write('{\n\t"games" : "none"\n}')
            CurrentUser(username, email, password, dob, "NZD")
            app.destroy()
            app = HazeMain()
            app.resizable(False, False)
            app.mainloop()
        else:
            self.labelErrorVar.set(str(errorList))

class Haze_Main(tk.Frame):
    def __init__(self, parent, controller):
        #This class draws the main home frame for the main window
        #The frame displays a welcome message, the users top 2 played games aswell as the games on sale currently
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global buttonList
        lineStyle = "#084258"
        frameMain = tk.Frame(self, bg=DS.mainBG)
        #Header
        frameHeaderBar = tk.Frame(frameMain, bg=DS.mainBG)
        headerFont = tkfont.Font(family='Arial', size=16, weight="bold")
        self.labelStore = tk.Label(frameHeaderBar, text="Store", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelStore.bind("<Button-1>", lambda event: controller.show_frame("Haze_Store"))
        self.labelStore.bind("<Enter>", lambda event: self.on_enter(self.labelStore))
        self.labelStore.bind("<Leave>", lambda event: self.on_leave(self.labelStore))
        self.labelStore.grid(column=0, row=0, padx=26, pady=8)
        self.labelLibrary = tk.Label(frameHeaderBar, text="Library", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLibrary.bind("<Button-1>", lambda event: controller.show_frame("Haze_Library"))
        self.labelLibrary.bind("<Enter>", lambda event: self.on_enter(self.labelLibrary))
        self.labelLibrary.bind("<Leave>", lambda event: self.on_leave(self.labelLibrary))
        self.labelLibrary.grid(column=1, row=0, padx=26, pady=8)
        self.labelSettings = tk.Label(frameHeaderBar, text="Settings", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelSettings.bind("<Button-1>", lambda event: controller.show_frame("Haze_Settings"))
        self.labelSettings.bind("<Enter>", lambda event: self.on_enter(self.labelSettings))
        self.labelSettings.bind("<Leave>", lambda event: self.on_leave(self.labelSettings))
        self.labelSettings.grid(column=2, row=0, padx=26, pady=8)
        self.labelLogout = tk.Label(frameHeaderBar, text="Logout", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLogout.bind("<Button-1>", lambda event: self.Logout())
        self.labelLogout.bind("<Enter>", lambda event: self.on_enter(self.labelLogout))
        self.labelLogout.bind("<Leave>", lambda event: self.on_leave(self.labelLogout))
        self.labelLogout.grid(column=3, row=0, padx=(95,26), pady=8)
        headerLine = tk.Canvas(frameHeaderBar, height=2, width=570, bd=0, highlightthickness=0, bg=lineStyle)
        headerLine.grid(row=1, padx=10, column=0, columnspan=4)
        frameHeaderBar.grid(row=0)
        #Main content
        titleFont = tkfont.Font(family='Arial', size=14, weight="bold")
        contentFont = tkfont.Font(family='Arial', size=12)
        frameMainFrame = tk.Frame(frameMain, bg=DS.mainBG)
        #Welcome
        frameWelcome = tk.Frame(frameMainFrame, bg=DS.mainBG)
        labelWelcome = tk.Label(frameWelcome, text="Welcome To Haze", font=titleFont, bg=DS.mainBG, fg=DS.mainFG)
        labelWelcome.grid(padx=25)
        frameWelcome.grid(row=0, column=0, pady=20)
        #Lines
        welcomeLine = tk.Canvas(frameMainFrame, height=2, width=200, bd=0, highlightthickness=0, bg=lineStyle)
        welcomeLine.grid(row=1, padx=10, column=0)
        midLine = tk.Canvas(frameMainFrame, height=300, bd=0, highlightthickness=0, width=2, bg=lineStyle)
        midLine.grid(row=0, column=1, padx=(16,0), rowspan=3, pady=0)
        #Promos
        self.gamesLibrary = list(DictionaryReader("config/gamesLibrary").items())
        self.saleInfo = list(DictionaryReader("config/saleInfo").items())
        saleFont = tkfont.Font(family='Arial', size=20, weight="bold")
        fontS = tkfont.Font(family="Arial", overstrike=1, size=10)
        framePromos = tk.Frame(frameMainFrame, bg=DS.mainBG)
        labelPromos = tk.Label(framePromos, text="Promotions", font=tkfont.Font(family='Arial', size=18, weight="bold"), bg=DS.mainBG, fg=DS.mainFG)
        labelPromos.grid(row=0, pady=(2, 18))
        #If the saleInfo file fails, tell user else display the sales set in saleInfo.txt
        if len(self.saleInfo) < 2:
            errorLabel = tk.Label(labelPromos, text="Sale info not found\nDouble check you have the\nsaleInfo.txt file").grid()
        else:
            #Promo 1
            framePromo1 = tk.Frame(framePromos, bg=DS.startupD)
            labelPromo1Var = tk.StringVar()
            labelPromo1Var.set(self.gamesLibrary[int(self.saleInfo[0][0])][1]["title"])
            labelPromo1Title = tk.Label(framePromo1, textvariable=labelPromo1Var, font=titleFont, bg=DS.startupD, fg=DS.mainFG)
            labelPromo1Title.grid(row=0, column=0, pady=10, columnspan=2)
            framePromo1Frame = tk.Frame(framePromo1, bg=DS.startupD)
            labelPromo1RedSVar = tk.StringVar()
            labelPromo1RedSVar.set(self.DisplaySale(0, False))
            labelPromo1RedS = tk.Label(framePromo1Frame, textvariable=labelPromo1RedSVar, bg=DS.startupD, fg=DS.mainFG, font=fontS)
            labelPromo1RedS.grid(row=0, column=0)
            labelPromo1RedVar = tk.StringVar()
            labelPromo1RedVar.set(self.DisplaySale(0, True))
            labelPromo1Red = tk.Label(framePromo1Frame, textvariable=labelPromo1RedVar, bg=DS.startupD, fg=DS.mainFG)
            labelPromo1Red.grid(row=1, column=0)
            framePromo1Frame.grid(row=1, column=0, padx=25, pady=10)
            labelPromo1SaleVar = tk.StringVar()
            labelPromo1SaleVar.set("-" + str('%.3g'%(100 - self.saleInfo[0][1]*100)) + "%")
            labelPromo1Sale = tk.Label(framePromo1, textvariable=labelPromo1SaleVar, font=saleFont, bg=DS.startupD, fg=DS.mainFG)
            labelPromo1Sale.grid(row=1, column=1, padx=10)
            framePromo1.grid(row=1, column=0, pady=5, rowspan=2)
            #Promo 2
            framePromo2 = tk.Frame(framePromos, bg=DS.startupD)
            labelPromo2Var = tk.StringVar()
            labelPromo2Var.set(self.gamesLibrary[int(self.saleInfo[1][0])][1]["title"])
            labelPromo2Title = tk.Label(framePromo2, textvariable=labelPromo2Var, font=titleFont, bg=DS.startupD, fg=DS.mainFG)
            labelPromo2Title.grid(row=0, column=0, pady=10, columnspan=2)
            framePromo2Frame = tk.Frame(framePromo2, bg=DS.startupD)
            labelPromo2RedSVar = tk.StringVar()
            labelPromo2RedSVar.set(self.DisplaySale(1, False))
            labelPromo2RedS = tk.Label(framePromo2Frame, textvariable=labelPromo2RedSVar, bg=DS.startupD, fg=DS.mainFG, font=fontS)
            labelPromo2RedS.grid(row=0, column=0)
            labelPromo2RedVar = tk.StringVar()
            labelPromo2RedVar.set(self.DisplaySale(1, True))
            labelPromo2Red = tk.Label(framePromo2Frame, textvariable=labelPromo2RedVar, bg=DS.startupD, fg=DS.mainFG)
            labelPromo2Red.grid(row=1, column=0)
            framePromo2Frame.grid(row=1, column=0, padx=25, pady=10)
            labelPromo2SaleVar = tk.StringVar()
            labelPromo2SaleVar.set("-" + str('%.3g'%(100 - self.saleInfo[1][1]*100)) + "%")
            labelPromo2Sale = tk.Label(framePromo2, textvariable=labelPromo2SaleVar, font=saleFont, bg=DS.startupD, fg=DS.mainFG)
            labelPromo2Sale.grid(row=1, column=1, padx=10)
            framePromo2.grid(row=3, column=0, pady=15, rowspan=2)
        framePromos.grid(padx=(40,20), row=0, column=2, rowspan=6, pady=16)
        #Quick
        frameQuick = tk.Frame(frameMainFrame, bg=DS.mainBG)
        labelQuick = tk.Label(frameQuick, text="Quick Access", font=titleFont, bg=DS.mainBG, fg=DS.mainFG)
        labelQuick.grid(row=0, pady=(0, 20))
        #Quick 1
        #If the users library is too small to display, tell them else display their most played game
        if currentUser.sortedPlayed == "Empty":
            frameEmpty = tk.Frame(frameQuick, bg=DS.startupD) 
            labelEmpty = tk.Label(frameEmpty, bg=DS.startupD, fg=DS.startupFG, text="Your library is empty", font=tkfont.Font(family="Arial", size=16, weight="bold"))
            labelEmpty.grid(row=0, column=0, pady=(12,8))
            labelEmpty2 = tk.Label(frameEmpty, bg=DS.startupD, fg=DS.startupFG, text="Expand it by visiting the store page", font=tkfont.Font(family="Arial", size=10, weight="bold"))
            labelEmpty2.grid(row=1, column=0, pady=(0, 28))
            frameEmpty.grid(row=1, column=0, pady=32, padx=23)
        else:
            frameQuickLinks = tk.Frame(frameQuick, bg=DS.startupD)
            #Quick 1
            frameQuick1 = tk.Frame(frameQuickLinks, bg=DS.startupD) 
            quick1Game = currentUser.sortedPlayed[0][1]["title"]
            varQuick1Title = tk.StringVar()
            varQuick1Title.set(quick1Game)
            labelQuick1Title = tk.Label(frameQuick1, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick1Title, font=tkfont.Font(family='Arial', size=12, weight="bold"))
            labelQuick1Title.grid(row=0, column=0, columnspan=2, padx=(10,2))
            varQuick1Time = tk.StringVar()
            varQuick1Time.set("You've played: " + str('%.3g'%(int(currentUser.sortedPlayed[0][1]["timePlayed"] / 60))) + " hours")
            lableQuick1Time = tk.Label(frameQuick1, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick1Time, font=tkfont.Font(family="Arial", size=9))
            lableQuick1Time.grid(row=1, column=0, padx=10)
            buttonVar1 = tk.StringVar()
            buttonVar1.set("Play")
            buttonPlay1 = tk.Button(frameQuickLinks, state="normal", bg=DS.mainHover, fg=DS.mainFG, command=lambda: LaunchGame(quick1Game), text="Play", font=tkfont.Font(family="Arial", size=10))
            buttonPlay1.grid(sticky="w", row=0, column=1, rowspan=1, padx=10, ipadx=2, pady=3)
            buttonList += [buttonPlay1]
            frameQuick1.grid(row=0, column=0, pady=(10,6), ipadx=10)
            #Quick 2
            frameQuick2 = tk.Frame(frameQuickLinks, bg=DS.startupD) 
            quick2Game = currentUser.sortedPlayed[1][1]["title"]
            varQuick2Title = tk.StringVar()
            varQuick2Title.set(quick2Game)
            labelQuick2Title = tk.Label(frameQuick2, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick2Title, font=tkfont.Font(family='Arial', size=12, weight="bold"))
            labelQuick2Title.grid(row=0, column=0, columnspan=2, padx=(10,2))
            varQuick2Time = tk.StringVar()
            varQuick2Time.set("You've played: " + str('%.3g'%(int(currentUser.sortedPlayed[1][1]["timePlayed"] / 60))) + " hours")
            lableQuick2Time = tk.Label(frameQuick2, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick2Time, font=tkfont.Font(family="Arial", size=9))
            lableQuick2Time.grid(row=1, column=0, padx=10)
            buttonVar2 = tk.StringVar()
            buttonVar2.set("Play")
            buttonPlay2 = tk.Button(frameQuickLinks, state="normal", bg=DS.mainHover, fg=DS.mainFG, command=lambda: LaunchGame(quick2Game), text="Play", font=tkfont.Font(family="Arial", size=10))
            buttonPlay2.grid(sticky="w", row=1, column=1, rowspan=1, padx=10, ipadx=2, pady=3)
            buttonList += [buttonPlay2]
            frameQuick2.grid(row=1, column=0, pady=(10,6), ipadx=10)
            #Quick 3
            frameQuick3 = tk.Frame(frameQuickLinks, bg=DS.startupD) 
            quick3Game = currentUser.sortedPlayed[2][1]["title"]
            varQuick3Title = tk.StringVar()
            varQuick3Title.set(quick3Game)
            labelQuick3Title = tk.Label(frameQuick3, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick3Title, font=tkfont.Font(family='Arial', size=12, weight="bold"))
            labelQuick3Title.grid(row=0, column=0, columnspan=2, padx=(10,2))
            varQuick3Time = tk.StringVar()
            varQuick3Time.set("You've played: " + str('%.3g'%(int(currentUser.sortedPlayed[2][1]["timePlayed"] / 60))) + " hours")
            lableQuick3Time = tk.Label(frameQuick3, bg=DS.startupD, fg=DS.mainFG, textvariable=varQuick3Time, font=tkfont.Font(family="Arial", size=9))
            lableQuick3Time.grid(row=1, column=0)
            buttonVar3 = tk.StringVar()
            buttonVar3.set("Play")
            buttonPlay3 = tk.Button(frameQuickLinks, state="normal", bg=DS.mainHover, fg=DS.mainFG, command=lambda: LaunchGame(quick3Game), text="Play", font=tkfont.Font(family="Arial", size=10))
            buttonPlay3.grid(sticky="w", row=2, column=1, rowspan=1, padx=10, ipadx=2, pady=3)
            buttonList += [buttonPlay3]
            frameQuick3.grid(row=2, column=0, pady=(10,6), ipadx=10)
            frameQuickLinks.grid(padx=20)
        frameQuick.grid(row=2, column=0, pady=20)

        frameMainFrame.grid()
        frameMain.grid()        

    #Formats the price before and after selected discount
    def DisplaySale(self, index, divide):
        display = str(currentUser.currency) + " $"
        if divide:
            display += str('%.3g'%(Converter((self.saleInfo[index][1] * self.gamesLibrary[int(self.saleInfo[index][0])][1]["price"]), currentUser.currency)-0.01))
        else:
            display += str('%.3g'%(Converter((self.gamesLibrary[int(self.saleInfo[index][0])][1]["price"]), currentUser.currency)-0.01))
        return display

    #Ask user if they want to logout
    def Logout(self):
        self.windowLogout = tk.Toplevel(bg=DS.mainBG)
        self.windowLogout.resizable(False, False)
        self.windowLogout.wm_title("Logout")
        frameButtons = tk.Frame(self.windowLogout, bg=DS.mainBG)
        labelLogoutMessage = tk.Label(self.windowLogout, fg=DS.mainFG, bg=DS.mainBG, text="Are you sure you want to log out?",
            font=tkfont.Font(family='Arial', size=10, weight="bold", slant="roman")).pack(pady=(18,8), padx=15)
        buttonYes = tk.Button(frameButtons, text="Yes", fg=DS.mainFG, bg=DS.mainBG, command=lambda: self.LogoutYes()).pack(padx=12, ipadx=8, pady=20, side="left")
        buttonNo = tk.Button(frameButtons, text="No", fg=DS.mainFG, bg=DS.mainBG, command=self.windowLogout.destroy).pack(padx=12, ipadx=8, pady=20, side="left")
        frameButtons.pack()

    #Logout user
    def LogoutYes(self):
        global app, path
        self.windowLogout.destroy()
        config = open(str(path)+"/config/config.txt", "w")
        config.write('{\n\t"logged": "False",\n\t"currentUser": ""\n\t"currency": "NZD"\n}')
        config.close()
        app.destroy()
        app = HazeStartup()
        app.resizable(False, False)
        app.mainloop()

    #Hover function
    def on_enter(self, who):
        who.config(fg=DS.mainHover)

    #Hover function
    def on_leave(self, who):
        who.config(fg=DS.mainFG)

class Haze_Library(tk.Frame):
    def __init__(self, parent, controller):
        #This class draws the library frame in the main window
        #This frame shows the user their games and displays relevant info for each game aswell as a play/install button and uninstall button
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lineStyle = "#084258"
        frameMain = tk.Frame(self, bg=DS.mainBG)
        frameHeaderBar = tk.Frame(frameMain, bg=DS.mainBG)
        headerFont = tkfont.Font(family='Arial', size=16, weight="bold")
        self.labelStore = tk.Label(frameHeaderBar, text="Store", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelStore.bind("<Button-1>", lambda event: controller.show_frame("Haze_Store"))
        self.labelStore.bind("<Enter>", lambda event: self.on_enter(self.labelStore))
        self.labelStore.bind("<Leave>", lambda event: self.on_leave(self.labelStore))
        self.labelStore.grid(column=0, row=0, padx=26, pady=8)
        self.labelHome = tk.Label(frameHeaderBar, text="Home", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelHome.bind("<Button-1>", lambda event: controller.show_frame("Haze_Main"))
        self.labelHome.bind("<Enter>", lambda event: self.on_enter(self.labelHome))
        self.labelHome.bind("<Leave>", lambda event: self.on_leave(self.labelHome))
        self.labelHome.grid(column=1, row=0, padx=32, pady=8)
        self.labelSettings = tk.Label(frameHeaderBar, text="Settings", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelSettings.bind("<Button-1>", lambda event: controller.show_frame("Haze_Settings"))
        self.labelSettings.bind("<Enter>", lambda event: self.on_enter(self.labelSettings))
        self.labelSettings.bind("<Leave>", lambda event: self.on_leave(self.labelSettings))
        self.labelSettings.grid(column=2, row=0, padx=26, pady=8)
        self.labelLogout = tk.Label(frameHeaderBar, text="Logout", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLogout.bind("<Button-1>", lambda event: self.Logout())
        self.labelLogout.bind("<Enter>", lambda event: self.on_enter(self.labelLogout))
        self.labelLogout.bind("<Leave>", lambda event: self.on_leave(self.labelLogout))
        self.labelLogout.grid(column=3, row=0, padx=(95,26), pady=8)
        headerLine = tk.Canvas(frameHeaderBar, height=2, width=570, bd=0, highlightthickness=0, bg=lineStyle)
        headerLine.grid(row=1, padx=10, column=0, columnspan=4)
        frameHeaderBar.grid(row=0)
        #Main content
        self.gamesLibrary = list(currentUser.gamesLibrary.items())
        titleFont = tkfont.Font(family='Arial', size=12, weight="bold")
        contentFont = tkfont.Font(family='Arial', size=12)
        frameMainFrame = tk.Frame(frameMain, bg=DS.mainBG)
        labelGamesTitle = tk.Label(frameMainFrame, bg=DS.mainBG, fg=DS.mainFG, text="Library", font=tkfont.Font(family="Arial", size=20, weight="bold"))
        labelGamesTitle.grid(row=0, column=0, pady=(14,0))
        frameGamesLibrary = tk.Frame(frameMainFrame, bg=DS.startupD)
        #Game 1
        frameGame1 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame1Var = tk.StringVar()
        self.TryDisplay(0, labelGame1Var)
        labelGame1Title = tk.Label(frameGame1, bg=DS.mainHover, fg=DS.mainFG, textvariable=labelGame1Var, font=titleFont)
        labelGame1Title.grid(row=0, column=0, ipadx=15)
        labelGame1Title.bind("<Button-1>", lambda event: self.DisplayGame(0, labelGame1Title))
        frameGame1.grid(sticky="w", row=0, column=0, pady=(10,1), ipadx=20)
        #Game 2
        frameGame2 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame2Var = tk.StringVar()
        self.TryDisplay(1, labelGame2Var)
        labelGame2Title = tk.Label(frameGame2, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame2Var, font=titleFont)
        labelGame2Title.grid(row=0, column=0, ipadx=15)
        labelGame2Title.bind("<Button-1>", lambda event: self.DisplayGame(1, labelGame2Title))
        frameGame2.grid(sticky="w", row=1, column=0, pady=1, ipadx=20)
        #Game 3
        frameGame3 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame3Var = tk.StringVar()
        self.TryDisplay(2, labelGame3Var)
        labelGame3Title = tk.Label(frameGame3, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame3Var, font=titleFont)
        labelGame3Title.grid(row=0, column=0, ipadx=15)
        labelGame3Title.bind("<Button-1>", lambda event: self.DisplayGame(2, labelGame3Title))
        frameGame3.grid(sticky="w", row=2, column=0, pady=1, ipadx=20)
        #Game 4
        frameGame4 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame4Var = tk.StringVar()
        self.TryDisplay(3, labelGame4Var)
        labelGame4Title = tk.Label(frameGame4, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame4Var, font=titleFont)
        labelGame4Title.grid(row=0, column=0, ipadx=15)
        labelGame4Title.bind("<Button-1>", lambda event: self.DisplayGame(3, labelGame4Title))
        frameGame4.grid(sticky="w", row=3, column=0, pady=1, ipadx=20)
        #Game 5
        frameGame5 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame5Var = tk.StringVar()
        self.TryDisplay(4, labelGame5Var)
        labelGame5Title = tk.Label(frameGame5, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame5Var, font=titleFont)
        labelGame5Title.grid(row=0, column=0, ipadx=15)
        labelGame5Title.bind("<Button-1>", lambda event: self.DisplayGame(4, labelGame5Title))
        frameGame5.grid(sticky="w", row=4, column=0, pady=1, ipadx=20)
        #Game 6
        frameGame6 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame6Var = tk.StringVar()
        self.TryDisplay(5, labelGame6Var)
        labelGame6Title = tk.Label(frameGame6, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame6Var, font=titleFont)
        labelGame6Title.grid(row=0, column=0, ipadx=15)
        labelGame6Title.bind("<Button-1>", lambda event: self.DisplayGame(5, labelGame6Title))
        frameGame6.grid(sticky="w", row=5, column=0, pady=1, ipadx=20)
        #Game 7
        frameGame7 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame7Var = tk.StringVar()
        self.TryDisplay(6, labelGame7Var)
        labelGame7Title = tk.Label(frameGame7, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame7Var, font=titleFont)
        labelGame7Title.grid(row=0, column=0, ipadx=15)
        labelGame7Title.bind("<Button-1>", lambda event: self.DisplayGame(6, labelGame7Title))
        frameGame7.grid(sticky="w", row=6, column=0, pady=1, ipadx=20)
        #Game 8
        frameGame8 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame8Var = tk.StringVar()
        self.TryDisplay(7, labelGame8Var)
        labelGame8Title = tk.Label(frameGame8, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame8Var, font=titleFont)
        labelGame8Title.grid(row=0, column=0, ipadx=15)
        labelGame8Title.bind("<Button-1>", lambda event: self.DisplayGame(7, labelGame8Title))
        frameGame8.grid(sticky="w", row=7, column=0, pady=1, ipadx=20)
        #Game 9
        frameGame9 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame9Var = tk.StringVar()
        self.TryDisplay(8, labelGame9Var)
        labelGame9Title = tk.Label(frameGame9, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame9Var, font=titleFont)
        labelGame9Title.grid(row=0, column=0, ipadx=15)
        labelGame9Title.bind("<Button-1>", lambda event: self.DisplayGame(8, labelGame9Title))
        frameGame9.grid(sticky="w", row=8, column=0, pady=1, ipadx=20)
        #Game 10
        frameGame10 = tk.Frame(frameGamesLibrary, bg=DS.startupD)
        labelGame10Var = tk.StringVar()
        self.TryDisplay(9, labelGame10Var)
        labelGame10Title = tk.Label(frameGame10, bg=DS.startupD, fg=DS.mainFG, textvariable=labelGame10Var, font=titleFont)
        labelGame10Title.grid(row=0, column=0, ipadx=15)
        labelGame10Title.bind("<Button-1>", lambda event: self.DisplayGame(9, labelGame10Title))
        frameGame10.grid(sticky="w", row=9, column=0, pady=1, ipadx=20)
        frameGamesLibrary.grid(sticky="w", row=1, column=0, padx=(28,20), ipadx=12, ipady=4)

        #Divider
        midLine = tk.Canvas(frameMainFrame, height=300, bd=0, highlightthickness=0, width=2, bg=lineStyle)
        midLine.grid(row=0, column=1, padx=(16,0), rowspan=3)

        #Main display
        frameGamesDisplay = tk.Frame(frameMainFrame, bg=DS.mainBG)
        self.currentIndex = 0
        frameTitle = tk.Frame(frameGamesDisplay, bg=DS.mainBG)
        self.labelMainVar = tk.StringVar()
        self.labelMainVar.set(self.gamesLibrary[self.currentIndex][1]["title"])
        labelMainTitle = tk.Label(frameTitle, textvariable=self.labelMainVar, fg=DS.mainFG, bg=DS.mainBG, font=tkfont.Font(family="Arial", size=16, weight="bold"))
        labelMainTitle.grid(row=0, column=0)
        #VR
        self.labelVRVar = tk.StringVar()
        self.labelVRVar.set("")
        labelVR = tk.Label(frameTitle, bg=DS.mainBG, fg=DS.mainFG, textvariable=self.labelVRVar)
        labelVR.grid(row=0, column=1, padx=2, pady=(0, 4))
        frameTitle.grid(sticky="w", row=0, column=0, padx=30)
        #Time played
        self.labelTimePlayedVar = tk.StringVar()
        self.labelTimePlayedVar.set("You've played: " + str('%.2g'%(int(self.gamesLibrary[self.currentIndex][1]["timePlayed"])/60)) + " hours")
        labelTimePlayed = tk.Label(frameGamesDisplay, bg=DS.startupD, fg=DS.mainFG, textvariable=self.labelTimePlayedVar, font=tkfont.Font(family='Arial', size=8))
        labelTimePlayed.grid(sticky="w", row=1, column=0, padx=30, pady=(6,30))
        #Developer and Publisher info
        self.labelDevVar = tk.StringVar()
        self.labelDevVar.set("Developer: " + str(self.gamesLibrary[self.currentIndex][1]["developer"]))
        labelDev = tk.Label(frameGamesDisplay, textvariable=self.labelDevVar, font=tkfont.Font(family="Arial", size=10), bg=DS.mainBG, fg=DS.mainFG)
        labelDev.grid(sticky="w", row=2, column=0, padx=30)
        self.labelPubVar = tk.StringVar()
        self.labelPubVar.set("Publisher: " + str(self.gamesLibrary[self.currentIndex][1]["publisher"]))
        labelPub = tk.Label(frameGamesDisplay, textvariable=self.labelPubVar, font=tkfont.Font(family="Arial", size=10), bg=DS.mainBG, fg=DS.mainFG)
        labelPub.grid(sticky="w", row=3, column=0, padx=30)
        self.buttonGameVar = tk.StringVar()
        self.buttonGameVar.set("Play")
        self.buttonGame = tk.Button(frameGamesDisplay, textvariable=self.buttonGameVar, font=tkfont.Font(family="Arial", size=12), bg=DS.mainHover, fg=DS.mainFG, command=lambda:
            self.InstallGame(self.currentIndex, self.InstallStatus(self.currentIndex)))
        self.buttonGame.grid(sticky="w", padx=32, pady=18, ipadx=10, ipady=3, row=4, column=0)
        self.buttonUninstall = tk.Button(frameGamesDisplay, text="Uninstall", font=tkfont.Font(family="Arial", size=10),
            bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.UninstallGame(self.currentIndex))
        self.buttonUninstall.grid(sticky="w", padx=32, pady=16, ipady=2, row=5, column=0)
        frameGamesDisplay.grid(row=0, column=2, rowspan=4, columnspan=2, sticky="e")
        self.InstallStatus(self.currentIndex)
        frameMainFrame.grid(sticky="w")
        frameMain.grid()  
        self.prevLabel = labelGame1Title
        global buttonList
        buttonList += [self.buttonGame]
        buttonList += [self.buttonUninstall]

    def TryDisplay(self, index, who):
        try:
            who.set(self.gamesLibrary[index][1]["title"])
        except:
            who.set(" ")

    #Updates the games library when the user installs/uninstalls a game
    def UpdateLibrary(self):
        currentUser.gamesLibrary = DictionaryReader(str(path)+"/users/"+str(currentUser.username)+"/gamesLibrary")
        self.gamesLibrary = list(currentUser.gamesLibrary.items())
        print(self.gamesLibrary)

    #Uninstalls the game the user has selected
    def UninstallGame(self, index):
        self.buttonUninstall["state"] = "disabled"
        self.buttonGameVar.set("Install")
        with open("users/" + str(currentUser.username) + "/gamesLibrary.txt", "r") as data:
            gamesLibrary = data.readlines()
            line = 1 + (9*(index+1)-4)
            gamesLibrary[line] = '\t\t"installed": "False",\n'
            with open ("users/" + str(currentUser.username) + "/gamesLibrary.txt", "w") as data:
                data.writelines(gamesLibrary)
                data.close()
            data.close()
        self.UpdateLibrary()

    #Installs the game the user has selected
    def InstallGame(self, index, install):
        if self.InstallStatus(self.currentIndex):
            self.buttonGameVar.set("Play")
            self.buttonUninstall["state"] = "normal"
            with open("users/" + str(currentUser.username) + "/gamesLibrary.txt", "r") as data:
                gamesLibrary = data.readlines()
                line = 1 + (9*(index+1)-4)
                gamesLibrary[line] = '\t\t"installed": "True",\n'
                with open ("users/" + str(currentUser.username) + "/gamesLibrary.txt", "w") as data:
                    data.writelines(gamesLibrary)
                    data.close()
                data.close()
            self.UpdateLibrary()
        else:
            LaunchGame(self.gamesLibrary[index][1]["title"])

    #Updates the states of relevant buttons
    def InstallStatus(self, index):
        if self.gamesLibrary[index][1]["installed"] == "False":
            self.buttonUninstall["state"] = "disabled"
            self.buttonGameVar.set("Install")
            return False
        else:
            self.buttonGameVar.set("Play")
            self.buttonUninstall["state"] = "normal"
            return True

    #Updates the display area with selected game info
    def DisplayGame(self, index, who):
        try:
            self.currentIndex = index
            self.prevLabel.config(bg=DS.startupD)
            self.labelMainVar.set(self.gamesLibrary[index][1]["title"])
            self.labelTimePlayedVar.set("You've played: " + str('%.2g'%(int(self.gamesLibrary[index][1]["timePlayed"])/60)) + " hours")
            self.labelDevVar.set("Developer: " + str(self.gamesLibrary[index][1]["developer"]))
            self.labelPubVar.set("Publisher: " + str(self.gamesLibrary[index][1]["publisher"]))
            if self.gamesLibrary[index][1]["vr"] == "True":
                self.labelVRVar.set("VR")
            else:
                self.labelVRVar.set("")
            who.config(bg=DS.mainHover)
            self.prevLabel = who
            self.InstallStatus(index)
        except:
            pass

    def on_enter(self, who):
        who.config(fg=DS.mainHover)

    def on_leave(self, who):
        who.config(fg=DS.mainFG)

    def Logout(self):
        self.windowLogout = tk.Toplevel(bg=DS.mainBG)
        self.windowLogout.resizable(False, False)
        self.windowLogout.wm_title("Logout")
        frameButtons = tk.Frame(self.windowLogout, bg=DS.mainBG)
        labelLogoutMessage = tk.Label(self.windowLogout, fg=DS.mainFG, bg=DS.mainBG, text="Are you sure you want to log out?",
            font=tkfont.Font(family='Arial', size=10, weight="bold", slant="roman")).pack(pady=(18,8), padx=15)
        buttonYes = tk.Button(frameButtons, text="Yes", fg=DS.mainFG, bg=DS.mainBG, command=lambda: self.LogoutYes()).pack(padx=12, ipadx=8, pady=20, side="left")
        buttonNo = tk.Button(frameButtons, text="No", fg=DS.mainFG, bg=DS.mainBG, command=self.windowLogout.destroy).pack(padx=12, ipadx=8, pady=20, side="left")
        frameButtons.pack()

    def LogoutYes(self):
        global app, path
        self.windowLogout.destroy()
        config = open(str(path)+"/config/config.txt", "w")
        config.write('{\n\t"logged": "False",\n\t"currentUser": ""\n\t"currency": "NZD"\n}')
        config.close()
        app.destroy()
        app = HazeStartup()
        app.resizable(False, False)
        app.mainloop()
        

class Haze_Store(tk.Frame):
    def __init__(self, parent, controller):
        #This class draws the store frame in the main window
        #This frame allows the user to buy games for their library
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lineStyle = "#084258"
        #Main
        frameMain = tk.Frame(self, bg=DS.mainBG)
        #Header
        frameHeaderBar = tk.Frame(frameMain, bg=DS.mainBG)
        headerFont = tkfont.Font(family='Arial', size=16, weight="bold")
        self.labelHome = tk.Label(frameHeaderBar, text="Home", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelHome.bind("<Button-1>", lambda event: controller.show_frame("Haze_Main"))
        self.labelHome.bind("<Enter>", lambda event: self.on_enter(self.labelHome))
        self.labelHome.bind("<Leave>", lambda event: self.on_leave(self.labelHome))
        self.labelHome.grid(column=0, row=0, padx=24, pady=8)
        self.labelLibrary = tk.Label(frameHeaderBar, text="Library", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLibrary.bind("<Button-1>", lambda event: controller.show_frame("Haze_Library"))
        self.labelLibrary.bind("<Enter>", lambda event: self.on_enter(self.labelLibrary))
        self.labelLibrary.bind("<Leave>", lambda event: self.on_leave(self.labelLibrary))
        self.labelLibrary.grid(column=1, row=0, padx=26, pady=8)
        self.labelSettings = tk.Label(frameHeaderBar, text="Settings", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelSettings.bind("<Button-1>", lambda event: controller.show_frame("Haze_Settings"))
        self.labelSettings.bind("<Enter>", lambda event: self.on_enter(self.labelSettings))
        self.labelSettings.bind("<Leave>", lambda event: self.on_leave(self.labelSettings))
        self.labelSettings.grid(column=2, row=0, padx=26, pady=8)
        self.labelLogout = tk.Label(frameHeaderBar, text="Logout", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLogout.bind("<Button-1>", lambda event: self.Logout())
        self.labelLogout.bind("<Enter>", lambda event: self.on_enter(self.labelLogout))
        self.labelLogout.bind("<Leave>", lambda event: self.on_leave(self.labelLogout))
        self.labelLogout.grid(column=3, row=0, padx=(95,26), pady=8)
        headerLine = tk.Canvas(frameHeaderBar, height=2, width=570, bd=0, highlightthickness=0, bg=lineStyle)
        headerLine.grid(row=1, padx=10, column=0, columnspan=4)
        frameHeaderBar.grid(row=0, sticky="w")
        #Main content
        self.gamesLibrary = list(DictionaryReader("config/gamesLibrary").items())
        self.saleInfo = list(DictionaryReader("config/saleInfo").items())
        titleFont = tkfont.Font(family='Arial', size=14, weight="bold")
        contentFont = tkfont.Font(family='Arial', size=12)
        fontS = tkfont.Font(family="Arial", overstrike=1, size=10)
        saleFont = tkfont.Font(family='Arial', size=20, weight="bold")
        frameMainFrame = tk.Frame(frameMain, bg=DS.mainBG)
        frameSale = tk.Frame(frameMainFrame, bg=DS.mainBG)
        labelSale = tk.Label(frameSale, bg=DS.mainBG, fg=DS.mainFG, font=tkfont.Font(family="Arial", size=18, weight="bold"), text="Sales")
        labelSale.grid(row=0, column=0, columnspan=2, padx=20, pady=6)
        #Sale 1
        frameSale1 = tk.Frame(frameSale, bg=DS.startupD)
        self.labelSale1Var = tk.StringVar()
        self.TryDisplay(0, self.labelSale1Var)
        labelSale1Title = tk.Label(frameSale1, textvariable=self.labelSale1Var, font=titleFont, bg=DS.startupD, fg=DS.mainFG)
        labelSale1Title.grid(row=0, column=0, pady=5, columnspan=2)
        frameSale1Frame = tk.Frame(frameSale1, bg=DS.startupD)
        labelSale1RedSVar = tk.StringVar()
        labelSale1RedSVar.set(self.DisplaySale(0, False))
        labelSale1RedS = tk.Label(frameSale1Frame, textvariable=labelSale1RedSVar, bg=DS.startupD, fg=DS.mainFG, font=fontS)
        labelSale1RedS.grid(row=0, column=0)
        labelSale1RedVar = tk.StringVar()
        labelSale1RedVar.set(self.DisplaySale(0, True))
        labelSale1Red = tk.Label(frameSale1Frame, textvariable=labelSale1RedVar, bg=DS.startupD, fg=DS.mainFG)
        labelSale1Red.grid(row=1, column=0)
        frameSale1Frame.grid(row=1, column=0, padx=25, pady=10)
        labelSale1SaleVar = tk.StringVar()
        labelSale1SaleVar.set("-" + str('%.3g'%(100 - self.saleInfo[0][1]*100)) + "%")
        labelSale1Sale = tk.Label(frameSale1, textvariable=labelSale1SaleVar, font=saleFont, bg=DS.startupD, fg=DS.mainFG)
        labelSale1Sale.grid(row=1, column=1, padx=10)
        self.buttonSale1 = tk.Button(frameSale1, text="Add to cart", bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.CartAdd(0, self.buttonSale1, self.labelPrice1Var))
        self.buttonSale1.grid(row=2, column=0, columnspan=2)
        frameSale1.grid(padx=20, row=1, column=0, ipady=5, pady=5)
        #Sale 2
        frameSale2 = tk.Frame(frameSale, bg=DS.startupD)
        self.labelSale2Var = tk.StringVar()
        self.TryDisplay(1, self.labelSale2Var)
        labelSale2Title = tk.Label(frameSale2, textvariable=self.labelSale2Var, font=titleFont, bg=DS.startupD, fg=DS.mainFG)
        labelSale2Title.grid(row=0, column=0, pady=5, columnspan=2)
        frameSale2Frame = tk.Frame(frameSale2, bg=DS.startupD)
        labelSale2RedSVar = tk.StringVar()
        labelSale2RedSVar.set(self.DisplaySale(1, False))
        labelSale2RedS = tk.Label(frameSale2Frame, textvariable=labelSale2RedSVar, bg=DS.startupD, fg=DS.mainFG, font=fontS)
        labelSale2RedS.grid(row=0, column=0)
        labelSale2RedVar = tk.StringVar()
        labelSale2RedVar.set(self.DisplaySale(1, True))
        labelSale2Red = tk.Label(frameSale2Frame, textvariable=labelSale2RedVar, bg=DS.startupD, fg=DS.mainFG)
        labelSale2Red.grid(row=1, column=0)
        frameSale2Frame.grid(row=1, column=0, padx=25, pady=10)
        labelSale2SaleVar = tk.StringVar()
        labelSale2SaleVar.set("-" + str('%.3g'%(100 - self.saleInfo[1][1]*100)) + "%")
        labelSale2Sale = tk.Label(frameSale2, textvariable=labelSale2SaleVar, font=saleFont, bg=DS.startupD, fg=DS.mainFG)
        labelSale2Sale.grid(row=1, column=1, padx=10)
        self.buttonSale2 = tk.Button(frameSale2, text="Add to cart", bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.CartAdd(1, self.buttonSale2, self.labelPrice2Var))
        self.buttonSale2.grid(row=2, column=0, columnspan=2)
        frameSale2.grid(row=3, column=0, ipady=5, pady=5, rowspan=2)
        frameSale.grid(row=0, column=0, rowspan=2)
        #Mid line
        midLine = tk.Canvas(frameMainFrame, height=300, bd=0, highlightthickness=0, width=2, bg=lineStyle)
        midLine.grid(row=0, column=1, rowspan=3)
        #Cart
        frameShoppingCart = tk.Frame(frameMainFrame, bg=DS.startupD)
        labelShoppingTitle = tk.Label(frameShoppingCart, bg=DS.startupD, fg=DS.mainFG, text="Shopping Cart", font=tkfont.Font(family="Arial", size=16, weight="bold"), padx=20)
        labelShoppingTitle.grid(row=0, column=0, pady=5, ipadx=50)
        #Shopping 1
        frameShopping1 = tk.Frame(frameShoppingCart, bg=DS.startupD)
        buttonX1 = tk.Button(frameShopping1, bg=DS.startupD, fg=DS.mainFG, text="X", font=tkfont.Font(family="Arial", size=6, weight="bold"), command=lambda: self.CartRemove(0))
        buttonX1.grid(row=0, column=0) 
        self.labelShopping1Var = tk.StringVar()
        self.labelShopping1Var.set("")
        labelShopping1 = tk.Label(frameShopping1, bg=DS.startupD, fg=DS.mainFG, textvariable=self.labelShopping1Var, font=contentFont)
        labelShopping1.grid(row=0, column=1, padx=3)
        self.labelPrice1Var = tk.StringVar()
        self.labelPrice1Var.set("")
        labelPrice1 = tk.Label(frameShopping1, bg=DS.startupD, fg=DS.mainFG, textvariable=self.labelPrice1Var, font=contentFont)
        labelPrice1.grid(row=0, column=2, padx=3)
        frameShopping1.grid(row=1, column=0, pady=2)
        #Shopping 2
        frameShopping2 = tk.Frame(frameShoppingCart, bg=DS.startupD)
        buttonX2 = tk.Button(frameShopping2, bg=DS.startupD, fg=DS.mainFG, text="X", font=tkfont.Font(family="Arial", size=6, weight="bold"), command=lambda: self.CartRemove(1))
        buttonX2.grid(row=0, column=0)
        self.labelShopping2Var = tk.StringVar()
        self.labelShopping2Var.set("")
        labelShopping2 = tk.Label(frameShopping2, bg=DS.startupD, fg=DS.mainFG, textvariable=self.labelShopping2Var, font=contentFont)
        labelShopping2.grid(row=0, column=1, padx=2)
        self.labelPrice2Var = tk.StringVar()
        self.labelPrice2Var.set("")
        labelPrice2 = tk.Label(frameShopping2, bg=DS.startupD, fg=DS.mainFG, textvariable=self.labelPrice2Var, font=contentFont)
        labelPrice2.grid(row=0, column=2, padx=3)
        frameShopping2.grid(row=2, column=0, pady=3)
        #Total label
        self.labelTotalVar = tk.StringVar()
        self.labelTotalVar.set("Total: $0")
        labelTotal = tk.Label(frameShoppingCart, textvariable=self.labelTotalVar, bg=DS.startupD, fg=DS.mainFG, font=titleFont)
        labelTotal.grid(row=3, column=0, padx=20, pady=6)
        #Checkout button
        buttonCheckout = tk.Button(frameShoppingCart, bg=DS.mainHover, fg=DS.mainFG, text="Checkout", font=tkfont.Font(family="Arial", size=10, weight="bold"), command=lambda: self.Checkout())
        buttonCheckout.grid(row=4, column=0, ipadx=12, ipady=4, padx=20)
        frameShoppingCart.grid(row=0, column=2, sticky="w", padx=20, pady=5, ipady=5)
        #Buy
        smallTitleFont = tkfont.Font(family="Arial", size=12, weight="bold")
        frameBuy = tk.Frame(frameMainFrame, bg=DS.mainBG)
        #Shopping 3
        frameShopping3 = tk.Frame(frameBuy, bg=DS.startupD)
        self.labelShopping3Var = tk.StringVar()
        self.TryDisplay(2, self.labelShopping3Var)
        labelShopping3 = tk.Label(frameShopping3, textvariable=self.labelShopping3Var, bg=DS.startupD, fg=DS.mainFG, font=smallTitleFont)
        labelShopping3.grid(row=0, column=0, pady=7, padx=19)
        labelPrice3Var = tk.StringVar()
        labelPrice3Var.set(self.DisplaySale(2, False))
        labelPrice3 = tk.Label(frameShopping3, textvariable=labelPrice3Var, bg=DS.startupD, fg=DS.mainFG, font=contentFont)
        labelPrice3.grid(row=0, column=1, padx=5)
        self.buttonBuy3 = tk.Button(frameShopping3, text="Add to cart", bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.CartAdd(2, self.buttonBuy3, labelPrice3Var))
        self.buttonBuy3.grid(row=0, column=2, padx=5)
        frameShopping3.grid(sticky="w", row=0, column=0)
        #Shopping 4
        frameShopping4 = tk.Frame(frameBuy, bg=DS.startupD)
        self.labelShopping4Var = tk.StringVar()
        self.TryDisplay(3, self.labelShopping4Var)
        labelShopping4 = tk.Label(frameShopping4, textvariable=self.labelShopping4Var, bg=DS.startupD, fg=DS.mainFG, font=smallTitleFont)
        labelShopping4.grid(row=0, column=0, pady=7, padx=10)
        labelPrice4Var = tk.StringVar()
        labelPrice4Var.set(self.DisplaySale(3, False))
        labelPrice4 = tk.Label(frameShopping4, textvariable=labelPrice4Var, bg=DS.startupD, fg=DS.mainFG, font=contentFont)
        labelPrice4.grid(row=0, column=1, padx=5)
        self.buttonBuy4 = tk.Button(frameShopping4, text="Add to cart", bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.CartAdd(3, self.buttonBuy4, labelPrice4Var))
        self.buttonBuy4.grid(row=0, column=2, padx=5)
        frameShopping4.grid(sticky="w", row=1, column=0)
        #Shopping 5
        frameShopping5 = tk.Frame(frameBuy, bg=DS.startupD)
        self.labelShopping5Var = tk.StringVar()
        self.TryDisplay(4, self.labelShopping5Var)
        labelShopping5 = tk.Label(frameShopping5, textvariable=self.labelShopping5Var, bg=DS.startupD, fg=DS.mainFG, font=smallTitleFont)
        labelShopping5.grid(row=0, column=0, pady=7, padx=21)
        labelPrice5Var = tk.StringVar()
        labelPrice5Var.set(self.DisplaySale(4, False))
        labelPrice5 = tk.Label(frameShopping5, textvariable=labelPrice5Var, bg=DS.startupD, fg=DS.mainFG, font=contentFont)
        labelPrice5.grid(row=0, column=1, padx=5)
        self.buttonBuy5 = tk.Button(frameShopping5, text="Add to cart", bg=DS.mainHover, fg=DS.mainFG, command=lambda: self.CartAdd(4, self.buttonBuy5, labelPrice5Var))
        self.buttonBuy5.grid(row=0, column=2, padx=5)
        frameShopping5.grid(sticky="w", row=2, column=0)
        self.buttonList = ["",""]
        self.allButtonList = [self.buttonSale1, self.buttonSale2, self.buttonBuy3, self.buttonBuy4, self.buttonBuy5]
        self.labelList = [self.labelSale1Var, self.labelSale2Var, self.labelShopping3Var, self.labelShopping4Var, self.labelShopping5Var]
        self.CheckStore()
        frameBuy.grid(row=1, column=2)
        frameMainFrame.grid(sticky="w")
        frameMain.grid(sticky="w")  

    #Attempt to display the title of the book based on given index
    def TryDisplay(self, index, who):
        try:
            who.set(self.gamesLibrary[int(self.saleInfo[index][0])][1]["title"])
        except:
            who.set("")
        self.CheckStore()

    def CheckStore(self):
        gamesLibrary = DictionaryReader("users/" + str(currentUser.username) + "/gamesLibrary.txt")
        for game in range(0, 5):
            try:
                if gamesLibrary[str(5+game)]["title"] == self.labelList[game].get():
                    self.allButtonList[game]["state"] = "disabled"
            except:
                pass

    #Checkout function draws a credit card window
    def Checkout(self):
        self.windowCheckout = tk.Toplevel(bg=DS.mainBG)
        self.windowCheckout.resizable(False, False)
        self.windowCheckout.wm_title("Checkout")
        frameCheckout = tk.Frame(self.windowCheckout, bg=DS.mainBG)
        #Title
        labelTitle = tk.Label(frameCheckout, text="Please enter you credit card", fg=DS.mainFG, bg=DS.mainBG, font=tkfont.Font(family="Arial", size=10))
        labelTitle.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        #Number
        labelNumber = tk.Label(frameCheckout, text="Number:", fg=DS.mainFG, bg=DS.mainBG)
        labelNumber.grid(row=1, column=0, padx=2, pady=10, columnspan=2)
        traceNumberEntry = tk.StringVar()
        entryNumber = tk.Entry(frameCheckout, textvariable=traceNumberEntry, borderwidth=0, insertbackground=DS.startupFG, fg=DS.startupFG, bg=DS.startupD)
        entryNumber.grid(row=1, column=2, padx=2, pady=10, columnspan=2)
        #Expiry
        labelExpiry = tk.Label(frameCheckout, text="Expiry:", fg=DS.mainFG, bg=DS.mainBG)
        labelExpiry.grid(row=2, column=0, padx=2, pady=10)
        traceExpiryEntry = tk.StringVar()
        entryExpiry = tk.Entry(frameCheckout, textvariable=traceExpiryEntry, borderwidth=0, insertbackground=DS.startupFG, fg=DS.startupFG, bg=DS.startupD, width=6)
        entryExpiry.grid(row=2, column=1, padx=2, pady=10)
        #CVV
        labelCVV = tk.Label(frameCheckout, text="CVV:", fg=DS.mainFG, bg=DS.mainBG)
        labelCVV.grid(row=2, column=2, padx=2, pady=10)
        traceCVVEntry = tk.StringVar()
        entryCVV = tk.Entry(frameCheckout, textvariable=traceCVVEntry, borderwidth=0, insertbackground=DS.startupFG, fg=DS.startupFG, bg=DS.startupD, width=4)
        entryCVV.grid(row=2, column=3, padx=2, pady=10)
        #Submit
        buttonSubmit = tk.Button(frameCheckout, text="Submit", command=lambda: self.SubmitCreditcard(traceNumberEntry.get(), traceExpiryEntry.get(), traceCVVEntry.get()), bg=DS.mainHover, fg=DS.mainFG)
        buttonSubmit.grid(row=3, column=1, columnspan=2)
        #Error Msg
        self.labelErrorVar = tk.StringVar()
        labelError = tk.Label(frameCheckout, textvariable=self.labelErrorVar, bg=DS.mainBG, fg=DS.mainFG)
        labelError.grid(row=4, column=1, columnspan=2)

        frameCheckout.grid(padx=20, pady=20)

    #Loosely checks whether the entered info is somewhat plausible and if yes, show success
    #Only needs 12 characters in the number section, 4 in the expiry and 3 in the cvv
    def SubmitCreditcard(self, number, expiry, cvv):
        errorList = ""
        if len(number) != 12:
            errorList += "Number\n"
        if len(expiry) != 4:
            errorList += "Expiry\n"
        if len(cvv) != 3:
            errorList += "CVV\n"
        if errorList == "":
            self.labelErrorVar.set("")
            self.windowSuccess = tk.Toplevel(bg=DS.mainBG)
            self.windowSuccess.resizable(False, False)
            self.windowSuccess.wm_title("Success")
            labelSuccess = tk.Label(self.windowSuccess, text="Successfully purchased", fg=DS.mainFG, bg=DS.mainBG, font=tkfont.Font(family="Arial", size=14, weight="bold")).grid(row=0, column=0, pady=10, padx=10)
            buttonAccept = tk.Button(self.windowSuccess, text="Ok", command=lambda: self.windowSuccess.destroy(), bg=DS.mainHover, fg=DS.mainFG).grid(row=1, column=0, pady=10, padx=20)
            with open("users/" + str(currentUser.username) + "/gamesLibrary.txt", "r") as file:
                gamesLibrary = file.readlines()
                del gamesLibrary[len(gamesLibrary)-1]
                gamesLibrary[len(gamesLibrary)-1] = "\t},\n"
                maxGame = int(gamesLibrary[len(gamesLibrary)-9].replace('\t"', '').replace('": {', ''))
                for game in range(0, 2):
                    if currentUser.shoppingCart[game] == "":
                        pass
                    else:
                        with open("config/gamesLibrary.txt", "r") as file:
                            realGamesLib = file.readlines()
                        start = 9*(maxGame+game+1)+1
                        gamesLibrary += '\t"' + str(maxGame+game+1) + '": {\n'
                        for lines in range(start+1, start+8):
                            print(realGamesLib[lines])
                            gamesLibrary += [realGamesLib[lines]]
                        if game == 0 and currentUser.shoppingCart[game] != "":
                            try:
                                if currentUser.shoppingCart[game+1] != "":
                                    gamesLibrary += "\t},\n"
                            except:
                                pass
                gamesLibrary += "\t}\n}" 
                with open("users/" + str(currentUser.username) + "/gamesLibrary.txt", "w") as file:
                    file.writelines(gamesLibrary)
                    file.close()
                file.close()
            Haze_Library.UpdateLibrary(Haze_Library)
            self.windowCheckout.destroy()
        else:
            errorList += "Are incorrect"
            self.labelErrorVar.set(errorList)

    #Calculates the total price of the shopping cart
    def CalculateCart(self):
        totalMsg = "Total: $"
        total = 0
        gameLib = []
        for item in range(0, 2):
            if currentUser.shoppingCart[item] == "":
                pass
            else:
                if item == 0:
                    price = self.labelPrice1Var.get() 
                else:
                    price = self.labelPrice2Var.get() 
                total += float(price.replace("NZD $", ""))
        totalMsg += str(total)
        self.labelTotalVar.set(totalMsg)
        self.CheckStore()

    #Adds the selected game to the shopping cart
    def CartAdd(self, index, who, var):
        if currentUser.shoppingCart[0] == "":
            currentUser.shoppingCart[0] = self.gamesLibrary[int(self.saleInfo[index][0])][1]
            self.labelPrice1Var.set(self.DisplaySale(index, True))
            self.labelShopping1Var.set(currentUser.shoppingCart[0]["title"])
            who["state"] = "disabled"
            self.buttonList[0] = who
            currentUser.cartIndexes[0] = 5+index
            self.CalculateCart()
        elif currentUser.shoppingCart[1] == "":
            currentUser.shoppingCart[1] = self.gamesLibrary[int(self.saleInfo[index][0])][1]
            self.labelPrice2Var.set(self.DisplaySale(index, True))
            self.labelShopping2Var.set(currentUser.shoppingCart[1]["title"])
            who["state"] = "disabled"
            self.buttonList[1] = who
            currentUser.cartIndexes[1] = 5+index
            self.CalculateCart()
        self.CheckStore()

    #Removes the selected game from the shopping cart
    def CartRemove(self, index):
        if index == 0:
            currentUser.shoppingCart[0] = ""
            self.labelPrice1Var.set("")
            self.labelShopping1Var.set("")
            self.buttonList[0]["state"] = "normal"
            currentUser.cartIndexes[0] = ""
            self.CalculateCart()
        elif index == 1:
            currentUser.shoppingCart[1] = ""
            self.labelPrice2Var.set("")
            self.labelShopping2Var.set("")
            self.buttonList[1]["state"] = "normal"
            currentUser.cartIndexes[1] = ""
            self.CalculateCart()
        self.CheckStore()
 
    #Formats the price before and after selected discount
    def DisplaySale(self, index, divide):
        self.CheckStore()
        try:
            display = str(currentUser.currency) + " $"
            if divide:
                display += str('%.3g'%(Converter((self.saleInfo[index][1] * self.gamesLibrary[int(self.saleInfo[index][0])][1]["price"]), currentUser.currency)-0.01))
            else:
                display += str('%.3g'%(Converter((self.gamesLibrary[int(self.saleInfo[index][0])][1]["price"]), currentUser.currency)-0.01))
            return display
        except:
            return ""

    def on_enter(self, who):
        who.config(fg=DS.mainHover)

    def on_leave(self, who):
        who.config(fg=DS.mainFG)

    def Logout(self):
        self.windowLogout = tk.Toplevel(bg=DS.mainBG)
        self.windowLogout.resizable(False, False)
        self.windowLogout.wm_title("Logout")
        frameButtons = tk.Frame(self.windowLogout, bg=DS.mainBG)
        labelLogoutMessage = tk.Label(self.windowLogout, fg=DS.mainFG, bg=DS.mainBG, text="Are you sure you want to log out?",
            font=tkfont.Font(family='Arial', size=10, weight="bold", slant="roman")).pack(pady=(18,8), padx=15)
        buttonYes = tk.Button(frameButtons, text="Yes", fg=DS.mainFG, bg=DS.mainBG, command=lambda: self.LogoutYes()).pack(padx=12, ipadx=8, pady=20, side="left")
        buttonNo = tk.Button(frameButtons, text="No", fg=DS.mainFG, bg=DS.mainBG, command=self.windowLogout.destroy).pack(padx=12, ipadx=8, pady=20, side="left")
        frameButtons.pack()

    def LogoutYes(self):
        global app, path
        self.windowLogout.destroy()
        config = open(str(path)+"/config/config.txt", "w")
        config.write('{\n\t"logged": "False",\n\t"currentUser": ""\n\t"currency": "NZD"\n}')
        config.close()
        app.destroy()
        app = HazeStartup()
        app.resizable(False, False)
        app.mainloop()

class Haze_Settings(tk.Frame):
    def __init__(self, parent, controller):
        #Settings frame for the main window
        #This frame allows the user to change their settings
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lineStyle = "#084258"
        frameMain = tk.Frame(self, bg=DS.mainBG)
        frameHeaderBar = tk.Frame(frameMain, bg=DS.mainBG)
        headerFont = tkfont.Font(family='Arial', size=16, weight="bold")
        self.labelStore = tk.Label(frameHeaderBar, text="Store", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelStore.bind("<Button-1>", lambda event: controller.show_frame("Haze_Store"))
        self.labelStore.bind("<Enter>", lambda event: self.on_enter(self.labelStore))
        self.labelStore.bind("<Leave>", lambda event: self.on_leave(self.labelStore))
        self.labelStore.grid(column=0, row=0, padx=26, pady=8)
        self.labelLibrary = tk.Label(frameHeaderBar, text="Library", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLibrary.bind("<Button-1>", lambda event: controller.show_frame("Haze_Library"))
        self.labelLibrary.bind("<Enter>", lambda event: self.on_enter(self.labelLibrary))
        self.labelLibrary.bind("<Leave>", lambda event: self.on_leave(self.labelLibrary))
        self.labelLibrary.grid(column=1, row=0, padx=26, pady=8)
        self.labelHome = tk.Label(frameHeaderBar, text="Home", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelHome.bind("<Button-1>", lambda event: controller.show_frame("Haze_Main"))
        self.labelHome.bind("<Enter>", lambda event: self.on_enter(self.labelHome))
        self.labelHome.bind("<Leave>", lambda event: self.on_leave(self.labelHome))
        self.labelHome.grid(column=2, row=0, padx=38, pady=8)
        self.labelLogout = tk.Label(frameHeaderBar, text="Logout", font=headerFont, fg=DS.mainFG, bg=DS.mainBG)
        self.labelLogout.bind("<Button-1>", lambda event: self.Logout())
        self.labelLogout.bind("<Enter>", lambda event: self.on_enter(self.labelLogout))
        self.labelLogout.bind("<Leave>", lambda event: self.on_leave(self.labelLogout))
        self.labelLogout.grid(column=3, row=0, padx=(95,26), pady=8)
        headerLine = tk.Canvas(frameHeaderBar, height=2, width=570, bd=0, highlightthickness=0, bg=lineStyle)
        headerLine.grid(row=1, padx=10, column=0, columnspan=4)
        frameHeaderBar.grid(row=0)
        #Main content
        titleFont = tkfont.Font(family='Arial', size=14, weight="bold")
        contentFont = tkfont.Font(family='Arial', size=12)
        frameMainFrame = tk.Frame(frameMain, bg=DS.mainBG)
        labelExplain = tk.Label(frameMainFrame, font=tkfont.Font(size=20, weight="bold"), bg=DS.mainBG, fg=DS.mainFG
            ,text="This tab currently serves no purpose as\nthe program has been optimised for\nyour best experience, it would in theory\nallow the user to change\ntheir login info and currency")
        labelExplain.grid(row=1, column=0, padx=10, pady=60, sticky="n")
        frameMainFrame.grid()
        frameMain.grid()  

    def on_enter(self, who):
        who.config(fg=DS.mainHover)

    def on_leave(self, who):
        who.config(fg=DS.mainFG)

    def Logout(self):
        self.windowLogout = tk.Toplevel(bg=DS.mainBG)
        self.windowLogout.resizable(False, False)
        self.windowLogout.wm_title("Logout")
        frameButtons = tk.Frame(self.windowLogout, bg=DS.mainBG)
        labelLogoutMessage = tk.Label(self.windowLogout, fg=DS.mainFG, bg=DS.mainBG, text="Are you sure you want to log out?",
            font=tkfont.Font(family='Arial', size=10, weight="bold", slant="roman")).pack(pady=(18,8), padx=15)
        buttonYes = tk.Button(frameButtons, text="Yes", fg=DS.mainFG, bg=DS.mainBG, command=lambda: self.LogoutYes()).pack(padx=12, ipadx=8, pady=20, side="left")
        buttonNo = tk.Button(frameButtons, text="No", fg=DS.mainFG, bg=DS.mainBG, command=self.windowLogout.destroy).pack(padx=12, ipadx=8, pady=20, side="left")
        frameButtons.pack()

    def LogoutYes(self):
        global app, path
        self.windowLogout.destroy()
        config = open(str(path)+"/config/config.txt", "w")
        config.write('{\n\t"logged": "False",\n\t"currentUser": ""\n\t"currency": "NZD"\n}')
        config.close()
        app.destroy()
        app = HazeStartup()
        app.resizable(False, False)
        app.mainloop()

#Creates a game window
class LaunchGame:
    def __init__(self, game):
        self.gameMessage = tk.StringVar()
        self.gameWindow = tk.Toplevel(bg=DS.mainBG)
        self.gameWindow.resizable(False, False)
        self.gameWindow.wm_title("game")
        self.gameWindow.bind("<Return>", self.destroyWindow)
        self.gameWindow.focus_force()
        gameFrame = tk.Frame(self.gameWindow, bg=DS.mainBG)
        self.gameLabel = tk.Label(gameFrame, textvariable = self.gameMessage, bg=DS.mainBG, fg=DS.mainFG, font=tkfont.Font(family='Arial', size=10, weight="bold"))
        self.gameLabel.grid(row = 0, column = 0)
        gameAcceptButton = tk.Button(gameFrame, text="Exit", command=self.destroyWindow, bg=DS.mainBG, fg=DS.mainFG)
        gameAcceptButton.grid(row=1, column=0, padx=10, pady=10, ipadx=8, ipady=5)
        self.gameMessage.set("Launched " + game)
        gameFrame.pack(side="top", fill="both", expand=True, padx=70, pady=10)
        CurrentUser.currentlyPlaying = True
        buttonState()

    #Destroy game window
    def destroyWindow(self, *args):
        CurrentUser.currentlyPlaying = False
        buttonState()
        self.gameWindow.destroy()  
        
#Create error window
class raiseError:
    def __init__(self, errorMessage):
        global errorActive, errorWindowObject
        if errorActive:
            try:
                if errorWindowObject.errorWindow.state() == "normal":
                    errorWindowObject.errorMessage.set(errorMessage)
                    errorWindowObject.errorWindow.focus_force()
                else:
                    errorActive = False
            except:
                errorActive = False
        elif not errorActive:
            errorActive = True
            self.errorMessage = tk.StringVar()
            self.errorWindow = tk.Toplevel()
            self.errorWindow.resizable(False, False)
            self.errorWindow.wm_title("Error")
            self.errorWindow.bind("<Return>", self.destroyWindow)
            self.errorWindow.focus_force()
            errorFrame = tk.Frame(self.errorWindow)
            self.errorLabel = tk.Label(errorFrame, textvariable = self.errorMessage)
            self.errorLabel.grid(row = 0, column = 0)
            errorAcceptButton = tk.Button(errorFrame, text="OK", command=self.destroyWindow)
            errorAcceptButton.grid(row=1, column=0)
            self.errorMessage.set("Error: " + errorMessage)
            errorFrame.pack(side="top", fill="both", expand=True, padx=70, pady=10)
            errorWindowObject = self

    def destroyWindow(self, *args):
        global errorActive
        errorActive = False
        self.errorWindow.destroy()    

#Turns buttons on and off if user is playing a game
def buttonState():
    global buttonList
    if not CurrentUser.currentlyPlaying:
        for button in buttonList:
            button["state"] = "normal"
    else:
        for button in buttonList:
            button["state"] = "disabled"

#Open dictionary from txt file
def DictionaryReader(File):
    if ".txt" not in File:
        File = str(File) + ".txt"
    with open(File, "r") as text:
        loaded = json.loads(str(text.read().replace("\n", "")))
        text.close()
    return loaded

#Converts currency
def Converter(Price, Currency):
    if len(Currency) != 3:
        Currency = Location.currency
    else:
        pass
    Currencies = {
    "USD": 0.68,
    "NZD": 1,
    "AUD": 0.94,
    "GBP": 0.53,
    "CAD": 0.90
    }
    return Price*Currencies[Currency]

#Checks if user is logged in on startup
def Startup():
    global path, app, currentUser
    config = DictionaryReader(str(path)+"/config/config")
    if config["logged"] == "True":
        targetUser = config["currentUser"]
        tUI = DictionaryReader((str(path)+"/users/"+str(targetUser)+"/config"))
        currentUser = CurrentUser(tUI["username"], tUI["password"], tUI["email"], tUI["DOB"], tUI["currency"])
        return HazeMain()
    else:
        return HazeStartup()
        
currentUser = ""
buttonList = []
countryList = DictionaryReader("config/countryList")
path = os.path.dirname(os.path.realpath(__file__))
userList = []
for users in os.listdir(str(path) + "/users/"):
    userList += str(users)
emailList = []
errorActive = False
errorWindow = ""
DS = DS()
app = Startup()
app.resizable(False, False)
app.mainloop()

from tkinter import *
import json
import re
import pyperclip


def popupMessage(title, message, windowToClose=None):
    popupWindow = Toplevel()
    popupWindow.title(title)
    if not windowToClose:
        close = popupWindow.destroy
    elif windowToClose == 'all':
        close = popupWindow.quit
    else:
        def close():
            popupWindow.destroy()
            windowToClose.destroy()
    msg = Label(popupWindow, text=message, padx=10, pady=10)
    ok = Button(popupWindow, text="Ok", padx=10,
                pady=10, command=close)
    msg.pack()
    ok.pack()


def convertText(text, switches):
    reportMessage = ''
    char_found = False
    word_found = False
    for k in switches:
        if len(k) == 1:
            if k in text:
                char_found = True
        else:
            if re.search(r'(?<!\w)' + k + r'(?!\w)', text):
                word_found = True

    if char_found or word_found:
        for k in switches:
            if len(k) == 1:
                if k in text:
                    kcount = text.count(k)
                    text = text.replace(k, switches[k])
                    reportMessage += f"{k} -> {switches[k]}. {kcount} occurrence(s).\n"
            else:
                if re.search(r'(?<!\w)' + k + r'(?!\w)', text):
                    text, kcount = re.subn(
                        r'(?<!\w)' + k + r'(?!\w)', switches[k], text)
                    reportMessage += f"{k} -> {switches[k]}. {kcount} occurrence(s).\n"
        pyperclip.copy(text)
        popupMessage('Changes made.', reportMessage +
                     "Edit text copied to clipboard.")

    else:
        popupMessage(
            'No changes made.', 'There were no special characters or other switches to make in your text.')


class Whitelist:
    def __init__(self):
        with open("savefile.json", "r", encoding="utf-8") as f:
            self.savedData = json.load(f)
        try:
            self.regex = self.savedData['regex']
        except KeyError:
            self.regex = ''
        self.displayWhitelist()

    def displayWhitelist(self):
        self.whitelist = Toplevel()
        self.whitelist.title("Whitelist")

        self.displayRegex = StringVar()
        self.displayRegex.set(self.regex)
        l = Label(self.whitelist, textvariable=self.displayRegex,
                  padx=10, pady=10)
        self.e = Entry(self.whitelist, width=40)
        self.e.insert(0, self.regex)
        b = Button(self.whitelist, text="Submit", padx=10,
                   pady=10, command=self.updateWhitelist)
        self.displayMessage = StringVar()
        dm = Label(self.whitelist, textvariable=self.displayMessage,
                   padx=10, pady=10)
        l.pack()
        self.e.pack()
        b.pack()
        dm.pack()

    def updateWhitelist(self):
        contents = self.e.get()
        if contents == self.regex:
            self.displayMessage.set("No changes made.")
        else:
            self.regex = contents
            self.savedData['regex'] = self.regex
            with open("savefile.json", "w") as f:
                json.dump(self.savedData, f, indent=4)
            self.displayMessage.set("Regex updated.")
            self.displayRegex.set(self.regex)
            input_window.reloadFile()


class Switchlist:
    def __init__(self):
        with open("savefile.json", "r", encoding="utf-8") as f:
            self.savedData = json.load(f)
        try:
            self.switches = self.savedData['switches']
        except KeyError:
            self.switches = {}
        self.displaySwitchlist()

    def displaySwitchlist(self):
        self.switchlist = Toplevel()
        self.switchlist.title("Switchlist")

        self.lb = Listbox(self.switchlist, height=20, width=40)
        for k, v in self.switches.items():
            self.lb.insert(END, f"{k} ----> {v}")
        self.lb.grid(row=0, column=0, columnspan=3)
        sb = Scrollbar(self.switchlist)
        sb.grid(row=0, column=4, sticky=N + S)
        self.lb.config(yscrollcommand=sb.set)
        sb.config(command=self.lb.yview)

        add = Button(self.switchlist, text="Add",
                     padx=10, pady=10, command=self.add)
        delete = Button(self.switchlist, text="Delete",
                        padx=10, pady=10, command=self.delete)
        edit = Button(self.switchlist, text="Edit",
                      padx=10, pady=10, command=self.edit)
        add.grid(row=1, column=0)
        delete.grid(row=1, column=1)
        edit.grid(row=1, column=2)

    def add(self):
        def addEntry():
            bf = e1.get()
            aft = e2.get()
            if bf == "" or aft == "":
                popupMessage("Error", "Inputs cannot be blank.",
                             windowToClose=addWindow)
                return
            self.savedData['switches'][bf] = aft
            self.lb.insert(END, f"{bf} -----> {aft}")
            with open('savefile.json', 'w') as f:
                json.dump(self.savedData, f, indent=4)

            popupMessage(
                "Successful", "Successfully added new entry.", windowToClose=addWindow)
            input_window.reloadFile()

        addWindow = Toplevel()
        addWindow.title("Add entry")
        before = Label(addWindow, text="Before")
        after = Label(addWindow, text="After")
        e1 = Entry(addWindow, width=10)
        e2 = Entry(addWindow, width=10)
        l = Label(addWindow, text="----->")
        b = Button(addWindow, text='Confirm',
                   padx=10, pady=10, command=addEntry)
        before.grid(row=0, column=0)
        after.grid(row=0, column=2)
        e1.grid(row=1, column=0)
        l.grid(row=1, column=1)
        e2.grid(row=1, column=2)
        b.grid(row=2, column=1)

    def delete(self):
        selectedindex = self.lb.curselection()
        if not selectedindex:
            popupMessage("Nothing selected",
                         "Please select an entry to delete.")
        else:
            selectedindex = selectedindex[0]

            name = self.lb.get(selectedindex).split()[0]
            del self.savedData['switches'][name]
            with open('savefile.json', 'w') as f:
                json.dump(self.savedData, f, indent=4)
            self.lb.delete(selectedindex)
            input_window.reloadFile()

    def edit(self):
        selectedindex = self.lb.curselection()
        if not selectedindex:
            popupMessage("Nothing selected", "Please select an entry to edit.")
        else:
            def editEntry():
                bf = e1.get()
                aft = e2.get()
                if bf == "" or aft == "":
                    popupMessage("Error", "Inputs cannot be blank.",
                                 windowToClose=editWindow)
                    return
                del self.savedData['switches'][key]
                self.savedData['switches'][bf] = aft
                with open('savefile.json', 'w') as f:
                    json.dump(self.savedData, f, indent=4)
                self.lb.delete(selectedindex)
                self.lb.insert(selectedindex, f"{bf} -----> {aft}")

                popupMessage(
                    "Successful", "Successfully edited entry.", windowToClose=editWindow)
                input_window.reloadFile()

            selectedindex = selectedindex[0]
            bf = self.lb.get(selectedindex).split()[0]
            aft = self.lb.get(selectedindex).split()[2]
            key = bf

            editWindow = Toplevel()
            editWindow.title("Edit entry")
            before = Label(editWindow, text="Before")
            after = Label(editWindow, text="After")
            e1 = Entry(editWindow, width=10)
            e2 = Entry(editWindow, width=10)

            e1.insert(0, bf)
            e2.insert(0, aft)

            l = Label(editWindow, text="----->")
            b = Button(editWindow, text='Confirm',
                       padx=10, pady=10, command=editEntry)
            before.grid(row=0, column=0)
            after.grid(row=0, column=2)
            e1.grid(row=1, column=0)
            l.grid(row=1, column=1)
            e2.grid(row=1, column=2)
            b.grid(row=2, column=1)


class InputText:
    def __init__(self):
        with open("savefile.json", "r", encoding="utf-8") as f:
            self.savedData = json.load(f)
        try:
            self.regex = self.savedData['regex']
        except KeyError:
            popupMessage(
                "Regex not found.",
                "Please go to Settings - Whitelist to set a regex pattern. Click 'Ok' after you've done that.", windowToClose='all')
        try:
            self.switches = self.savedData['switches']
        except KeyError:
            self.switches = {}

    def reloadFile(self):
        with open("savefile.json", 'r', encoding="utf-8") as f:
            self.savedData = json.load(f)
        self.regex = self.savedData['regex']
        self.switches = self.savedData['switches']
        print("testing")

    def displayTextbox(self):
        label = Label(root, text="Input your text here:", padx=10, pady=10)
        label.pack()
        self.tb = Text(root, height=40, width=140)
        self.tb.pack()
        submitButton = Button(root, text="Submit", padx=10,
                              pady=10, command=self.submit)
        submitButton.pack()

    def submit(self):
        text = self.tb.get("1.0", END)
        pattern = re.compile(self.regex)
        self.unregistered = []
        for char in text:
            if not pattern.findall(char):
                if char not in self.switches:
                    if char not in self.unregistered:
                        self.unregistered += char
        if self.unregistered:
            RegisterCharacters(self.unregistered, text)
        else:
            convertText(text, self.switches)


class RegisterCharacters:
    def __init__(self, unregistered, text):
        self.text = text
        self.unregistered = unregistered
        with open("savefile.json", "r", encoding="utf-8") as f:
            self.savedData = json.load(f)
        try:
            self.regex = self.savedData['regex']
        except KeyError:
            popupMessage(
                "Regex not found.",
                "Please go to Settings - Whitelist to set a regex pattern. Click 'Ok' after you've done that.", windowToClose='all')
        try:
            self.switches = self.savedData['switches']
        except KeyError:
            self.switches = {}
        self.displayWindow()

    def displayWindow(self):
        self.reg = Toplevel()
        self.reg.title("Unregistered character(s) found.")
        self.makeRows(self.unregistered)
        saveButton = Button(self.reg, text="Save Changes",
                            padx=10, pady=10, command=self.save)
        saveButton.grid(row=len(self.unregistered) + 1, column=1)
        switchButton = Button(
            self.reg, text="Start Switching", padx=10, pady=10, command=lambda: convertText(self.text, self.switches))
        switchButton.grid(row=len(self.unregistered) + 1, column=2)

    def makeRows(self, unregistered):
        self.rowDict = {}
        for i, char in enumerate(unregistered):
            self.rowDict[char] = {}
            self.rowDict[char]['name'] = char
            self.rowDict[char]['label'] = Label(
                self.reg, text=char, padx=10, pady=10)
            self.rowDict[char]['checkbutton'] = Checkbutton(
                self.reg, text='Whitelist', padx=10, pady=10)
            self.rowDict[char]['checkbutton'].bind(
                '<Button-1>', self.toggleEntry)
            self.rowDict[char]['entry'] = Entry(self.reg, width=10)
            self.rowDict[char]['label'].grid(row=i, column=0)
            self.rowDict[char]['checkbutton'].grid(row=i, column=1)
            self.rowDict[char]['entry'].grid(row=i, column=2)

    def toggleEntry(self, event):
        cb = event.widget
        for char in self.rowDict:
            if self.rowDict[char]['checkbutton'] == cb:
                e = self.rowDict[char]['entry']
                break
        if e['state'] == NORMAL:
            e.config(state=DISABLED)
        elif e['state'] == DISABLED:
            e.config(state=NORMAL)

    def save(self):
        whitelistedChars = []
        for char in self.rowDict:
            if self.rowDict[char]['entry']['state'] == DISABLED:
                whitelistedChars += char
            elif self.rowDict[char]['entry']['state'] == NORMAL:
                self.switches[char] = self.rowDict[char]['entry'].get()
        self.regex = self.regex[:-1] + ''.join(whitelistedChars) + ']'
        self.savedData['regex'] = self.regex
        self.savedData['switches'] = self.switches

        with open('savefile.json', 'w') as f:
            json.dump(self.savedData, f, indent=4)

        popupMessage('Changes saved.', 'Your switches have been registered.')

    def convert(self):
        reportMessage = ''
        if any(k in self.text for k in self.switches):
            for k in self.switches:
                kcount = self.text.count(k)
                self.text = self.text.replace(k, self.switches[k])
                reportMessage += f"{k} -> {self.switches[k]}. {kcount} occurrences.\n"
            pyperclip.copy(self.text)
            popupMessage('Changes made.', reportMessage +
                         "Edit text copied to clipboard.",
                         windowToClose=self.reg)

        else:
            popupMessage(
                'No changes made.',
                'There were no special characters or other switches to make in your text.')


root = Tk()

root.title("Text Switcher")
mainMenu = Menu(root)
root.config(menu=mainMenu)
settingsMenu = Menu(mainMenu)
mainMenu.add_cascade(label='Settings', menu=settingsMenu)
settingsMenu.add_command(label="White List", command=lambda: Whitelist())
settingsMenu.add_command(label="Switch List", command=lambda: Switchlist())
input_window = InputText()
input_window.displayTextbox()


root.mainloop()

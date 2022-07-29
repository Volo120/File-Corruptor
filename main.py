from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
import sys, random

class App(Tk):
    VER = "1.1"
    def __init__(self):
        super().__init__()
        self.title(f"Corruptor {App.VER}")
        self.geometry("500x400")

        self.file = ""
        self.new_file = ""
        self.is_random = BooleanVar()
        self.is_replaced = BooleanVar()

        # ------------- menu ---------------
        
        self.menu = Menu(self)
        self.file_menu = Menu(self.menu, tearoff=False)

        self.file_menu.add_command(label="attach file", command=self.attach_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: sys.exit())

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menu)

        # -----------------------------------

        self.file_label = Label(self, text="No file attached")
        self.file_label.pack(pady=5)

        self.mainFrame = Frame(self)
        self.mainFrame.pack(pady=5)

        self.startByteLabel = Label(self.mainFrame, text="Start byte")
        self.startByteLabel.grid(row=0, column=0)

        self.startByteEntry = Entry(self.mainFrame)
        self.startByteEntry.insert(0, str(0))
        self.startByteEntry.grid(row=0, column=1, padx=5)

        self.endByteLabel = Label(self.mainFrame, text="End byte")
        self.endByteLabel.grid(row=1, column=0)

        self.endByteEntry = Entry(self.mainFrame)
        self.endByteEntry.insert(0, str(0))
        self.endByteEntry.grid(row=1, column=1, padx=5)

        self.autoFillButton = Button(self.mainFrame, text="Auto fill", command=self.auto_end_func)
        self.autoFillButton.grid(row=1, column=2, padx=5)

        self.autoEndByteLabel = Label(self.mainFrame, text="Start byte")
        self.autoEndByteLabel.grid(row=0, column=0)

        self.byteBlockSizeLabel = Label(self.mainFrame, text="Byte block size")
        self.byteBlockSizeLabel.grid(row=2, column=0)

        self.byteBlockSizeEntry = Entry(self.mainFrame)
        self.byteBlockSizeEntry.insert(0, str(0))
        self.byteBlockSizeEntry.grid(row=2, column=1, padx=5)

        self.byteBlockSpaceLabel = Label(self.mainFrame, text="Byte block space")
        self.byteBlockSpaceLabel.grid(row=3, column=0)

        self.byteBlockSpaceEntry = Entry(self.mainFrame)
        self.byteBlockSpaceEntry.insert(0, str(0))
        self.byteBlockSpaceEntry.grid(row=3, column=1, padx=5, pady=5)

        self.addByteLabel = Label(self.mainFrame, text="Add byte")
        self.addByteLabel.grid(row=4, column=0)

        self.addByteEntry = Entry(self.mainFrame)
        self.addByteEntry.insert(0, str(0))
        self.addByteEntry.grid(row=4, column=1, padx=5)

        # -------------- Hidden -----------------

        self.minMaxFrame = Frame(self)

        self.minMaxFrame.pack()
        self.minMaxFrame.pack_forget()

        self.minByteLabel = Label(self.minMaxFrame, text="Min byte")
        self.minByteLabel.grid_forget()

        self.minByteEntry = Entry(self.minMaxFrame, width=7)
        self.minByteEntry.insert(0, str(0))
        self.minByteEntry.grid_forget()

        self.maxByteLabel = Label(self.minMaxFrame, text="Max byte")
        self.maxByteLabel.grid_forget()

        self.maxByteEntry = Entry(self.minMaxFrame, width=7)
        self.maxByteEntry.insert(0, str(255))
        self.maxByteEntry.grid_forget()

        # ----------------------------------------

        self.randomCheckButton = Checkbutton(self, text="Randomize bytes", variable=self.is_random, onvalue=True, offvalue=False, command=self.random_on_off)
        self.randomCheckButton.pack()

        self.replaceCheckButton = Checkbutton(self, text="Replace bytes", variable=self.is_replaced, onvalue=True, offvalue=False)
        self.replaceCheckButton.pack()

        self.corruptButton = Button(self, text="Corrupt!", font=("Helvitica", 23, "normal"), command=self.corrupt_file)
        self.corruptButton.pack(side="bottom", pady=20)

    def random_on_off(self):
        if self.is_random.get():
            self.addByteLabel.grid_forget()
            self.addByteEntry.grid_forget()

            self.minMaxFrame.pack()

            self.minByteLabel.grid(row=0, column=0)
            self.minByteEntry.grid(row=0, column=1, padx=3)

            self.maxByteLabel.grid(row=1, column=0)
            self.maxByteEntry.grid(row=1, column=1, padx=3)

        else:
            self.minMaxFrame.pack_forget()
            self.addByteLabel.grid(row=4, column=0)
            self.addByteEntry.grid(row=4, column=1, padx=5)

    def auto_end_func(self):
        if self.new_file != "" and self.file != "":
            self.endByteEntry.delete(0, END)
            self.endByteEntry.insert(0, Path(self.file).stat().st_size)

    def corrupt_file(self):
        try:
            baseFile = open(self.file, "rb+")
            corruptedFile = open(self.new_file, "wb+")
        except FileNotFoundError:
            self.attach_file()
            return

        def copy_file_contents(mainFile, corruptedFile, endByte):
            for z in range(0, endByte):
                currentByte = mainFile.read(1)
                corruptedFile.write(currentByte)

        def add_corrupt(baseFile, corruptedFile, blockSpace):
            for y in range(0, int(self.byteBlockSizeEntry.get())):
                currentByte = baseFile.read(1)
                if currentByte == b"":
                    break
                currentByte = int.from_bytes(currentByte, byteorder="big")

                if int(self.minByteEntry.get()) > 255: # if min or max value > 255
                    self.minByteEntry.delete(0, END)
                    self.minByteEntry.insert(0, str(255))

                if int(self.maxByteEntry.get()) > 255:
                    self.maxByteEntry.delete(0, END)
                    self.maxByteEntry.insert(0, str(255))

                if self.is_random:
                    if self.is_replaced: # Replace and randomize bytes
                        currentByte = 0
                        currentByte += random.randint(int(self.minByteEntry.get()), int(self.maxByteEntry.get()))
                    else: # Randomize without replacing bytes
                        currentByte += random.randint(int(self.minByteEntry.get()), int(self.maxByteEntry.get()))
                else: # Increase bytes
                    if self.is_replaced: # if replace enabled
                        currentByte = int(self.addByteEntry.get())
                    else:
                        currentByte += int(self.addByteEntry.get())
                if currentByte > 255 or currentByte < 0: # if byte bigger than 255 or less than 0
                    currentByte = currentByte % 255
                currentByte = currentByte.to_bytes(1, byteorder="big")
                corruptedFile.write(currentByte)

            copy_file_contents(baseFile, corruptedFile, blockSpace)

        baseFile.seek(0)
        copy_file_contents(baseFile, corruptedFile, int(self.startByteEntry.get()))

        corruptStepSize = int(self.byteBlockSizeEntry.get()) + int(self.byteBlockSpaceEntry.get())
        for x in range(int(self.startByteEntry.get()), int(self.endByteEntry.get()), corruptStepSize):
            add_corrupt(baseFile, corruptedFile, int(self.byteBlockSpaceEntry.get()))

        while True:
            currentByte = baseFile.read(1)
            if currentByte == b"": break
            corruptedFile.write(currentByte)

        baseFile.close()
        corruptedFile.close()

    def attach_file(self):
        win = Toplevel(self)
        win.geometry("600x140")

        def open_file():
            file = filedialog.askopenfile()
            if not file: return
            input_file_entry.delete("1.0", END)
            input_file_entry.insert("1.0", file.name)

        def save_file():
            file = filedialog.asksaveasfile()
            if not file: return
            output_file_entry.delete("1.0", END)
            output_file_entry.insert("1.0", file.name)

        def ok_func():
            if Path(input_file_entry.get("1.0", END).strip()).is_dir() or Path(output_file_entry.get("1.0", END).strip()).is_dir():
                messagebox.showerror(title="Error", message="Please provide a valid file")
                return

            if len(input_file_entry.get("1.0", END).strip()) > 0 and len(output_file_entry.get("1.0", END).strip()) > 0:
                self.file = input_file_entry.get("1.0", END).strip()
                self.new_file = output_file_entry.get("1.0", END).strip()
                self.file_label['text'] = self.file
            win.destroy()

        frame = Frame(win)
        frame.pack(pady=5)

        input_file_label = Label(frame, text="input file")
        input_file_label.grid(row=0, column=0, padx=3)

        input_file_entry = Text(frame, width=30, height=1)
        input_file_entry.grid(row=0, column=1, padx=3)

        input_file_button = Button(frame, text="open...", command=open_file)
        input_file_button.grid(row=0, column=2, padx=3)

        output_file_label = Label(frame, text="output file")
        output_file_label.grid(row=1, column=0, padx=3)

        output_file_entry = Text(frame, width=30, height=1)
        output_file_entry.grid(row=1, column=1, padx=3)

        output_file_button = Button(frame, text="open...", command=save_file)
        output_file_button.grid(row=1, column=2, padx=3, pady=5)

        ok_button = Button(win, text="ok", width=10, command=ok_func)
        ok_button.pack()

        input_file_entry.insert("1.0", self.file)
        output_file_entry.insert("1.0", self.new_file)

        win.mainloop()

if __name__ == "__main__":
    App().mainloop()
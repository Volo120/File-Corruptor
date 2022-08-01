from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
import sys, random

class App(Tk):
    VER = "v1.3.2"
    def __init__(self):
        super().__init__()
        self.title(f"Corruptor {App.VER}")
        self.geometry("500x400")

        self.file = ""
        self.new_file = ""
        self.is_random = BooleanVar()
        self.is_replaced = BooleanVar()
        self.engine = IntVar()
        self.is_hex = BooleanVar()
        self.is_exclusive = BooleanVar()
        
        # ------------- menu ---------------
        
        self.menu = Menu(self, tearoff=False)
        self.file_menu = Menu(self.menu, tearoff=False)
        self.engine_menu = Menu(self.menu, tearoff=False)
        self.options_menu = Menu(self.menu, tearoff=False)

        self.file_menu.add_command(label="attach file", command=self.attach_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: sys.exit(), activebackground="#AF0000")

        self.engine_menu.add_radiobutton(label="Incrementer", variable=self.engine, value=0, command=self.change_engine)
        self.engine_menu.add_radiobutton(label="Randomizer", variable=self.engine, value=1, command=self.change_engine)
        self.engine_menu.add_radiobutton(label="Replacer", variable=self.engine, value=2, command=self.change_engine)

        self.options_menu.add_checkbutton(label="Hexadecimal", variable=self.is_hex, onvalue=True, offvalue=False, command=self.hex_on_off)

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Engine", menu=self.engine_menu)
        self.menu.add_cascade(label="Options", menu=self.options_menu)

        self.configure(menu=self.menu)

        # -----------------------------------

        self.engine.set(0) # sets engine to default (Incrementer)

        self.file_label = Label(self, text="No file attached", cursor="hand2")
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

        self.autoFillButton = Button(self.mainFrame, text="Auto fill", command=self.auto_fill_func)
        self.autoFillButton.grid(row=1, column=2, padx=5)

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

        self.minByteLabel = Label(self.minMaxFrame, text="Min byte")
        self.minByteEntry = Entry(self.minMaxFrame, width=7)
        self.minByteEntry.insert(0, str(0))

        self.maxByteLabel = Label(self.minMaxFrame, text="Max byte")
        self.maxByteEntry = Entry(self.minMaxFrame, width=7)
        self.maxByteEntry.insert(0, str(255))

        # ***

        self.replaceFrame = Frame(self)

        self.targetByteLabel = Label(self.replaceFrame, text="Target byte")
        self.targetByteEntry = Entry(self.replaceFrame, width=7)
        self.targetByteEntry.insert(0, str(0))

        self.replaceWithLabel = Label(self.replaceFrame, text="Replace with")
        self.replaceWithEntry = Entry(self.replaceFrame, width=7)
        self.replaceWithEntry.insert(0, str(0))

        self.exclusiveCheckbutton = Checkbutton(self, text="Exclusive", variable=self.is_exclusive, command=self.exclusive_func)
        self.replaceCheckbutton = Checkbutton(self, text="Replace", variable=self.is_replaced)

        # ----------------------------------------

        self.corruptButton = Button(self, text="Corrupt!", font=("Helvitica", 23, "normal"), command=self.corrupt_file)
        self.corruptButton.pack(side="bottom", pady=20)

        self.change_engine()

        self.file_label.bind("<Button-1>", self.attach_file)

    def exclusive_func(self):
        if self.is_exclusive.get():
            self.targetByteLabel.configure(state=NORMAL)
            self.targetByteEntry.configure(state=NORMAL)
            self.replaceWithLabel.configure(text="Replace with")
        else:
            self.targetByteLabel.configure(state=DISABLED)
            self.targetByteEntry.configure(state=DISABLED)
            self.replaceWithLabel.configure(text="Replace all with")

    def hex_on_off(self):
        if self.is_hex.get(): # Hex on
            startByte = int(self.startByteEntry.get())
            self.startByteEntry.delete(0, END)
            self.startByteEntry.insert(0, hex(startByte))

            endByte = int(self.endByteEntry.get())
            self.endByteEntry.delete(0, END)
            self.endByteEntry.insert(0, hex(endByte))

            blockSizeByte = int(self.byteBlockSizeEntry.get())
            self.byteBlockSizeEntry.delete(0, END)
            self.byteBlockSizeEntry.insert(0, hex(blockSizeByte))

            blockSpaceByte = int(self.byteBlockSpaceEntry.get())
            self.byteBlockSpaceEntry.delete(0, END)
            self.byteBlockSpaceEntry.insert(0, hex(blockSpaceByte))

            addByte = int(self.addByteEntry.get())
            self.addByteEntry.delete(0, END)
            self.addByteEntry.insert(0, hex(addByte))

            minByte = int(self.minByteEntry.get())
            self.minByteEntry.delete(0, END)
            self.minByteEntry.insert(0, hex(minByte))

            maxByte = int(self.maxByteEntry.get())
            self.maxByteEntry.delete(0, END)
            self.maxByteEntry.insert(0, hex(maxByte))

            targetByte = int(self.targetByteEntry.get())
            self.targetByteEntry.delete(0, END)
            self.targetByteEntry.insert(0, hex(targetByte))

            replaceByte = int(self.replaceWithEntry.get())
            self.replaceWithEntry.delete(0, END)
            self.replaceWithEntry.insert(0, hex(replaceByte))
        else: # Hex off
            startByte = self.startByteEntry.get()
            self.startByteEntry.delete(0, END)
            self.startByteEntry.insert(0, int(startByte, 16))

            endByte = self.endByteEntry.get()
            self.endByteEntry.delete(0, END)
            self.endByteEntry.insert(0, int(endByte, 16))

            blockSizeByte = self.byteBlockSizeEntry.get()
            self.byteBlockSizeEntry.delete(0, END)
            self.byteBlockSizeEntry.insert(0, int(blockSizeByte, 16))

            blockSpaceByte = self.byteBlockSpaceEntry.get()
            self.byteBlockSpaceEntry.delete(0, END)
            self.byteBlockSpaceEntry.insert(0, int(blockSpaceByte, 16))

            addByte = self.addByteEntry.get()
            self.addByteEntry.delete(0, END)
            self.addByteEntry.insert(0, int(addByte, 16))

            minByte = self.minByteEntry.get()
            self.minByteEntry.delete(0, END)
            self.minByteEntry.insert(0, int(minByte, 16))

            maxByte = self.maxByteEntry.get()
            self.maxByteEntry.delete(0, END)
            self.maxByteEntry.insert(0, int(maxByte, 16))

            targetByte = self.targetByteEntry.get()
            self.targetByteEntry.delete(0, END)
            self.targetByteEntry.insert(0, int(targetByte, 16))

            replaceByte = self.replaceWithEntry.get()
            self.replaceWithEntry.delete(0, END)
            self.replaceWithEntry.insert(0, int(replaceByte, 16))

    def change_engine(self):
        current_engine = self.engine.get()
        if current_engine == 0: # Incrementer engine
            self.geometry("500x300")
            self.replaceFrame.pack_forget()
            self.targetByteLabel.grid_forget()
            self.targetByteEntry.grid_forget()

            self.minMaxFrame.pack_forget()
            self.addByteLabel.grid(row=4, column=0)
            self.addByteEntry.grid(row=4, column=1, padx=5)
            self.replaceCheckbutton.pack_forget()
            self.exclusiveCheckbutton.pack_forget()

            self.is_random.set(False)
            self.is_replaced.set(False)
            self.is_exclusive.set(False)

        if current_engine == 1: # Randomizer engine
            self.geometry("500x370")
            self.addByteLabel.grid_forget()
            self.addByteEntry.grid_forget()

            self.replaceFrame.pack_forget()
            self.targetByteLabel.grid_forget()
            self.targetByteEntry.grid_forget()

            self.minMaxFrame.pack()
            self.minByteLabel.grid(row=0, column=0)
            self.minByteEntry.grid(row=0, column=1, padx=3)

            self.maxByteLabel.grid(row=1, column=0)
            self.maxByteEntry.grid(row=1, column=1, padx=3)
            self.replaceCheckbutton.pack(pady=4)
            self.exclusiveCheckbutton.pack_forget()

            self.is_random.set(True)
            self.is_replaced.set(False)
            self.is_exclusive.set(False)

        if current_engine == 2: # Replacer engine
            self.geometry("500x370")
            self.addByteLabel.grid_forget()
            self.addByteEntry.grid_forget()

            self.minMaxFrame.pack_forget()
            self.minByteLabel.grid_forget()
            self.minByteEntry.grid_forget()
            self.maxByteLabel.grid_forget()
            self.maxByteEntry.grid_forget()

            self.replaceFrame.pack()
            self.targetByteLabel.grid(row=0, column=0)
            self.targetByteEntry.grid(row=0, column=1, padx=3)
            self.replaceWithLabel.grid(row=1, column=0)
            self.replaceWithEntry.grid(row=1, column=1, padx=3)
            self.replaceCheckbutton.pack_forget()
            self.exclusiveCheckbutton.pack(pady=4)
            
            self.is_random.set(False)
            self.is_replaced.set(True)
            self.is_exclusive.set(True)
            
            self.exclusive_func()

    def auto_fill_func(self):
        if self.new_file != "" and self.file != "":
            if not self.is_hex.get(): # Hex mode off
                self.endByteEntry.delete(0, END)
                self.endByteEntry.insert(0, Path(self.file).stat().st_size)
            else: # Hex mode on
                self.endByteEntry.delete(0, END)
                self.endByteEntry.insert(0, hex(Path(self.file).stat().st_size))
        else:
            self.attach_file()

    def corrupt_file(self):
        try:
            baseFile = open(self.file, "rb+")
            corruptedFile = open(self.new_file, "wb+")
        except FileNotFoundError:
            self.attach_file()
            return

        HEX = self.is_hex.get()
        start = self.startByteEntry.get()
        end = self.endByteEntry.get()
        blockSize = self.byteBlockSizeEntry.get()
        blockSpace = self.byteBlockSpaceEntry.get()
        addByte = self.addByteEntry.get()
        minByte = self.minByteEntry.get()
        maxByte = self.maxByteEntry.get()
        targetByte = self.targetByteEntry.get()
        replaceByte = self.replaceWithEntry.get()

        if HEX: # converting hexadecimal to integer
            start = int(start, 16)
            end = int(end, 16)
            blockSize = int(blockSize, 16)
            blockSpace = int(blockSpace, 16)
            addByte = int(addByte, 16)
            minByte = int(minByte, 16)
            maxByte = int(maxByte, 16)
            targetByte = int(targetByte, 16)
            replaceByte = int(replaceByte, 16)

        # for the swapper engine
        currentByteList1 = []
        bufferList = []
        currentByteList2 = []

        def copy_file_contents(mainFile, corruptedFile, endByte):
            for z in range(0, endByte):
                currentByte = mainFile.read(1)
                corruptedFile.write(currentByte)

        def corrupt(baseFile, corruptedFile, blockSpace):
            for y in range(0, int(blockSize)):
                currentByte = baseFile.read(1)
                if currentByte == b"":
                    break
                currentByte = int.from_bytes(currentByte, byteorder="big")

                if self.engine.get() == 1: # Increase bytes
                    currentByte += int(addByte)

                if self.is_random and self.engine.get() == 1:
                    if self.is_replaced: # Replace and randomize bytes
                        currentByte = 0
                        currentByte += random.randint(int(minByte), int(maxByte))
                    else: # Randomize without replacing bytes
                        currentByte += random.randint(int(minByte), int(maxByte))

                if self.is_replaced and self.engine.get() == 2: # Replace bytes
                    if self.is_exclusive.get(): # exclusive on
                        if currentByte == int(targetByte):
                            currentByte = int(replaceByte)
                    else: # exclusive off
                        currentByte = int(replaceByte)

                if currentByte > 255 or currentByte < 0: # if byte bigger than 255 or less than 0
                    currentByte = currentByte % 255
                currentByte = currentByte.to_bytes(1, byteorder="big")
                corruptedFile.write(currentByte)

            copy_file_contents(baseFile, corruptedFile, blockSpace)

        baseFile.seek(0)
        copy_file_contents(baseFile, corruptedFile, int(start))

        corruptStepSize = int(blockSize) + int(blockSpace)
        for x in range(int(start), int(end), corruptStepSize):
            corrupt(baseFile, corruptedFile, int(blockSpace))

        while True:
            currentByte = baseFile.read(1)
            if currentByte == b"": break
            corruptedFile.write(currentByte)

        baseFile.close()
        corruptedFile.close()

    def attach_file(self, event=None):
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
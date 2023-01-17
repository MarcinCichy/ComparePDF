from tkinter import *


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.txt_enterField = Text(frm_Second_Frame, width=80, height=25)  # ,width = 100, height = 100
        self.txt_enterField.grid(row=1, column=0, padx=2, pady=10, sticky=NE)
        scrollbar = Scrollbar(frm_Second_Frame, orient='vertical', command=self.txt_ListOfFiles.yview)
        scrollbar.grid(row=1, column=2, sticky='NS')
        self.txt_enterField.config(yscrollcommand=scrollbar.set)
		
		
root = Tk()
root.title('bin2txt Converter')
root.geometry('900x550')
app = Application(root)
root.mainloop()
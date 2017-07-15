import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

class Application(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
		self.createWidgets()

	def createWidgets(self):
		pic = Image.open("df-icon.png")
		pic = pic.resize((35,35))
		self.img = ImageTk.PhotoImage(pic)
		print(self.img.height())
		print(self.img.width())
		self.c = tk.Canvas(self)
		self.c.grid()
		self.c.create_image(0,0,anchor=tk.NW,image=self.img)
		
		self.button = tk.Button(self,image=self.img)
		self.button.grid()
		
		
app = Application()
app.master.title('Masterwork Dwarf Fortress')
app.mainloop()
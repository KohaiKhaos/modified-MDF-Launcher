import tkinter as tk
import ttk





class Application(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master)
		self.columnconfigure(0,minsize=50)
		self.rowconfigure(0,minsize=50)
		self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
		self.createWidgets()
		
	def createWidgets(self):
		
		txt = tk.StringVar()
		txt.set("Red")
		button = ttk.Menubutton(self,direction="flush",text="red",textvariable=txt)
		button.grid()
		
		menu = tk.Menu(button,tearoff=0)
		menu.add_radiobutton(label = "Red")
		menu.add_radiobutton(label = "Blue")
		menu.add_radiobutton(label = "Green")
		
		button['menu'] = menu
		
app = Application()
app.master.title('Masterwork Dwarf Fortress')
app.mainloop()
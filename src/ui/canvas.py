#  _______           __ ______ __                __               
# |   |   |.-----.--|  |      |  |--.-----.----.|  |--.-----.----.
# |       ||  _  |  _  |   ---|     |  -__|  __||    <|  -__|   _|
# |__|_|__||_____|_____|______|__|__|_____|____||__|__|_____|__|  

# Re-Usable UI Elements - Scrollable Canvas Tab

# (c) 2021 JTSage.  MIT License.
import tkinter as Tk
import tkinter.ttk as ttk

class ModCheckCanvasTab() :
	"""
	Build a ttk.Canvas (scrollable) tab

	Args:
		notebookTab (object): Parent Element
		title (str): Title of this tab
		description (str): Description of this tab
		extraText (list, optional): Extra info to display. Defaults to None.
		hideCanvas (bool, optional): Set to True to hide the scrollable canvas. Defaults to False.
	""" 

	def __init__(self, notebookTab, title, description, extraText=None, hideCanvas = False) :
		self.title        = title
		self._notebookTab = notebookTab
		self._description = description
		self._extraText   = extraText
		self._hideCanvas  = hideCanvas

		self._vertScrollbar = None
		self._scrollCanvas  = None
		self._inCanvasFrame = None

		self._build()

	def _build(self) :
		"""Build the canvas inside _parent """

		ttk.Label(self._notebookTab, text=self.title, font='Calibri 12 bold').pack()
		ttk.Label(self._notebookTab, text=self._description, wraplength = 640).pack(fill='x')

		if self._extraText is not None :

			for idx, thisText in enumerate(self._extraText, start=1) :
				padY = (
					10 if idx == 1 else 0,
					10 if idx == len(self._extraText) else 0
				)

				ttk.Label(self._notebookTab, text=thisText, anchor='w').pack(padx=(30,0), pady=padY, fill='x')


		if ( not self._hideCanvas ) :

			self._scrollCanvas   = Tk.Canvas(self._notebookTab, bd=2, relief='ridge')
			self._vertScrollbar  = ttk.Scrollbar(self._notebookTab, orient="vertical", command=self._scrollCanvas.yview)
			self._inCanvasFrame  = ttk.Frame(self._scrollCanvas, border=1, padding=(30,0))

			self._inCanvasFrame.bind(
				"<Configure>",
				lambda e: self._scrollCanvas.configure(
					scrollregion=self._scrollCanvas.bbox("all")
				)
			)

			self._scrollCanvas.create_window((0, 0), window=self._inCanvasFrame, anchor="nw")
			self._scrollCanvas.configure(yscrollcommand=self._vertScrollbar.set)
			self._scrollCanvas.pack(side="left", fill="both", expand=True)

			self._vertScrollbar.pack(side="right", fill="y")

			self._inCanvasFrame.bind('<Enter>', self._bound_to_mousewheel)
			self._inCanvasFrame.bind('<Leave>', self._unbound_to_mousewheel)

	def _on_mousewheel(self, event):
		""" Handle mousewheel events """
		self._scrollCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def _bound_to_mousewheel(self, event):
		""" Bind mousewheel events """
		self._scrollCanvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def _unbound_to_mousewheel(self, event):
		""" Unbind mousewheel events """
		self._scrollCanvas.unbind_all("<MouseWheel>")

	def clear_items(self) :
		"""Clear the canvas of data items """
		for widget in self._inCanvasFrame.winfo_children():
			widget.destroy()

	def add_item(self, term, desc) :
		"""Add an item to the scrollable canvas

		Args:
			term (str): Title of the item (bold, bulleted)
			desc (str): Description text (normal, indented)
		"""

		ttk.Label(
			self._inCanvasFrame,
			text   = "\u2022 " + term,
			anchor = 'w',
			font   = 'Calibri 9 bold'
		).pack(fill = 'x', padx = 0, pady = (10,0))

		ttk.Label(
			self._inCanvasFrame,
			text       = desc,
			anchor     = 'w',
			wraplength = 540 # (640-30-30-40)
		).pack(fill = 'x', pady = 0, padx = (40,0))


	

import tkinter as Tk
import tkinter.ttk as ttk
import locale

class ModCheckTreeTab() :

	def __init__(self, parent, title, description, columns, base, columnExtra=None) :
		self._parent      = parent
		self._UIParts     = {}
		self.title        = title
		self._description = description
		self._base        = base

		self._columns     = [("#"+str(i),j) for i,j in zip(range(1,len(columns)+1), columns)]
		self._columnExtra = columnExtra

		self._build()

	def _build(self) :
		ttk.Label(self._parent, text=self.title, font='Helvetica 12 bold').pack()
		ttk.Label(self._parent, text=self._description, wraplength = 600).pack(fill='x')

		self._UIParts["tree"] = ttk.Treeview(self._parent, selectmode='browse', columns=self._columns, show='headings')
		self._UIParts["tree"].pack(expand=True, side='left', fill='both', pady=(5,0))

		if self._columnExtra is not None :
			for thisExtraKey in self._columnExtra.keys():
				self._UIParts["tree"].column(thisExtraKey, **self._columnExtra[thisExtraKey])

		self._UIParts["VSB"] = ttk.Scrollbar(self._parent, orient="vertical", command=self._UIParts["tree"].yview)
		self._UIParts["VSB"].pack(side='right', fill='y', pady=(25,2))

		self._UIParts["tree"].configure(yscrollcommand=self._UIParts["VSB"].set)

		for col,name in self._columns:
			self._UIParts["tree"].heading(col, text=name, command=lambda _col=col: \
 				 self._treeview_sort(self._UIParts["tree"], _col, False))

		self._UIParts["tree"].bind("<Double-1>", self._on_double_click)

	def _on_double_click(self, event):
		thisItem    = self._UIParts["tree"].identify('item',event.x,event.y)
		thisModName = self._UIParts["tree"].item(thisItem,"text")
		thisMod     = self._base._modList[thisModName]
		thisInfoBox = Tk.Toplevel(self._parent.winfo_toplevel())

		thisInfoBox.title(thisModName)
		thisInfoBox.geometry("650x250")
	
		ttk.Label(thisInfoBox, text=thisModName, font='Helvetica 14 bold', anchor='center').pack(fill='x', pady=(10,10))

		if thisMod.name() is not None:
			ttk.Label(thisInfoBox, font='Helvetica 12', text=thisMod.name(), anchor='center').pack(fill='x')

		ttk.Label(thisInfoBox, text="", anchor='center').pack(fill='x')

		if thisMod.isNotMissing() :
			ttk.Label(thisInfoBox, text=thisMod.fullPath(), anchor='center').pack(fill='x')
			ttk.Label(thisInfoBox, text=self._base._IOStrings["size-on-disk"] + ": " + str(locale.format_string("%d", thisMod._fileSize, grouping=True)) + " (" + thisMod.size() + ")", anchor='center').pack(fill='x', pady=(5,0))
		else :
			ttk.Label(thisInfoBox, text=self._base._IOStrings["mod-file-not-found"], anchor='center').pack(fill='x')
		
		ttk.Label(thisInfoBox, text=self._base._IOStrings["active-in"] + ": " + thisMod.getAllActiveHR(), anchor='center').pack(fill='x', pady=(10,0))
		ttk.Label(thisInfoBox, text=self._base._IOStrings["used-in"] + ": " + thisMod.getAllUsedHR(), anchor='center').pack(fill='x', pady=(10,0))

		thisOkButton = ttk.Button(thisInfoBox, text=self._base._IOStrings["ok-button-label"], command=thisInfoBox.destroy)
		
		thisOkButton.pack(side="bottom", fill='x', padx=40, pady=(0,20))
		thisOkButton.bind('<Return>', lambda event=None: thisOkButton.invoke())
		thisOkButton.focus()

		thisInfoBox.bind("<Escape>", lambda x: thisInfoBox.destroy())

	def clear_items(self) :
		self._UIParts["tree"].delete(*self._UIParts["tree"].get_children())

	def add_item(self, name, values):
		self._UIParts["tree"].insert(
			parent = '',
			index  = 'end',
			text   = name,
			values = values)

	def _treeview_sort(self, tv, col, reverse):
		l = [(self._size_to_real_num(tv.set(k, col)), k) for k in tv.get_children('')]

		l.sort(
			key=lambda t : self._lower_if_possible(t),
			reverse=reverse
		)		

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l): # pylint: disable=unused-variable
			tv.move(k, '', index)

		# reverse sort next time
		tv.heading(col, command=lambda _col=col: \
				 self._treeview_sort(tv, _col, not reverse))

	def _size_to_real_num(self, text) :
		try :
			num, ext = text.split()

			if ext == "B":
				return float(num)
			if ext == "Kb" :
				return float(num) * 1024
			if ext == "Mb" :
				return float(num) * 1024 * 1024
			if ext == "Gb" :
				return float(num) * 1024 * 1024 * 1024
		
		except ValueError :
			return text

		return text

	def _lower_if_possible(self, x):
		if isinstance(x[0], float) :
			return x
		else :
			try:
				return (x[0].lower(), x[1])
			except AttributeError:
				return x
	
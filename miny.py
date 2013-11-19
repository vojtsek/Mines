# -*- coding: utf-8 -*-

# Zápočtový program - Hledání min
# Vojtěch Hudeček, zimní semestr, ak. rok 2012/13
# předmět: programování I  NPRG030, kruh 41
#
#


#import použitých knihoven, standartní součást Pythonu
import wx, math, random, time, pickle
import wx.lib.buttons as buttons

wx.SetDefaultPyEncoding('utf-8')

class Choice(wx.Frame):
	
# Třída dědící od objektu knihovny wx Frame
# Slouží pro zobrazení okna s výběrem parametrů hry

	def __init__ (self,parent):

# konstruktor třídy Choice
# Provede inicializaci rodičovského objektu Frame, okno má pevnou velikost
# Nastaví se implicitní rozměry, koeficient obtížnosti a počet min
# Volá se incicializační metoda init()

		super(Choice,self).__init__(parent,title='Volba parametrů',style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,size=(400,230))
		self.Centre()
		self.width = 8 # počet polí na šířku
		self.height = 8 # pole na výšku
		self.count = self.width * self.height # počet polí
		self.q = 0.15 # koeficient obtížnosti
		self.mines = math.trunc(math.ceil(self.count * self.q)) # počet min
		self.init()


		
	def init(self):
		
# Inicializační metoda, vytvoření komponent GUI a přiřazení obsluh událostí

		wx.StaticText(self,label='Velikost (Š x V)',pos=(15,20)) # štítky
		wx.StaticLine(self,pos=(10,40),size=(150,2))
		
		wx.StaticText(self,label='Počet min',pos=(185,20))
		wx.StaticLine(self,pos=(180,40),size=(150,2))
		
		self.size8 = wx.RadioButton(self,label='8 x 8',id=8,pos=(30,50),style = wx.RB_GROUP) # skupina RadioButtons pro výběr rozměrů
		self.size16 = wx.RadioButton(self,label='16 x 16',id=16,pos=(30,80))
		self.size24 = wx.RadioButton(self,label='24 x 16',id=24,pos=(30,110))
		self.sizeC = wx.RadioButton(self,label='',id=100,pos=(30,140)) # volitelné rozměry
		self.customWidth = wx.SpinCtrl(self,value=str(1),pos=(55,140),size=(55,30),min=2,max=30,id=101) # šířka, maximum je 30 polí
		self.customWidth.Disable() # rozměry je možné volit pouze při zvolení příslušného RadioButton
		wx.StaticText(self,label='x',pos=(111,145))
		self.customHeight = wx.SpinCtrl(self,value=str(1),pos=(120,140),size=(55,30),min=2,max=18,id=102) # výška maximum je 18 polí
		self.customHeight.Disable()			
		
		# skupina RadioButtons pro výběr počtu min, ve skutečnosti se volí koeficient
		self.easy = wx.RadioButton(self,label=str(math.trunc(math.ceil(self.count * 0.15)))+' (lehká)',id=2,pos=(200,50),size=(120,25),style = wx.RB_GROUP)
		self.medium = wx.RadioButton(self,label=str(math.trunc(math.ceil(self.count * 0.35)))+' (střední)',id=4,pos=(200,80),size=(120,25))
		self.hard = wx.RadioButton(self,label=str(math.trunc(math.ceil(self.count * 0.55)))+' (těžká)',id=6,pos=(200,110),size=(120,25))
		self.custom = wx.RadioButton(self,label='',id=103,pos=(200,140)) # volitelný počet
		self.customCount = wx.SpinCtrl(self,value=str(self.mines),pos=(225,140),size=(55,30),min=0,max=self.count-1,id=104)
		self.customCount.Disable() # pouze při zvolení příslušného RadioButton
		
		# přiřazení obsluhy události při změně rozměrů
		self.size8.Bind(wx.EVT_RADIOBUTTON,self.SetS)
		self.size16.Bind(wx.EVT_RADIOBUTTON,self.SetS)
		self.size24.Bind(wx.EVT_RADIOBUTTON,self.SetS)
		self.sizeC.Bind(wx.EVT_RADIOBUTTON,self.SetS)
		self.customWidth.Bind(wx.EVT_SPINCTRL,self.SetS)
		self.customHeight.Bind(wx.EVT_SPINCTRL,self.SetS)
		
		# přiřazení obsluhy události při změně počtu min
		self.easy.Bind(wx.EVT_RADIOBUTTON,self.SetC)
		self.medium.Bind(wx.EVT_RADIOBUTTON,self.SetC)
		self.hard.Bind(wx.EVT_RADIOBUTTON,self.SetC)
		self.custom.Bind(wx.EVT_RADIOBUTTON,self.SetC)
		self.customCount.Bind(wx.EVT_SPINCTRL,self.SetC)
		
		# štítek a tlačítko pro potvrzení volby a začátek hry
		self.lbl = wx.StaticText(self,label='8x8, 10 min',pos=(100,185))
		self.new = wx.BitmapButton(self,1024,wx.Bitmap('./images/ok_transp.png'),pos=(210,180))
		self.new.SetFocus()
		# přiřazení obsluhy události
		self.new.Bind(wx.EVT_BUTTON,self.Create)
		#zobrazení okna
		self.Show(True)
		
	def SetS(self, e):
		
# Metoda volaná při změně rozměrů, nastaví rozměry, počet min 

		# získání id komponenty která vyvolal událost
		id = e.GetId()
		if id == 8: # rozměr 8x8, nastavení rozměrů, zákaz volby vlastních
			h = w = 8
			self.customHeight.Disable()
			self.customWidth.Disable()
		elif id == 16: # rozměr 16x16
			self.customHeight.Disable()
			self.customWidth.Disable()
			h = w = 16
		elif id == 24: # rozměr 24x16
			self.customHeight.Disable()
			self.customWidth.Disable()
			h = 16
			w = 24
		elif id == 100: # vlastní rozměry, povolení volby a nastavení výšky a šířky
			self.customHeight.Enable()
			self.customWidth.Enable()
			w = self.customWidth.GetValue()
			h = self.customHeight.GetValue()
		else: # vlastní rozměry, povolení volby a nastavení výšky a šířky
			w = self.customWidth.GetValue()
			h = self.customHeight.GetValue()
		# nastavení rozměrů
		self.Set(w,h,self.q)
		
	def SetC(self, e):
		
# Metoda volaná při změně počtu min

		id = e.GetId()
		if id == 2: # nastavení koeficientu obtížnosti
			q = 0.15
			self.customCount.Disable()
		elif id == 4:
			q = 0.35
			self.customCount.Disable()
		elif id == 6:
			q = 0.55
			self.customCount.Disable()
		elif id == 103: # vlastní počet min, výpočet koeficientu, zpřistupnění pole pro volbu počtu
			q = float(self.customCount.GetValue()) / self.count # koeficient je s plovoucí čárkou, jinak by byl jen 0 nebo 1
			self.customCount.Enable()
		elif id == 104: # vlastní počet min, výpočet koeficientu
			q = float(self.customCount.GetValue()) / self.count
		self.Set(self.width,self.height,q)
		
	def Set(self,w,h,q):
	
# Nastavení zvolených hodnot do proměnných
		self.width = w
		self.height = h
		self.q = q
		self.count = self.width * self.height
		self.mines = math.trunc(math.ceil(self.count * self.q)) # výpočet počtu min
		self.customCount.SetRange(1,self.count-1) # nastavení maximálního možného počtu min
		# přepočítání počtu min pro dané rozměry a změna štítků
		self.easy.SetLabel(str(math.trunc(math.ceil(self.count * 0.15))) + ' (lehká)')
		self.medium.SetLabel(str(math.trunc(math.ceil(self.count * 0.35))) + ' (střední)')
		self.hard.SetLabel(str(math.trunc(math.ceil(self.count * 0.55))) + ' (těžká)')
		self.lbl.SetLabel(str(w) + 'x' + str(h) + ', '+str(self.mines)+' min')
		
	def Create(self, e):
# Metoda pro vytvoření nové hry.
# Zavře okno s výběrem a vytvoří instanci třídy Game  se zvolenými hodnotami a tu předá konstruktoru třídy Mines
		self.Close()
		g = Game(self.width,self.height,self.count,self.mines)
		Mines(None,g)
		
class Field:

# Třída Field nese informace o poli, pro každé pole existuje její instance 

	def __init__ (self,n):
		
		# Konstruktor, nastavení hodnot
		
		self.mine = False; # jestli pole obsahuje minu
		self.cMines = 0; # počet sousedních polí s minami
		self.clicked = False; # jestli je pole odkliknuto
		self.cClicked = 0; # počet sousedních odkliknutých polí
		self.flagged = False; # jestli je pole označeno
		self.cFlagged = 0; # počet sousedních označených polí
		self.neighbours = n # počet sousedů

class Results:

# Pomocná třída slouží pro uložení výsledků do souboru
# při inicializaci se vytvoří seznam výsledků předaných konstrukotru, při ukládání se přidá nový výsledek
# metoda GetResults pouze vrací seznam výsledků
 
	def __init__(self,results):
		self.scores = list()
		for i in range(0,len(results)):
			self.scores.append(results[i])
	def GetResults(self):
		return self.res		
		
class Game:

# Třída Game nese všechny důležité informace o aktuálním stavu hry, ty jsou uloženy ve statických proměnných

	def __init__ (self,width,height,count,mines):
		
		# Konstruktor, nastavení předaných a implicitních hodnot
		
		self.count = count # počet polí
		self.mines = mines # počet min
		try: # načtení výsledků ze souboru pro daný rozměr, pokud existuje
			resFile = open('./results/results_'+str(self.mines),'r+')
			results = pickle.load(resFile)
			self.highscores = results
		except: # soubor s výsledky neexistuje
			self.highscores = Results(list())
		self.missFlag = -1 # proměnná uchovávající id pole, které je špatně označeno, používá se při nápovědě
		self.width = width # šířka
		self.hintLvl = 3
		self.height = height # výška
		self.movesCount = 0 # počet tahů
		self.minePos = [0] * mines # pole s pozicemi min
		self.flagPos = LinkedList() # spojový seznam s pozicemi označených polí
		self.possibleMoves = LinkedList() # spojový seznam s pozicemi, které mohou vést k dalšímu tahu
		self.moves = LinkedList() # spojový seznam tahů, umožňuje krok(y) zpět
		self.flagged = 0 # počet označených polí
		self.mismatches = 0 # počet mylně označených polí
		self.fields = [0] * count # pole instancí třídy Field
		for i in range(0,height):
			for j in range(0,width): # inicializace každého pole
				if (i == 0) or (i == height-1): # počet sousedů
					if (j==0) or (j == width -1):
						n = 3 # v rohu
					else:
						n = 5 # na kraji
				elif (j==0) or (j == width -1):
					n = 5 # na kraji
				else:
					n = 8 # uprostřed
				self.fields[i*width + j] = Field(n) # vytvoření instance
				
	def NotifyNeighbours(self,id,attr,op):
	
# Metoda sloužící pro změnu stavu okolních polí

		limitU = self.count # minimální a maximální možné id
		limitD = -1
		# Postupně se prochází všechna okolní pole (hlídá se okraj a přesáhnutí limitu)
		# sousedům se změní atribut předaný parametrem (inc / dec podle parametru)
		if (id - 1 > limitD) and (id % self.width != 0):
			exec('self.fields[id-1].'+attr+' '+op+'= 1')
		if id-self.width > limitD:
			exec('self.fields[id-self.width].'+attr+' '+op+'= 1')
		if (id-self.width-1 > limitD) and (id % self.width != 0):
			exec('self.fields[id-self.width-1].'+attr+' '+op+'= 1')
		if (id-self.width+1 > limitD) and ((id + 1) % self.width != 0):	
			exec('self.fields[id-self.width+1].'+attr+' '+op+'= 1');
		if (id+1 < limitU) and ((id + 1) % self.width != 0):
			exec('self.fields[id+1].'+attr+' '+op+'= 1')
		if id+self.width < limitU:	
			exec('self.fields[id+self.width].'+attr+' '+op+'= 1')
		if (id+self.width+1 < limitU) and ((id + 1) % self.width != 0):
			exec('self.fields[id+self.width+1].'+attr+' '+op+'= 1')
		if (id+self.width-1 < limitU) and (id % self.width != 0):	
			exec('self.fields[id+self.width-1].'+attr+' '+op+'= 1') 
		
	def SetMines(self,id):
		
# Metoda sloužící pro rozsetí min. Vyvoláno po prvním tahu

		flds = [0] * self.count # pole neobsazených indexů
		for j in range(0,self.count-1): # inicializace
			flds[j] = j
		tmp = flds[id]
		flds[id] = self.count - 1 # vyřazení pole, které vyvolalo událost. To zaručí, že prvním tahem nestoupneme na minu.
		flds[self.count - 1] = tmp
		for i in range(0,self.mines):
			# Pro každou minu je náhodně zvolena pozice a ta je následně vyřazena ze seznamu možností
			# To se děje výměnou s posledním možným prvkem a následným zmenšením pole.
			a = random.randint(0,self.count-i-2)
			self.fields[flds[a]].mine = True
			self.minePos[i] = flds[a]
			self.NotifyNeighbours(flds[a],'cMines','+') # změna stavu sousedů
			if self.fields[flds[a]].flagged == True: # pokud již bylo pole s minou označeno, zmenší se počet chybných označení
				self.mismatches -= 1
			tmp = flds[a]
			flds[a] = flds[self.count-i-2]
			flds[self.count-i-1] = tmp 
			
class ListNode:

# Třída simulující uzel obousměrného spojového seznamu
# uzel obsahuje id pole a ukazatele

	def __init__(self, fieldId,prev):
		self.fieldId = fieldId
		self.prev = prev
		self.next = None

class LinkedList:
	
# Třída simulující obousměrný spojový seznam, nese informace o prvním a posledním prvku a počtu uzlů

	def __init__(self):
		
		# Inicializace seznamu
		
		self.head = None
		self.tail = None
		self.count = 0
		
	def Insert(self,id):
		
		# Operace vložení prvku
		
		if self.tail != None: # Seznam není prázdný, přidání na konec
			new = ListNode(id,self.tail)
			self.tail.next = new
		else: # Vytvoření uzlu
			new = ListNode(id,None)
		if self.head == None: # Seznam je prázdný, nastavení prvního prvku
			self.head = new
		self.tail = new # nastavení posledního prvku
		self.count += 1 # změna počtu
		
	def RemoveBy(self,id):
		
		# Vyjmutí prvku podle hodnoty
		
		node = self.head
		while node != None: # nalezení prvku s danou hodnotu pomocí průchodu senzmamem a jeho následné vyjmutí
			if node.fieldId == id:
				self.Remove(node)
				break
			node = node.next
			
	def Remove(self,node):
		
		# Vyjmutí daného prvku ze spojového seznamu
		
		if node.prev != None: # existuje předchozí prvek, přepojení
			node.prev.next = node.next
		else:
			if node.next != None: # je to první prvek, má následníka
				self.head = node.next # přesunutí prvního prvku
				node.next.prev = None # nastavení předchůdce
			else:
				self.tail = None # je to jednoprvkový seznam
				self.head = None
		if node.next != None: # přepojení
			node.next.prev = node.prev
		else:
			if node.prev != None: # má předchůdce, ale ne následníka
				self.tail = node.prev # přesunutí posledního prvku
				node.prev.next = None # přepojení
			else:
				self.tail = None # jednoprvkový seznam
				self.head = None
		del node # odstranění uzlu z paměti
		self.count -= 1 # změna počtu
			
class Mines (wx.Frame):
	
# Třída dědící od wx.Frame
# Zobrazí herní okno, má k dispozici instanci třídy Game
# Dále obsahuje řadu metod umožňujícíh hru
	
	def __init__ (self,parent,g):
		
		# Konstruktor, nastaví hodnoty proměnných, vytvoří okno s předanými a přepočitanými rozměry
		# Vytvoří časovač a nastaví jeho obsluhu
		# Zavolá inicializační metodu
		
		self.game = g
		self.end = False
		if self.game.width * 36 > 450:
			w =self.game.width * 36
		else:
			w = 450
		super(Mines,self).__init__(parent,title='Hledání min',size=(w,self.game.height*36 + 60))
		self.timer = wx.Timer(self,-1)
		self.Bind(wx.EVT_TIMER, self.OnTick)
		self.Centre()
		self.init()

	def init(self):	
	
	# inicializační metoda, vytvoří potřebné GUI komponenty
	
		vbox = wx.BoxSizer(wx.VERTICAL) # layout
		layout = wx.GridSizer(self.game.height,self.game.width,1,1)
		
		menu_bar = wx.MenuBar() # vytvoření nabídky a přidání položek
		file_menu = wx.Menu()
		item_new = wx.MenuItem(file_menu,1,'Nová hra')
		item_reset = wx.MenuItem(file_menu,2,'Reset')
		item_results = wx.MenuItem(file_menu,3,'Výsledky')
		hint = wx.Menu()
		item_lvl1 = wx.MenuItem(hint,11,'Vypnuto',kind = wx.ITEM_RADIO)
		item_lvl2 = wx.MenuItem(hint,12,'Level 1',kind = wx.ITEM_RADIO)
		item_lvl3 = wx.MenuItem(hint,13,'Level 2',kind = wx.ITEM_RADIO)
		hint.AppendItem(item_lvl1)
		hint.AppendItem(item_lvl2)
		hint.AppendItem(item_lvl3)
		item_lvl3.Check()
		file_menu.AppendItem(item_new)
		file_menu.AppendItem(item_reset)
		file_menu.AppendItem(item_results)
		file_menu.AppendMenu(wx.ID_ANY,'Nápověda',hint)
		menu_bar.Append(file_menu,'Možnosti')
		self.SetMenuBar(menu_bar)
		
		# načtení obrázků ze souborů, konverze na potřebné rozměry a do bitmapy
		
		bmp = wx.Image("./images/explode.png", wx.BITMAP_TYPE_PNG)
		self.expl = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/mine.png", wx.BITMAP_TYPE_PNG)
		self.mine = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/ok_transp.png", wx.BITMAP_TYPE_PNG)
		self.ok = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/one.png", wx.BITMAP_TYPE_PNG)
		self.one = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/two.png", wx.BITMAP_TYPE_PNG)
		self.two = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/three.png", wx.BITMAP_TYPE_PNG)
		self.three = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/four.png", wx.BITMAP_TYPE_PNG)
		self.four = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/five.png", wx.BITMAP_TYPE_PNG)
		self.five = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/six.png", wx.BITMAP_TYPE_PNG)
		self.six = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/seven.png", wx.BITMAP_TYPE_PNG)
		self.seven = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/eight.png", wx.BITMAP_TYPE_PNG)
		self.eight = bmp.Rescale(25, 25).ConvertToBitmap()
		bmp = wx.Image("./images/danger.png", wx.BITMAP_TYPE_PNG)
		self.danger = bmp.Rescale(30, 30).ConvertToBitmap()
		bmp = wx.Image("./images/cross.png", wx.BITMAP_TYPE_PNG)
		self.cross = bmp.Rescale(30, 30).ConvertToBitmap()
		self.nullBmp = wx.EmptyBitmap(0,0)
				
		for i in range(0,self.game.count): # Vytvoření tlačítek, pomocí knihovny wx, přidání do layoutu a nastavení obsluhy událostí při kliku pravým a levým tlačítkem myši
			button = buttons.GenBitmapToggleButton(self,i,self.nullBmp,size=(35,35))
			layout.Add(button)
			button.Bind(wx.EVT_BUTTON,self.Click,id=i)
			button.Bind(wx.EVT_RIGHT_DOWN,self.Rclick,id=i)
				
		self.toolbar = self.CreateToolBar() # vytvoření nástrojové lišty, přidání ovládacích a informačních prvků
		new = self.toolbar.AddLabelTool(wx.ID_ANY,'Reset',wx.Bitmap('./images/new.png')) # reset hry
		res = self.toolbar.AddLabelTool(wx.ID_ANY,'Nová hra',wx.Bitmap('./images/reset.png')) # vytvoření nové hry
		self.hint = self.toolbar.AddLabelTool(wx.ID_ANY,'Hint',wx.Bitmap('./images/hint.png')) # nápověda
		self.back = self.toolbar.AddLabelTool(15,'Back',wx.Bitmap('./images/back.png')) # krok zpět
		self.toolbar.AddSeparator()
		self.counter = wx.StaticText(self.toolbar,label='Označeno: '+str(self.game.flagged)+'/'+str(self.game.mines)) # počet označených polí
		self.timeLbl = wx.StaticText(self.toolbar,label='00:00') # uplynulý čas
		self.toolbar.EnableTool(15,False) # znepřístupnění krkou zpět (na začátku nemá smysl)
		self.toolbar.AddControl(self.counter)
		self.toolbar.AddSeparator()
		self.toolbar.AddControl(self.timeLbl)
		self.toolbar.Realize()
		
		# přidání obsluhy událostí		
		self.Bind(wx.EVT_MENU,self.Reset,id=2)
		self.Bind(wx.EVT_MENU,self.New,id=1)
		self.Bind(wx.EVT_MENU,self.ShowScores,id=3)
		self.Bind(wx.EVT_MENU,self.SetHint,id=11)
		self.Bind(wx.EVT_MENU,self.SetHint,id=12)
		self.Bind(wx.EVT_MENU,self.SetHint,id=13)
		self.Bind(wx.EVT_TOOL,self.Reset,res)
		self.Bind(wx.EVT_TOOL,self.New,new)
		self.Bind(wx.EVT_TOOL,self.CallHint,self.hint)
		self.Bind(wx.EVT_TOOL,self.Back,self.back)
		
		# vložení layoutu na pozice, zobrazení okna
		vbox.Add(layout,flag=wx.ALIGN_CENTER)
		self.SetSizer(vbox)
		self.Show(True)
	def SetHint(self,e):
		
		# Nastaví úroveň nápovědy
		
		self.game.hintLvl = e.GetId() - 10
		
	def ShowScores(self,e):
		
		# Metoda volaná z menu, zobrazení výsledků načtených v konstruktoru třídy Game v dialogovém okně.
		# Seřazeno vzestupně
		
		scoreList = self.game.highscores.scores
		scores = ''
		scoreList.sort()
		for i in range(0,len(scoreList)):
			scores += '\n '+str(i+1) +'. '+ self.SecsToTime(scoreList[i])
		dial = wx.MessageDialog(None,scores, 'Výsledky', wx.OK)
		dial.ShowModal()	
		
	def Back(self, e):
		
		# Metoda zajišťující funkci krok zpět
		
		if self.game.moves.count > 1:	
			if self.end == True: # hra je skončena - šlápnutí na minu
				node = self.game.flagPos.head
				while node != None: # znovu zobrazí označená pole (skryje miny)
					btt = self.FindWindowById(node.fieldId)
					btt.SetBitmapLabel(self.danger)
					btt.SetValue(False)
					node = node.next
				self.end = False # znovunastavení proměnné indikující konec hry
				self.timer.Start(1000) # znovuspuštění časovače
			id = self.game.moves.tail # poslední tah
			if id != None:
				for i in id.fieldId: # fieldId může obsahovat i seznam - v případě, že  poslední tah odkryl více než jedno pole
				# znovu je "odkliknuto" dané pole
					btt = self.FindWindowById(i)
					field = self.game.fields[i]
					btt.SetValue(False)
					btt.SetBitmapLabel(self.nullBmp)
					self.game.movesCount	 -= 1 # snížení počtu tahů
					if field.clicked:
						self.game.NotifyNeighbours(i,'cClicked','-') # oznámení sousedům
					field.clicked = False
				self.game.moves.Remove(id) # odstranění tahu
			if self.game.movesCount <= 1: # je-li v situaci po prvím tahu, zakáže další krok zpět - zabrání znovurozsetí min
				self.toolbar.EnableTool(15,False)
		
			
	def Click(self,e):
		
		# Metoda vyvolaná po kliknutí levým tlačítkem na některé z polí
		
		self.moveList = list() # seznam tahů provedených na toto kliknutí
		if self.end != True: # není-li hra skončena
			if self.game.movesCount == 0: # je to první tah
				self.time = 0 # start časomíry
				self.timer.Start(1000)
				self.game.SetMines(e.GetId()); # rozsetí min
			else:
				self.toolbar.EnableTool(15,True) # zpřístupnění kroku zpět
			self.Move(e.GetId(),True) # provedení tahu metodou Move
			node = self.game.possibleMoves.head
			while(node != None): # procházení možných tahů a vyřazení těch, které už nejsou možné - všechna okolní pole jsou zaplněna
				if self.game.fields[node.fieldId].neighbours - self.game.fields[node.fieldId].cClicked -self.game.fields[node.fieldId].cFlagged<= 0:
					if node != None:
						self.game.possibleMoves.Remove(node)
						node = node.next
				else:
					node = node.next
		else: # hra je skončena, nijak se neovlivní stav tlačítek
			if self.game.fields[e.GetId()].clicked != True:
				self.FindWindowById(e.GetId()).SetValue(False)
			else:
				self.FindWindowById(e.GetId()).SetValue(True)
		self.game.moves.Insert(self.moveList) # vložení tahů, které proběhly do uzlu spojového seznamu
		if self.game.hintLvl > 1:
			self.Hint(True) # kontrola hratelnosti
	#	print self.game.fields[e.GetId()].cMines , ' Flagged: ',self.game.fields[e.GetId()].cFlagged,' Clicked: ',self.game.fields[e.GetId()].cClicked,' Neighbours: ',self.game.fields[e.GetId()].neighbours 
	#	print self.ReturnNeighbours(e.GetId())
					
	def Step(self,id,action):
		
		# Provede tah na jednom ze sousedních polí pole předaného parametrem
		
		self.moveList = list() # seznam provedených tahů
		n = self.ReturnNeighbours(id)
		for i in n: # procházení sousedů
			if (self.game.fields[i].flagged == False) and (self.game.fields[i].clicked == False): # soused není označen
				if action == 'click': # má se simulovat kliknutí levým tlačítkem
					if self.game.fields[i].mine == False: # dodatečná kontrola, neobsahuje-li minu
						self.Move(i,True) # provedení tahu
						self.toolbar.EnableTool(15,True) # povolení kroku zpět
						break # jen jedno pole
				else: # má se simulovat označení pole (pravé tlačítko)
					if self.game.fields[i].mine == True: # jde opravdu o pole s minou
						self.Mark(i) # provedení tahu
						self.FindWindowById(i).SetValue(False) 
						break # jen jedno pole
		self.game.moves.Insert(self.moveList) # vložení provedených tahů
		
	def Blink(self):
		
		# Pomocná metoda, obsahuje-li hra špatně označené pole, toto je zvýrazněno (křížkem) a je uložena jeho pozice, po volání časovače je znovu označeno
		
		node = self.game.flagPos.head
		while node != None:
			btt = self.FindWindowById(node.fieldId)
			field = self.game.fields[node.fieldId]
			if not field.mine:
				btt.SetBitmapLabel(self.cross)
				btt.SetValue(True)
				self.game.missFlag = node.fieldId
				break
			node = node.next
		
	def CallHint(self,e):
		
		# Volá funkci Hint
		
		if self.game.mismatches != 0: # některé z polí je špatně označeno
				self.Blink() # zvýraznění pole
		else:
			self.Hint(False)	
		
	def ReturnNeighbours(self,id):
		
		#  Metoda vrátí seznam sousedů pole předaného argumentem
		
		neighbours = list()
		limitU = self.game.count # limity podle počtu polí
		limitD = -1
		# senznam vzdáleností sousedů
		distances = [-1,-self.game.width,-self.game.width-1,-self.game.width+1,1,self.game.width,self.game.width+1,self.game.width-1]
		q = [id,1,id,id+1,id+1,1,id+1,id]
		for i in range(0,len(distances)): # procházení sousedů
			if (id + distances[i] > limitD) and (id + distances[i] < limitU) and (q[i] % self.game.width != 0): # jedná se o souseda
				neighbours.append(id+distances[i]) # připojení do seznamu
		return neighbours
			
	def Hint(self,control):
		
		# Stará se o nápovědu a kontrolu hratelnosti (určeno parametrem control)
		
		playable = False # je možné pokračovat?
		node = self.game.possibleMoves.head
		while(node != None): # procházení možných tahů
			if (self.game.fields[node.fieldId].neighbours - self.game.fields[node.fieldId].cClicked) <= (self.game.fields[node.fieldId].cMines ):
			# je jisté, že vedle tohoto pole už jsou všude miny 
				if control != True: # nejedná se o kontrolu
					self.Step(node.fieldId,'flag') # provedení tahu označením jednoho z polí
				else:
					playable = True	# jedná se o kontrolu, v tom případě je možné hrát dál
				break # nalezena možnost, konec
			elif (self.game.fields[node.fieldId].cFlagged == self.game.fields[node.fieldId].cMines) and (self.game.fields[node.fieldId].neighbours - self.game.fields[node.fieldId].cClicked - self.game.fields[node.fieldId].cFlagged > 0):
			# je jisté, že všechny miny kolem tohoto pole již jsou označeny
				if control != True: # nejedná se o kontrolu
					self.Step(node.fieldId,'click') # provedení tahu
					self.FindWindowById(node.fieldId).SetValue(True)
				else:
					playable = True # jedná se o kontrolu, v tom případě je možné hrát dál
				break # nalezena možnost, konec
			elif ((self.game.fields[node.fieldId].cMines - self.game.fields[node.fieldId].cFlagged) == 1) and (self.game.hintLvl == 3): # danému poli zbývá označit pouze 1 mina
				n = self.ReturnNeighbours(node.fieldId) # získání seznamu sousedů
				clickedN = list()
				unclickedN = list()
				possible = -1
				for i in n: # procházení sousedů a vytvoření seznamů odkrytých a neodkrytých polí
					if self.game.fields[i].clicked:
						clickedN.append(i)
					elif not self.game.fields[i].flagged:
						unclickedN.append(i)
				for i in unclickedN: # procházení neodkrytých polí
					if possible > -1:
						break
					for j in unclickedN:
						if i != j: # vynechá jedno z polí, ostatní odkryje (jen ve vnitřní struktuře)
							 self.game.NotifyNeighbours(j,'cClicked','+')
						else:
							self.game.NotifyNeighbours(j,'cFlagged','+') # vynechané pole označí
					for k in clickedN: # prochází neodkryté sousedy a zjišťuje, jestli označení daného pole neznemožní další tahy
						if (self.game.fields[k].cClicked + self.game.fields[k].cFlagged == self.game.fields[k].neighbours) and (self.game.fields[k].cMines != self.game.fields[k].cFlagged):
							possible = i # pokud by toto pole bylo označené, znemožnilo by to další tahy, mina na něm tedy určitě není
							break
					for j in unclickedN: # vrácení vnitřní struktury do původního stavu
						if i != j:
							self.game.NotifyNeighbours(j,'cClicked','-')
						else:
							self.game.NotifyNeighbours(j,'cFlagged','-')				
				if possible > -1:
					if control != True: # nejedná se o kontrolu
						self.Move(possible,True) # provedení tahu
						self.toolbar.EnableTool(15,True)
						self.FindWindowById(possible).SetValue(True)
					else:
						playable = True # jedná se o kontrolu, v tom případě je možné hrát dál
					break # nalezena možnost, konec
			node = node.next	# další uzel
		if (node == None) and (playable == False): # cyklus proběhl až na konec a není možné hrát
			node = self.game.possibleMoves.head
			if node != None: # pokud existuje alespoň jedno pole s volným okolím
				self.Step(node.fieldId,'click') # provede se jeden z tahů, uživatel ho nemohl předvídat
				# self.FindWindowById(node.fieldId).SetValue(True)
			else: # neexistuje ani jedno pole s volným okolím
				for i in range(0,self.game.count): # procházení všech polí
					fld = self.game.fields[i]
					if (fld.mine == False) and (fld.flagged == False) and (fld.clicked == False): # je-li možné toto pole odkrýt
						self.Move(i,True) # provede tah
						self.FindWindowById(i).SetValue(True)
						self.toolbar.EnableTool(15,True)
						break
		node = self.game.possibleMoves.head
		while(node != None): # procházení tahů a smazaní těch, které nově nejsou k dispozici
			if self.game.fields[node.fieldId].neighbours - self.game.fields[node.fieldId].cClicked -self.game.fields[node.fieldId].cFlagged<= 0:
				if node != None:
					self.game.possibleMoves.Remove(node)
					node = node.next
			else:
				node = node.next
		if playable == False: # nedá se hrát dál nebo se nejednalo o kontrolu
			try:
				self.Hint(True) # rekurzivní volání, dokud nebude možné pokračovat
			except:
				pass
				
	def SecsToTime(self,secs):
		
		# Jednoduchá pomocná metoda, která čas předaný v parametru v sekundách převede a vrátí řetězec ve formátu "mm:ss"
		
		m = secs / 60
		if m < 10:
			min = '0'+str(m)
		else:
			min = str(m)
		s = secs - m*60
		if s < 10:
			sec = '0'+str(s)
		else:
			sec = str(s)
		return min+':'+sec
		
	def OnTick(self,event):
		
		# Metoda vyvolaná při tiknutí časovače.
		# Inkrementuje uběhlý čas, případně znovu označí mylně zvolené pole
		
		self.time += 1
		self.timeLbl.SetLabel(self.SecsToTime(self.time))
		if self.game.missFlag > -1:
			btt = self.FindWindowById(self.game.missFlag)
			btt.SetBitmapLabel(self.danger)
			btt.SetValue(False)
		
	def ShowMines(self):
		
		# Zobrazí nevybuchlé miny, provede kontrolu označení
		
		for i in range(0,self.game.mines): # prochází miny
			if self.game.fields[self.game.minePos[i]].flagged != True:
				self.Move(self.game.minePos[i],False) # zobrazí pole s minou, bez výbuchu
		node = self.game.flagPos.head
		while node != None: # projde označená pole a rozliší ta označená správně a špatně
			btt = self.FindWindowById(node.fieldId)
			field = self.game.fields[node.fieldId]
			if field.mine:
				btt.SetBitmapLabel(self.ok)
			else:
				btt.SetBitmapLabel(self.cross)
			btt.SetValue(False)
			node = node.next
		
	def ShowPrev(self,id):
		
		# Metoda se zavolá při odkrytí pole, které nesouvisí s žádnou minou
		# prochází sousedy s menším id , pokud soused sousedí s minou, zastaví se, pokud ne, zavolá rekurzivně procházení dalších polí
		
		limitD = -1
		offset = -self.game.width-1
		if (id + offset > limitD) and (id % self.game.width != 0):
			if (self.game.fields[id+offset].clicked == False):
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowPrev(id+offset)
					self.ShowNext(id+offset)
		offset = - self.game.width
		if (id + offset > limitD):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowPrev(id+offset)
					self.ShowNext(id+offset)
		offset = - self.game.width+1
		if (id + offset > limitD) and ((id+1) % self.game.width != 0):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowPrev(id+offset)
					self.ShowNext(id+offset)
		offset = -1
		if (id + offset > limitD) and (id % self.game.width != 0):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowPrev(id+offset)	
					self.ShowNext(id+offset)
		
	def ShowNext(self,id):
		
		# Metoda se zavolá při odkrytí pole, které nesouvisí s žádnou minou
		# prochází sousedy s větším id , pokud soused sousedí s minou, zastaví se, pokud ne, zavolá rekurzivně procházení dalších polí
		
		limitU = self.game.count
		offset = self.game.width-1
		if (id + offset < limitU) and (id % self.game.width != 0):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowNext(id+offset)
					self.ShowPrev(id+offset)
		offset = self.game.width
		if (id + offset < limitU):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowNext(id+offset)
					self.ShowPrev(id+offset)
		offset = self.game.width+1
		if (id + offset < limitU) and ((id+1) % self.game.width != 0):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowNext(id+offset)
					self.ShowPrev(id+offset)
		offset = 1
		if (id + offset < limitU) and ((id+1) % self.game.width != 0):
			if self.game.fields[id+offset].clicked == False:
				self.Move(id+offset,False)
				if (self.game.fields[id+offset].cMines == 0):
					self.ShowNext(id+offset)
					self.ShowPrev(id+offset)
					
	def Rclick(self, e):
		
		# Obsluha události pravého kliku myší
		# Zavolá metodu označení a kontrolu hratelnosti
		
		self.Mark(e.GetId())	
		if self.game.hintLvl > 1:	
			self.Hint(True)
				
	def Mark(self,id):
		
		# Metoda (od)označí dané pole a provede akce s tím spojené
		
		if self.end != True: # Není konec hry
			btt = self.FindWindowById(id)
			if self.game.fields[id].clicked == False: # pole ještě není odkryto
				btt.SetValue(False)
				if self.game.fields[id].flagged == True: # pole je označeno
					if self.game.fields[id].mine == False: # neobsahuje minu
						self.game.mismatches -= 1 # zmenšení počtu chybných označení
					self.game.fields[id].flagged = False # odoznačení pole
					self.game.flagged -= 1 # zmenšení počtu označených polí
					self.counter.SetLabel('Označeno: '+str(self.game.flagged)+'/'+str(self.game.mines)) # změna štítku
					if self.game.fields[id].mine != False:
						self.game.NotifyNeighbours(id,'cFlagged','-') # oznámení sousedům
					self.game.flagPos.RemoveBy(id) # odstranění ze spojového seznamu
					if id == self.game.missFlag: # jedná se nalezené špatně označené pole, reset hodnoty
						self.game.missFlag = -1
					btt.SetBitmapLabel(self.nullBmp)
				else: # pole není označeno
					self.game.flagged += 1 # zvýšení počtu označených
					if self.game.fields[id].mine != False:
						self.game.NotifyNeighbours(id,'cFlagged','+') # oznámení sousedům
					if self.game.fields[id].mine == False: # neobsahuje minu - chybné označení
						self.game.mismatches += 1
					self.counter.SetLabel('Označeno: '+str(self.game.flagged)+'/'+str(self.game.mines)) # změna štítku
					self.game.fields[id].flagged = True # změna paramteru pole
					btt.SetBitmapLabel(self.danger)
					self.game.flagPos.Insert(id) # přidání do spojového seznamu
					if (self.game.mines == self.game.flagged) and (self.game.mismatches == 0): # jsou označeny všechny miny a správně - výhra
						self.timer.Stop() # zastavení časovače
						self.end = True # příznak konce
						self.moveList = list() # nutné uložení tahu pro případný krok zpět
						for i in range(0,self.game.count): # projde všechny pole a odkryje je
							if (self.game.fields[i].clicked != True) and (self.game.fields[i].flagged != True):
								self.Move(i,False)
						self.game.moves.Insert(self.moveList) # vložení tahu do spojového seznamu
						self.Save() # uložení výsledku
						
		node = self.game.possibleMoves.head
		while(node != None): # update spojového seznamu, vymazání polí, které nejsou dále použitelné
			if self.game.fields[node.fieldId].neighbours - self.game.fields[node.fieldId].cClicked -self.game.fields[node.fieldId].cFlagged <= 0:
				if node != None:
					self.game.possibleMoves.Remove(node)
					node = node.next
			else:
				node = node.next
				
	def Move(self,id,explode):
		
		# Metoda provádějící odkrytí daného pole a akce s tím spojené
		
		self.moveList.append(id) # přidání pole do seznamu daného tahu
		btt = self.FindWindowById(id)
		field = self.game.fields[id]
		if field.flagged:
			btt.SetValue(False)
		if (field.flagged == False) or (explode == False): # pole není označeno nebo je metoda volaná při rozkrývání více polí - ignoruje označená pole
			if field.flagged: # pole je označeno
				self.game.flagged -= 1 # změna počtu označených polí
				self.game.NotifyNeighbours(id,'cFlagged','-') # zpráva sousedům
				self.game.flagPos.RemoveBy(id) # odstranění ze spojového seznamu
				self.game.mismatches -= 1 # změna počtu chybných označení
				self.counter.SetLabel('Označeno: '+str(self.game.flagged)+'/'+str(self.game.mines))
			btt.SetBitmapLabel(self.nullBmp)
			if field.mine == False: # na poli není mina - zobrazení příslušného počtu okolních min
				if field.cMines == 1:
					btt.SetBitmapLabel(self.one)
				elif field.cMines == 2:
					btt.SetBitmapLabel(self.two)
				elif field.cMines == 3:
					btt.SetBitmapLabel(self.three)
				elif field.cMines == 4:
					btt.SetBitmapLabel(self.four)
				elif field.cMines == 5:
					btt.SetBitmapLabel(self.five)
				elif field.cMines == 6:
					btt.SetBitmapLabel(self.six)
				elif field.cMines == 7:
					btt.SetBitmapLabel(self.seven)
				elif field.cMines == 8:
					btt.SetBitmapLabel(self.eight)
				else: # nesousedím s minou, je-li metoda vyvolána klikem myši, nebo tahem (explode == True) provede se rozkrytí okolí
					if explode == True:
						self.ShowPrev(id)
						self.ShowNext(id)
			else: # obsahuje minu
				if explode == False: # pouze zobrazení min
					btt.SetBitmapLabel(self.mine)
					if not field.clicked:
						self.game.NotifyNeighbours(id,'cClicked','+') # zpráva sousedům
					field.clicked = True # změna parametrů pole
				else: # šlápnutí na minu
					if not field.clicked:
						self.game.NotifyNeighbours(id,'cClicked','+') # zpráva sousedům
					field.clicked = True # změna parametrů pole
					self.end = True # konec hry
					self.ShowMines() # zobrazí miny
					self.timer.Stop() # zastavení časovače
					btt.SetBitmapLabel(self.expl)
			btt.SetValue(True)
			if field.mine == False: # na poli není mina
				self.game.possibleMoves.Insert(id) # vložení pole mezi možné tahy
				if not field.clicked:
					self.game.NotifyNeighbours(id,'cClicked','+') # oznámení sousedům
				field.clicked = True # změna parametrů pole
			self.game.movesCount += 1 # změna počtu tahů
	
	def Save(self):
		
		# Metoda volaná pro případné uložení výsledků
		# Zobrazím dialogové okno, případně uloží výsledky do souboru
		
		cg = 'Gratulace, vyřešeno za: '
		cg += str(self.timeLbl.GetLabel())
		cg += '\n\n Uložit výsledek?'
		dial = wx.MessageDialog(None,cg, 'Info',wx.ICON_INFORMATION | wx.YES_NO) 
		result = dial.ShowModal() # zobrazení dialogu a načtení odpovědi
		if result == wx.ID_YES: # výsledky se mají uložit
			resFile = open('./results/results_'+str(self.game.mines),'w+') # otevření souboru pro daný rozměr
			self.game.highscores.scores.append(self.time) # připojení nového výsledku
			self.game.highscores.scores.sort() # seřazení výsledků
			if len(self.game.highscores.scores) > 10: # jen 10 nejlepších výsledků
				self.game.highscores.scores.remove(self.game.highscores.scores[10])
			pickle.dump(self.game.highscores,resFile) # uložení objektu pomocí modulu pickle
	
	def Reset(self, e):
		
		# Reset hracího plánu
		
		dial = wx.MessageDialog(None,'Zrušit stávající hru?', 'Info',wx.ICON_QUESTION | wx.YES_NO)
		result = dial.ShowModal() # dotaz na potvrzení akce
		if result == wx.ID_YES: 
			self.end = False #  zruší příznak konce
			self.toolbar.EnableTool(15,False) # znepřístupní krok zpět
			self.time = 0 # vynulování a zastavení časomíry
			self.timer.Stop()
			self.timeLbl.SetLabel('00:00')
			self.game = Game(self.game.width,self.game.height,self.game.count,self.game.mines) # nová instance třídy hra 
			for i in range(0,self.game.count): # uvedení tlačítek do původního stavu
				self.FindWindowById(i).SetValue(False)
				self.FindWindowById(i).SetBitmapLabel(self.nullBmp)
				
	def New(self, e):
		
		# Metoda volaná při vytváření nové hry
		
		dial = wx.MessageDialog(None,'Zrušit stávající hru?', 'Info',wx.ICON_QUESTION | wx.YES_NO)
		result = dial.ShowModal() # potvrzení akce
		if result == wx.ID_YES:
			self.Close() # zrušení své instance a otevření okna s volbou parametrů nové hry
			Choice(None)
		
		
# Začátek programu
# Inicializace okna s volbou parametrů hry a spuštění GUI

app = wx.App()
Choice(None)
app.MainLoop()
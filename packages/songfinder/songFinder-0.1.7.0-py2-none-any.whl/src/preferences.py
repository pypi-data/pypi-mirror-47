# -*- coding: utf-8 -*-


import os
from Tkinter import *
import ttk
import shutil
import filecmp
import src.messages as tkMessageBox
import src.messages as tkFileDialog

import globalvar as globalvar
import src.classPaths as classPaths

class ParamGen(object, Frame):
	def __init__(self, fenetre, papa, **kwargs):
		Frame.__init__(self, fenetre, **kwargs)
		self.grid()
		self.fenetre = fenetre
		self.papa = papa
		self.paths = classPaths.Paths()
		self.settingName = 'SettingsGen'

		self.screen_w = fenetre.winfo_screenwidth()
		self.screen_h = fenetre.winfo_screenheight()

		self.reset_button = Button(self, text='Reset', command=self.reset)
		self.ext_image = globalvar.genSettings.get('Extentions', 'image')
		self.FILETYPES_image = [(ext[1:].upper(), ext) for ext in self.ext_image] + [("All files", "*.*")]

		self.mot_data = Label(self, text = 'Base de données local: ')
		self.data_button = Button(self, text='Sauver/parcourir', command=self.change_rep)
		self.data_str = Entry(self, width=50)

		self.autoload = IntVar()
		self.autoload_button = Checkbutton(self, text="Charger la dernière liste au démarrage.", \
											variable=self.autoload, command=self.save_autoload)
		self.sync = IntVar()
		self.sync_button = Checkbutton(self, text="Synchroniser la base de données.", \
											variable=self.sync, command=self.save_sync)

		self.autoload_button.grid(row=0, column=0, columnspan=5, sticky='w' )
		self.sync_button.grid(row=1, column=0, columnspan=5, sticky='w' )

		self.mot_data.grid(row=2, column=0, columnspan=2, sticky='w' )
		self.data_str.grid(row=2, column=2, columnspan=7, sticky='w' )
		self.data_button.grid(row=2, column=9, columnspan=1, sticky='w' )
		self.reset_button.grid(row=3, column=0, columnspan=2)

		self.maj()

	def maj(self):
		if globalvar.genSettings.get('Parameters', 'autoload') == 'oui':
			self.autoload_button.select()
		self.data_str.delete(0, END)
		self.data_str.insert(0, self.paths.root)

	def change_rep(self):
		chemin = self.data_str.get()
		if chemin == self.paths.root:
			self.paths.save( tkFileDialog.askdirectory(parent = self.fenetre) )
		else:
			self.paths.save(chemin)
		self.maj()
		self.papa.updateData()

	def save_autoload(self):
		if self.autoload.get():
			str_valeur = 'oui'
		else:
			str_valeur = 'non'
		globalvar.genSettings.set('Parameters', 'autoload', str_valeur)
		self.maj()

	def save_sync(self):
		if self.sync.get():
			str_valeur = 'oui'
		else:
			str_valeur = 'non'
		globalvar.genSettings.set('Parameters', 'sync', str_valeur)
		self.paths = classPaths.Paths()
		self.paths.sync(self.papa)
		self.maj()

	def reset(self):
		if tkMessageBox.askyesno(u'Defaut', 'Etes vous sur de remettre les paramètres par defaut ?'):
			globalvar.sett.create()
			self.maj()

class ParamPres(object, Frame):
	def __init__(self, fenetre, papa, **kwargs):
		Frame.__init__(self, fenetre, **kwargs)
		self.grid()
		self.fenetre = fenetre
		self.papa = papa
		self.paths = classPaths.Paths()
		self.petit_mot_profil = Label(self, text = 'Profil: ')
		self.petit_mot_profil.grid(row=0, column=0, columnspan=3, sticky='w')

		self.settingName = 'SettingsPres'

		self.screen_w = fenetre.winfo_screenwidth()
		self.screen_h = fenetre.winfo_screenheight()

		self.fenetre_profil = None
		self.profil = ''
		self.liste_profil = []

		self.profil_selection = StringVar()
		self.combobox_profil = ttk.Combobox(self, textvariable = self.profil_selection, \
												values = self.liste_profil, state = 'readonly')
		self.combobox_profil.grid(row=0, column=3, columnspan=5)
		self.get_profil_liste()
		self.start_profil()

		self.etype = 'song'

		self.petit_mot_type = Label(self, text = 'Paramètres pour le type: ')
		self.petit_mot_type.grid(row=1, column=0, columnspan=3, sticky='w')

		self.liste_etype = globalvar.genSettings.get('Syntax', 'element_type')

		self.etype_selection	= StringVar()
		self.combobox_etype	= ttk.Combobox(self, textvariable = self.etype_selection, \
						values = self.liste_etype, state = 'readonly')
		self.combobox_etype.grid(row=1, column=3, columnspan=5)
		self.combobox_etype.set('song')

		self.ext_image = globalvar.genSettings.get('Extentions', 'image')
		self.FILETYPES_image = [(ext[1:].upper(), ext) for ext in self.ext_image] + [("All files", "*.*")]

		self.mot_background = Label(self, text = 'Arrière plan: ')
		self.background_button = Button(self, text='Sauver/parcourir', command=self.change_background)
		self.background_str = Entry(self, width=60)

		self.add_profil_button = Button(self, text='Sauvegarder le profil', command=self.fenetre_creation_profil)

		self.dictParam = {"Numéroter les diapositives.":"Numerote_diapo",\
							"Afficher le titre/commentaire.":"Print_title",\
							"Enlever les majuscules aux pronoms.":"Clean_majuscule",\
							"Mettre des majuscules en début de lignes.":"Majuscule",\
							'Verifier les "bis".':"Check_bis",\
							"Passer à la ligne en fonction de la ponctuation.":"Saut_ligne",\
							"Passer à la lignes même sans ponctuation.":"Saut_ligne_force",\
							"Vérifier les espaces autour des ponctuations.":"Ponctuation",\
							"Numeroter les éléments ne contenant qu'une seul diapo.":"oneslide",\
							}

		self.var_justification = IntVar()
		self.justification_gauche = Radiobutton(self, text="Justifier à gauche.", \
												variable=self.var_justification, value=0, command=self.save)
		self.justification_centre = Radiobutton(self, text="Justifier au centre.", \
												variable=self.var_justification, value=1, command=self.save)
		self.justification_droite = Radiobutton(self, text="Justifier à droite.", \
												variable=self.var_justification, value=2, command=self.save)
		self.liste_justification = [self.justification_gauche, self.justification_centre, self.justification_droite]

		self.liste_mep = ['left', 'center', 'right']

		self.var_size = StringVar()
		self.mot_size = Label(self, text = 'Taille police: ')
		self.size_entry = Entry(self, textvariable=self.var_size, width=5)
		self.var_max_car = StringVar()
		self.mot_max_car = Label(self, text = 'Taille des lignes: ')
		self.max_car_entry = Entry(self, textvariable=self.var_max_car, width=5)
		self.save_sizes_button = Button(self, text='Sauver', command=self.save_sizes)

		self.combobox_etype.bind("<<ComboboxSelected>>", self.select_etype)
		self.combobox_profil.bind("<<ComboboxSelected>>", self.select_profil)

		for i, just in enumerate(self.liste_justification):
			just.bind("<ButtonRelease-1>", self.save)

		nb_boutton = len(self.dictParam)
		nb_justification = len(self.liste_justification)

		self.mot_background.grid(row=nb_boutton+5+nb_justification, column=0, columnspan=2, sticky='w' )
		self.background_str.grid(row=nb_boutton+5+nb_justification, column=2, columnspan=7, sticky='w' )
		self.background_button.grid(row=nb_boutton+5+nb_justification, column=9, columnspan=1, sticky='w' )

		self.add_profil_button.grid(row=nb_boutton+12+nb_justification, column=0, columnspan=10, sticky='ew' )

		column_width = 5
		nb_row = (nb_boutton+1)//2
		self.dictValeurs = dict()
		self.dictButton = dict()
		for i, (param, item) in enumerate(self.dictParam.items()):
			var = IntVar()
			button = Checkbutton(self, text=param, variable=var, command=self.save)
			self.dictValeurs[param] = var
			self.dictButton[item] = button
			column_num = i//nb_row * (column_width + 1)
			button.grid(row=i%nb_row+3, column=column_num, columnspan=column_width, sticky='w' )

		for i, just in enumerate(self.liste_justification):
			just.grid(row=nb_row+3+i, column=0, columnspan=5, sticky='w' )

		self.mot_size.grid(row=nb_boutton+8+nb_justification, column=0, columnspan=2, sticky='w' )
		self.size_entry.grid(row=nb_boutton+8+nb_justification, column=2, columnspan=1, sticky='w' )
		self.mot_max_car.grid(row=nb_boutton+8+nb_justification+1, column=0, columnspan=2, sticky='w' )
		self.max_car_entry.grid(row=nb_boutton+8+nb_justification+1, column=2, columnspan=1, sticky='w' )
		self.save_sizes_button.grid(row=nb_boutton+8+nb_justification, column=3, columnspan=1, rowspan=2, sticky='w' )

		self.separator0 = ttk.Separator(self, orient="horizontal")
		self.separator1 = ttk.Separator(self, orient="horizontal")
		self.separator2 = ttk.Separator(self, orient="horizontal")
		self.separator3 = ttk.Separator(self, orient="vertical")
		self.separator5 = ttk.Separator(self, orient="horizontal")

		self.separator0.grid(row=2, column=0, columnspan=10, sticky='ew' )
		self.separator1.grid(row=nb_boutton+4+nb_justification, column=0, columnspan=10, sticky='ew' )
		self.separator2.grid(row=nb_boutton+7+nb_justification, column=0, columnspan=10, sticky='ew' )
		self.separator3.grid(row=2, column=5, rowspan=nb_boutton+4+nb_justification-2, sticky='ns' )
		self.separator5.grid(row=nb_boutton+10+nb_justification, column=0, columnspan=10, sticky='ew' )

		self.maj()

	def maj(self):
		for param in self.dictParam.values():
			if globalvar.presSettings.get(self.etype, param) == 'oui':
				self.dictButton[param].select()
			else:
				self.dictButton[param].deselect()
		if self.etype == 'song':
			for button in self.dictButton.values():
				button.config(state=NORMAL)
			for i, just in enumerate(self.liste_justification):
				just.config(state=NORMAL)

		elif self.etype == 'verse':
			for button in self.dictButton.values():
				button.config(state=NORMAL)
			for i, just in enumerate(self.liste_justification):
				just.config(state=NORMAL)
			for param in ["Check_bis", "Clean_majuscule"]:
				self.dictButton[param].deselect()
				self.dictButton[param].config(state=DISABLED)

		elif self.etype == 'media':
			for button in self.dictButton.values():
				button.deselect()
				button.config(state=DISABLED)
			for param in ["Print_title", "Ponctuation"]:
				self.dictButton[param].config(state=NORMAL)
			for i, just in enumerate(self.liste_justification):
				just.config(state=NORMAL)

		elif self.etype == 'image':
			for button in self.dictButton.values():
				button.deselect()
				button.config(state=DISABLED)
			for param in ["Print_title", "Ponctuation"]:
				self.dictButton[param].config(state=NORMAL)
			for i, just in enumerate(self.liste_justification):
				just.config(state=NORMAL)

		elif self.etype == 'empty':
			for button in self.dictButton.values():
				button.deselect()
				button.config(state=DISABLED)
			for i, just in enumerate(self.liste_justification):
				just.config(state=DISABLED)

		elif self.etype == 'preach':
			for button in self.dictButton.values():
				button.config(state=NORMAL)
			for param in ["Check_bis", "Clean_majuscule", "oneslide"]:
				self.dictButton[param].deselect()
				self.dictButton[param].config(state=DISABLED)

		param = globalvar.presSettings.get(self.etype, 'Justification')
		self.var_justification.set(self.liste_mep.index(param))

		self.background = globalvar.presSettings.get(self.etype, 'Background')
		self.background_str.delete(0, END)
		self.background_str.insert(0, self.background)

		self.var_size.set(globalvar.presSettings.get('Presentation_Parameters', 'size'))
		self.var_max_car.set(globalvar.presSettings.get('Presentation_Parameters', 'size_line'))

	def save(self, event=0, *args):
		for param, valeur in self.dictValeurs.items():
			if valeur.get():
				str_valeur = 'oui'
			else:
				str_valeur = 'non'
			globalvar.presSettings.set(self.etype, self.dictParam[param], str_valeur)

		num = self.liste_mep[self.var_justification.get()]
		globalvar.presSettings.set(self.etype, 'Justification', str(num))

	def save_sizes(self):
		size = self.var_size.get()
		max_car = self.var_max_car.get()
		if settings.is_number(size):
			globalvar.presSettings.set('Presentation_Parameters', 'size', str(int(round(float(size)))))
		if settings.is_number(max_car):
			globalvar.presSettings.set('Presentation_Parameters', 'size_line', str(int(round(float(max_car)))))

		self.var_size.set(globalvar.presSettings.get('Presentation_Parameters', 'size'))
		self.var_max_car.set(globalvar.presSettings.get('Presentation_Parameters', 'size_line'))

	def change_background(self):
		chemin = self.background_str.get()
		if chemin == self.background:
			chemin = tkFileDialog.askopenfilename(filetypes=self.FILETYPES_image, parent = self.fenetre)
			if chemin and os.path.isfile(chemin):
				self.background = chemin
			elif chemin:
				tkMessageBox.showerror(u'Erreur', u'Le fichier est introuvable', parent = self.fenetre)
		else:
			if chemin and os.path.isfile(chemin):
				self.background = chemin
			elif chemin:
				tkMessageBox.showerror(u'Erreur', u'Le fichier est introuvable', parent = self.fenetre)
		globalvar.presSettings.set(self.etype, 'Background', self.background)
		self.maj()

	def select_etype(self, event):
		if self.combobox_etype.get():
			self.etype = self.combobox_etype.get()
			self.maj()

	def select_profil(self, event):
		if self.combobox_profil.get():
			self.profil = self.combobox_profil.get()
			shutil.copy( os.path.join(globalvar.settingsPath, self.settingName + '_' + self.profil) , os.path.join(globalvar.settingsPath, self.settingName) )
			globalvar.sett.read()
			self.maj()

	def start_profil(self):
		for filename in os.listdir(globalvar.settingsPath):
			if filename.find(self.settingName + '_') != -1 and \
				filecmp.cmp( os.path.join(globalvar.settingsPath, filename) , os.path.join(globalvar.settingsPath, self.settingName) ):
				self.profil = filename[filename.find('_')+1:]
				self.combobox_profil.set(self.profil)

	def fenetre_creation_profil(self):
		if not self.fenetre_profil	:
			self.fenetre_profil = Toplevel(self)
			self.fenetre_profil.wm_attributes("-topmost", 1)
			self.fenetre_profil.title("Nouveau profil")
			self.fenetre_profil.geometry("%dx%d+%d+%d"%(170, 80, self.screen_w//2-100, self.screen_h//4-25))

			self.text_set=Label(self.fenetre_profil, text="Nom du nouveau profil")
			self.nom_profil = Entry(self.fenetre_profil, width=20)
			self.bouton_set = Button(self.fenetre_profil, text='Créer', command=self.cree_profil)

			self.text_set.grid(row=0, column=0)
			self.nom_profil.grid(row=1, column=0)
			self.bouton_set.grid(row=2, column=0)

			self.fenetre_profil.update()
			self.nom_profil.focus_set()

	def cree_profil(self):
		if self.nom_profil.get():
			self.profil = self.nom_profil.get()
			profil = os.path.join(globalvar.settingsPath, self.settingName + '_' + self.profil)
			if not os.path.isfile(profil) or \
								tkMessageBox.askyesno(u'Conflit', 'Le fichier %s existe déjà, voulez-vous le remplacer ?'%profil, \
								parent = self.fenetre_profil):
				globalvar.sett.write()
				shutil.copy( os.path.join(globalvar.settingsPath, self.settingName), profil)
				self.fenetre_profil.destroy()
				self.fenetre_profil = None
				if os.path.isfile(profil):
					tkMessageBox.showinfo(u'Confirmation', u'Le fichier %s a été écrit'%profil, parent = self.fenetre)
					self.combobox_profil.set(self.profil)
			else:
				tkMessageBox.showerror(u'Erreur', u'Le fichier %s n\'a pas été crée'%profil, parent = self.fenetre)
		self.get_profil_liste()

	def get_profil_liste(self):
		# Creation de la liste de profil
		self.liste_profil = []
		for root, dirs, files in os.walk(globalvar.settingsPath):
			for fichier in files:
				if fichier.find('Settings_') != -1:
					self.liste_profil.append(fichier[9:])
			break
		self.combobox_profil['values'] = self.liste_profil

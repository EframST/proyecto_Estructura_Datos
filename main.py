#------PROGRAMA PARA SORTEAR GRUPOS DE COMPETICIONES UEFA APLICANDO COLAS--------
#Aplicacion de colas en los métodos bombos_champions_league, bombos_europa_league, bombos_conference_league, sortear_Grupos, mostrar_grupos
#Aplicación de colas en lineas #626-#1055

from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk #Para evitar errores intalar paquete Pillow desde configuración
from cola import Cola
import random
import pygame #Para evitar errores intalar paquete pygame desde configuración
import sqlite3

class main():
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.geometry("1205x720")
        self.wind.resizable(False,False)
        self.wind.title('Equipos Registrados')
        self.wind.iconphoto(False, ImageTk.PhotoImage(file='logoUEFA.png'))
        pygame.init()
        pygame.mixer.music.load('EuropaLeagueAmsterdam.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(1000)

        self.fondo = Image.open("fondoPrincipal.jpg")
        self.fondo=self.fondo.resize((1280,720), Image.ANTIALIAS)
        self.imagen=ImageTk.PhotoImage(self.fondo)
        self.imagelabel = Label(self.wind, image=self.imagen).place(x=-2,y=0)

        # Crear cuadro de elementos
        frame = LabelFrame(self.wind, text='Registre el Equipo')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Nombre Input
        Label(frame, text='Nombre:').grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Liga Input
        Label(frame, text='Liga:').grid(row=2, column=0)
        self.liga = Entry(frame)
        self.liga.grid(row=2, column=1)

        # Posicion Temporada  Anterior Input
        Label(frame, text='Posicion Temporada Anterior:').grid(row=3, column=0)
        self.posicion = Entry(frame)
        self.posicion.grid(row=3, column=1)

        # Valor Equipo en Dolares Input
        Label(frame, text='Valor Equipo:').grid(row=4, column=0)
        self.valor_Equipo = Entry(frame)
        self.valor_Equipo.grid(row=4, column=1)

        # Ranking UEFA Input
        Label(frame, text='Ranking UEFA:').grid(row=5, column=0)
        self.ranking_UEFA = Entry(frame)
        self.ranking_UEFA.grid(row=5, column=1)

        # Competición UEFA Input
        Label(frame, text='Competición UEFA:').grid(row=6, column=0)
        self.competicion_UEFA=StringVar()
        self.competicion_UEFA.set('UEFA Champions League')
        self.competicion = OptionMenu(frame,self.competicion_UEFA,'UEFA Champions League', 'UEFA Europa League', 'UEFA Conference League', 'UEFA Champions League (Campeón vigente)', 'UEFA Europa League (Campeón vigente)', 'UEFA Conference League (Campeón vigente)')
        self.competicion.grid(row=6, column=1)

        # Boton de Guardado
        ttk.Button(frame, text='Guardar', command=self.add_equipo).grid(row=7, columnspan=2, sticky=W + E)

        # OutPut Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabla
        self.tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3', '#4'))
        self.tree.grid(row=8, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Liga', anchor=CENTER)
        self.tree.heading('#2', text='Posicion', anchor=CENTER)
        self.tree.heading('#3', text='Valor', anchor=CENTER)
        self.tree.heading('#4', text='Ranking UEFA', anchor=CENTER)
        self.tree.heading('#5', text='Competición UEFA', anchor=CENTER)
        # Botones
        ttk.Button(frame, text='Guardar', command=self.add_equipo).grid(row=7, columnspan=2, sticky=W + E)
        ttk.Button(text='Borrar').grid(row=9, column=0, sticky=W + E)
        ttk.Button(text='Actualizar').grid(row=9, column=1, sticky=W + E)
        self.logoucl = Image.open('botonChampions.png')
        self.logoucl = self.logoucl.resize((128,128), Image.ANTIALIAS)
        self.logoucl = ImageTk.PhotoImage(self.logoucl)
        self.logouel = Image.open('botonEuropa.png')
        self.logouel = self.logouel.resize((128, 128), Image.ANTIALIAS)
        self.logouel = ImageTk.PhotoImage(self.logouel)
        self.logoucf = Image.open('botonConference.png')
        self.logoucf = self.logoucf.resize((128, 128), Image.ANTIALIAS)
        self.logoucf = ImageTk.PhotoImage(self.logoucf)
        frame.grid(row=0, column=0, columnspan=5, pady=20)
        Button(image=self.logoucl,command=self.champions_league).place(x=333,y=550)
        Button(image=self.logouel,command=self.europa_league).place(x=533,y=550)
        Button(image=self.logoucf,command=self.conference_league).place(x=733,y=550)

        #Actualizando datos
        self.get_equipos()
        #Botones
        ttk.Button(frame, text='Guardar', command=self.add_equipo).grid(row=7, columnspan=2, sticky=W + E)
        ttk.Button(text = 'Borrar',command = self.delete_equipo).grid(row = 9, column = 0,sticky = W+E)
        ttk.Button(text = 'Actualizar',command = self.edit_equipo).grid(row = 9, column = 1,sticky = W+E)


    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_equipos(self):
        # Limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consultando los datos
        query = 'SELECT * FROM equipo ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        # Rellenando los datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
    #Validar Datos
    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.liga.get()) != 0 and len(self.posicion.get()) != 0 and len(
            self.valor_Equipo.get()) != 0 and len(self.ranking_UEFA.get()) != 0 and len(self.competicion_UEFA.get()) != 0
    #Añadir Equipos
    def add_equipo(self):
        # Añadir
        if self.validacion():
            query = 'INSERT INTO equipo VALUES(?,?,?,?,?,?)'
            parameters = (
            self.nombre.get(), self.liga.get(), self.posicion.get(), self.valor_Equipo.get(), self.ranking_UEFA.get(), self.competicion_UEFA.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Equipo {} fue Añadido Correctamente'.format(self.nombre.get())
            self.nombre.delete(0,END)
            self.liga.delete(0,END)
            self.posicion.delete(0,END)
            self.valor_Equipo.delete(0,END)
            self.ranking_UEFA.delete(0,END)
            self.competicion_UEFA.set('UEFA Champions League')
        else:
            self.message['text'] = 'Los datos son requeridos'.format(self.get_equipos())
        self.get_equipos()
    #Borrando Equipos
    def delete_equipo(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Escoge un Equipo'
            return
        self.message['text']=''
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM equipo WHERE nombre = ?'
        self.run_query(query,(nombre,))
        self.message['text'] = 'La opcion {} fue eliminada correctamente '. format(nombre)
        self.get_equipos()
    #Editando Equipos
    def edit_equipo(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Escoge un Equipo'
            return
        nombre=self.tree.item(self.tree.selection())['text']
        old_liga = self.tree.item(self.tree.selection())['values'][0]
        old_posicion=self.tree.item(self.tree.selection())['values'][1]
        old_valor_Equipo=self.tree.item(self.tree.selection())['values'][2]
        old_ranking_UEFA=self.tree.item(self.tree.selection())['values'][3]
        old_competicion_UEFA = self.tree.item(self.tree.selection())['values'][4]
        self.edit_wind = Toplevel()
        self.edit_wind.title=' Editar Equipo'
        self.edit_wind.iconphoto(False, ImageTk.PhotoImage(file='logoUEFA.png'))
        self.edit_wind.resizable(False, False)

        #Old name
        Label(self.edit_wind, text = 'Nombre Antiguo:').grid(row = 0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind,value=nombre), state = 'readonly').grid(row=0,column= 2)
        #New name
        Label(self.edit_wind, text='Nombre Nuevo:').grid(row=0, column=7)
        new_nombre=Entry(self.edit_wind)
        new_nombre.insert(0, nombre)
        new_nombre.grid(row =0 ,column=8)

        #Old liga
        Label(self.edit_wind, text = 'Liga Antiguo:').grid(row = 1, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_liga), state='readonly').grid(row=1,column=2)
        #New liga
        Label(self.edit_wind, text='Liga Nueva:').grid(row=1, column=7)
        new_liga=Entry(self.edit_wind)
        new_liga.insert(0, old_liga)
        new_liga.grid(row =1 ,column=8)

        #Old posicion
        Label(self.edit_wind, text = 'Posicion Antigua:').grid(row = 2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_posicion), state='readonly').grid(row=2,column=2)
        #New posicion
        Label(self.edit_wind, text='Nueva Posicion:').grid(row=2, column=7)
        new_posicion=Entry(self.edit_wind)
        new_posicion.insert(0, old_posicion)
        new_posicion.grid(row =2 ,column=8)

        #Old valor_Equipo
        Label(self.edit_wind, text='Valor Antiguo:').grid(row=3, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_valor_Equipo), state='readonly').grid(row=3,column=2)
        #New valor_Equipo
        Label(self.edit_wind, text='Nuevo Valor:').grid(row=3, column=7)
        new_valor_Equipo=Entry(self.edit_wind)
        new_valor_Equipo.insert(0, old_valor_Equipo)
        new_valor_Equipo.grid(row =3 ,column=8)

        #Old ranking_UEFA
        Label(self.edit_wind, text='Ranking Antiguo:').grid(row=5, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_ranking_UEFA), state='readonly').grid(row=5,column=2)
        # New ranking_UEFA
        Label(self.edit_wind, text='Nuevo Ranking:').grid(row=5, column=7)
        new_ranking_UEFA = Entry(self.edit_wind)
        new_ranking_UEFA.insert(0, old_ranking_UEFA)
        new_ranking_UEFA.grid(row=5, column=8)

        #Old competicion_UEFA
        Label(self.edit_wind, text='Competicion Antigua:').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_competicion_UEFA), state='readonly').grid(row=6,column=2)
        #New competicion_UEFA
        Label(self.edit_wind, text='Competicion Nueva:').grid(row=6, column=7)
        new_competicion_UEFA=StringVar()
        new_competicion_UEFA.set(old_competicion_UEFA)
        new_competicion=OptionMenu(self.edit_wind,new_competicion_UEFA,*['UEFA Champions League', 'UEFA Europa League', 'UEFA Conference League', 'UEFA Champions League (Campeón vigente)', 'UEFA Europa League (Campeón vigente)', 'UEFA Conference League (Campeón vigente)'])
        new_competicion.grid(row=6, column=8)

        Button(self.edit_wind, text='Actualizar',command = lambda: self.edit_records
         (new_nombre.get(), nombre,new_liga.get(),old_liga,new_posicion.get(),old_posicion,new_valor_Equipo.get(),
         old_valor_Equipo,new_ranking_UEFA.get(),old_ranking_UEFA,new_competicion_UEFA.get(),old_competicion_UEFA)).grid(row = 8,column=2, sticky = W+E)

    def edit_records(self,new_nombre,nombre, new_liga,old_liga,new_posicion,old_posicion,new_valor_Equipo,old_valor_Equipo,new_ranking_UEFA,old_ranking_UEFA,new_competicion_UEFA,old_competicion_UEFA):
        query = 'UPDATE equipo SET nombre =?, liga = ?, posicion = ?, valor_Equipo= ?,ranking_UEFA= ?,competicion_UEFA=? WHERE nombre = ? AND liga = ? AND posicion = ? AND valor_Equipo= ? AND ranking_UEFA= ? AND competicion_UEFA=? '
        parameters = (new_nombre,new_liga,new_posicion,new_valor_Equipo,new_ranking_UEFA,new_competicion_UEFA,nombre,old_liga,old_posicion,old_valor_Equipo,old_ranking_UEFA,old_competicion_UEFA)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Se ha actualizado Correctamente el equipo {}'.format(nombre)
        self.get_equipos()

    def champions_league(self):
        query = 'SELECT * FROM equipo'
        db_rows=self.run_query(query)
        numeroEquipos=0
        for row in db_rows:
            if row[5] in ['UEFA Champions League','UEFA Champions League (Campeón vigente)','UEFA Europa League (Campeón vigente)']:
                numeroEquipos=numeroEquipos+1
        if numeroEquipos!=32:
            self.message['text'] = 'Se requieren 32 equipos para sortear'
            return

        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        validacionCampeonUCL=0
        for row in db_rows:
            if row[5]=='UEFA Champions League (Campeón vigente)':
                validacionCampeonUCL=validacionCampeonUCL+1
        if validacionCampeonUCL!=1:
            self.message['text'] = 'Se requiere un equipo campeón vigente de la UEFA Champions League'
            return

        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        validacionCampeonUEL=0
        for row in db_rows:
            if row[5]=='UEFA Europa League (Campeón vigente)':
                validacionCampeonUEL=validacionCampeonUEL+1
        if validacionCampeonUEL!=1:
            self.message['text'] = 'Se requiere un equipo campeón vigente de la UEFA Europa League'
            return

        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        validacionBombo1=0
        for row in db_rows:
            if row[1]=='Premier League' and row[2]==1:
                validacionBombo1=validacionBombo1+1
            elif row[1]=='LaLiga' and row[2]==1:
                validacionBombo1=validacionBombo1+1
            elif row[1]=='Serie A' and row[2]==1:
                validacionBombo1=validacionBombo1+1
            elif row[1]=='Ligue 1' and row[2]==1:
                validacionBombo1=validacionBombo1+1
            elif row[1]=='Bundesliga' and row[2]==1:
                validacionBombo1=validacionBombo1+1
            elif row[1]=='Primeira Liga' and row[2]==1:
                validacionBombo1=validacionBombo1+1
        if validacionBombo1!=6:
            self.message['text'] = 'Se requiere un equipo en la posición 1 de las ligas: Premier League, LaLiga, Serie A, Ligue 1, Bundesliga, Primeira Liga'
            return

        self.winucl=Toplevel()
        self.winucl.title('UEFA Champions League')
        self.winucl.geometry("1280x720")
        self.winucl.resizable(False,False)
        self.winucl.iconphoto(False, ImageTk.PhotoImage(file='UCL/logoUCL.png'))
        pygame.mixer.music.load('HimnoChampions.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1000)
        self.fondochampions=ImageTk.PhotoImage(file='UCL/fondoChampions.jpg')
        Label(self.winucl, image=self.fondochampions).place(x=-2,y=0)

        self.LabelEquipos=ImageTk.PhotoImage(file='UCL/EquiposTitulo.png')
        Label(self.winucl, image=self.LabelEquipos).place(x=640,y=30,anchor='center')
        self.treeucl=ttk.Treeview(self.winucl,height=4,columns=('#0', '#1', '#2', '#3'))
        self.treeucl.place(x=150,y=60)
        self.treeucl.heading('#0', text='Nombre', anchor=CENTER)
        self.treeucl.heading('#1', text='Liga', anchor=CENTER)
        self.treeucl.heading('#2', text='Posicion', anchor=CENTER)
        self.treeucl.heading('#3', text='Valor', anchor=CENTER)
        self.treeucl.heading('#4', text='Ranking UEFA', anchor=CENTER)
        query = 'SELECT * FROM equipo ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[5] in ['UEFA Champions League','UEFA Champions League (Campeón vigente)','UEFA Europa League (Campeón vigente)']:
                self.treeucl.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

        self.Grupos=-1
        while self.Grupos==-1:
            self.Bombo1 = self.bombos_champions_league()[0]
            self.Bombo2 = self.bombos_champions_league()[1]
            self.Bombo3 = self.bombos_champions_league()[2]
            self.Bombo4 = self.bombos_champions_league()[3]
            self.Bombo1Array = self.Bombo1.convertirArray()
            self.Bombo2Array = self.Bombo2.convertirArray()
            self.Bombo3Array = self.Bombo3.convertirArray()
            self.Bombo4Array = self.Bombo4.convertirArray()

            self.Grupos = self.sortear_Grupos(self.Bombo1,self.Bombo2,self.Bombo3,self.Bombo4)

        self.Bombo1Titulo = ImageTk.PhotoImage(file='UCL/Bombo1Titulo.png')
        self.Bombo2Titulo = ImageTk.PhotoImage(file='UCL/Bombo2Titulo.png')
        self.Bombo3Titulo = ImageTk.PhotoImage(file='UCL/Bombo3Titulo.png')
        self.Bombo4Titulo = ImageTk.PhotoImage(file='UCL/Bombo4Titulo.png')

        self.LabelBombo1Tit = Label(self.winucl,image = self.Bombo1Titulo)
        self.LabelBombo1Tit.place(x=250, y=280, anchor='center')
        self.LabelBombo1 = Label(self.winucl,
                                 text=f'{self.Bombo1Array[0]}\n\n{self.Bombo1Array[1]}\n\n{self.Bombo1Array[2]}\n\n{self.Bombo1Array[3]}\n\n'
                                      f'{self.Bombo1Array[4]}\n\n{self.Bombo1Array[5]}\n\n{self.Bombo1Array[6]}\n\n{self.Bombo1Array[7]}')
        self.LabelBombo1.place(x=250, y=450, width=160, height=300, anchor='center')
        self.LabelBombo2Tit = Label(self.winucl, image=self.Bombo2Titulo)
        self.LabelBombo2Tit.place(x=510, y=280, anchor='center')
        self.LabelBombo2 = Label(self.winucl,
                                 text=f'{self.Bombo2Array[0]}\n\n{self.Bombo2Array[1]}\n\n{self.Bombo2Array[2]}\n\n{self.Bombo2Array[3]}\n\n'
                                      f'{self.Bombo2Array[4]}\n\n{self.Bombo2Array[5]}\n\n{self.Bombo2Array[6]}\n\n{self.Bombo2Array[7]}')
        self.LabelBombo2.place(x=510, y=450, width=160, height=300, anchor='center')
        self.LabelBombo3Tit = Label(self.winucl, image=self.Bombo3Titulo)
        self.LabelBombo3Tit.place(x=770, y=280, anchor='center')
        self.LabelBombo3 = Label(self.winucl,
                                 text=f'{self.Bombo3Array[0]}\n\n{self.Bombo3Array[1]}\n\n{self.Bombo3Array[2]}\n\n{self.Bombo3Array[3]}\n\n'
                                      f'{self.Bombo3Array[4]}\n\n{self.Bombo3Array[5]}\n\n{self.Bombo3Array[6]}\n\n{self.Bombo3Array[7]}')
        self.LabelBombo3.place(x=770, y=450, width=160, height=300, anchor='center')
        self.LabelBombo4Tit = Label(self.winucl, image=self.Bombo4Titulo)
        self.LabelBombo4Tit.place(x=1030, y=280, anchor='center')
        self.LabelBombo4 = Label(self.winucl,
                                 text=f'{self.Bombo4Array[0]}\n\n{self.Bombo4Array[1]}\n\n{self.Bombo4Array[2]}\n\n{self.Bombo4Array[3]}\n\n'
                                      f'{self.Bombo4Array[4]}\n\n{self.Bombo4Array[5]}\n\n{self.Bombo4Array[6]}\n\n{self.Bombo4Array[7]}')
        self.LabelBombo4.place(x=1030, y=450, width=160, height=300, anchor='center')

        self.GrupoATitulo = ImageTk.PhotoImage(file='UCL/GrupoATitulo.png')
        self.GrupoBTitulo = ImageTk.PhotoImage(file='UCL/GrupoBTitulo.png')
        self.GrupoCTitulo = ImageTk.PhotoImage(file='UCL/GrupoCTitulo.png')
        self.GrupoDTitulo = ImageTk.PhotoImage(file='UCL/GrupoDTitulo.png')
        self.GrupoETitulo = ImageTk.PhotoImage(file='UCL/GrupoETitulo.png')
        self.GrupoFTitulo = ImageTk.PhotoImage(file='UCL/GrupoFTitulo.png')
        self.GrupoGTitulo = ImageTk.PhotoImage(file='UCL/GrupoGTitulo.png')
        self.GrupoHTitulo = ImageTk.PhotoImage(file='UCL/GrupoHTitulo.png')

        self.BotonSortear = ImageTk.PhotoImage(file='UCL/BotonSortear.png')
        self.BotonVolver = ImageTk.PhotoImage(file='UCL/BotonVolver.png')
        Button(self.winucl, image=self.BotonSortear, command=lambda:[self.mostrar_grupos(self.Grupos,self.winucl), self.LabelBombo1.place(x=200,y=2000), self.LabelBombo2.place(x=200,y=2000),
                                                            self.LabelBombo3.place(x=200,y=2000), self.LabelBombo4.place(x=200,y=2000),
                                                            Label(self.winucl, image=self.GrupoATitulo).place(x=250, y=255, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoBTitulo).place(x=510, y=255, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoCTitulo).place(x=770, y=255, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoDTitulo).place(x=1030, y=255, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoETitulo).place(x=250, y=475, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoFTitulo).place(x=510, y=475, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoGTitulo).place(x=770, y=475, anchor='center'),
                                                            Label(self.winucl, image=self.GrupoHTitulo).place(x=1030, y=475, anchor='center')]).place(x=560, y=200, anchor='center')
        Button(self.winucl, image=self.BotonVolver, command=lambda:[self.winucl.destroy(),
                                                                    pygame.mixer.music.load('EuropaLeagueAmsterdam.mp3'),
                                                                    pygame.mixer.music.set_volume(0.3),
                                                                    pygame.mixer.music.play(1000),
                                                                    ]).place(x=720, y=200, anchor='center')

    def europa_league(self):
        query = 'SELECT * FROM equipo'
        db_rows=self.run_query(query)
        numeroEquipos=0
        for row in db_rows:
            if row[5] in ['UEFA Europa League','UEFA Conference League (Campeón vigente)']:
                numeroEquipos=numeroEquipos+1
        if numeroEquipos!=32:
            self.message['text'] = 'Se requieren 32 equipos para sortear'
            return

        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        validacionCampeonUCF=0
        for row in db_rows:
            if row[5]=='UEFA Conference League (Campeón vigente)':
                validacionCampeonUCF=validacionCampeonUCF+1
        if validacionCampeonUCF!=1:
            self.message['text'] = 'Se requiere un equipo campeón vigente de la UEFA Conference League'
            return

        self.winuel=Toplevel()
        self.winuel.title('UEFA Europa League')
        self.winuel.geometry("1280x720")
        self.winuel.resizable(False,False)
        self.winuel.iconphoto(False, ImageTk.PhotoImage(file='UEL/logoUEL.png'))
        pygame.mixer.music.load('HimnoEuropaConference.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1000)
        self.fondoeuropa=Image.open('UEL/fondoEuropa.jpg')
        self.fondoeuropa=self.fondoeuropa.resize((1280,720), Image.ANTIALIAS)
        self.fondoeuropa=ImageTk.PhotoImage(self.fondoeuropa)
        Label(self.winuel, image=self.fondoeuropa).place(x=-2,y=0)

        self.LabelEquipos=ImageTk.PhotoImage(file='UEL/EquiposTitulo.png')
        Label(self.winuel, image=self.LabelEquipos).place(x=640,y=30,anchor='center')
        self.treeuel=ttk.Treeview(self.winuel,height=4,columns=('#0', '#1', '#2', '#3'))
        self.treeuel.place(x=150,y=60)
        self.treeuel.heading('#0', text='Nombre', anchor=CENTER)
        self.treeuel.heading('#1', text='Liga', anchor=CENTER)
        self.treeuel.heading('#2', text='Posicion', anchor=CENTER)
        self.treeuel.heading('#3', text='Valor', anchor=CENTER)
        self.treeuel.heading('#4', text='Ranking UEFA', anchor=CENTER)
        query = 'SELECT * FROM equipo ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[5] in ['UEFA Europa League','UEFA Conference League (Campeón vigente)']:
                self.treeuel.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

        self.Grupos=-1
        while self.Grupos==-1:
            self.Bombo1 = self.bombos_europa_league()[0]
            self.Bombo2 = self.bombos_europa_league()[1]
            self.Bombo3 = self.bombos_europa_league()[2]
            self.Bombo4 = self.bombos_europa_league()[3]
            self.Bombo1Array = self.Bombo1.convertirArray()
            self.Bombo2Array = self.Bombo2.convertirArray()
            self.Bombo3Array = self.Bombo3.convertirArray()
            self.Bombo4Array = self.Bombo4.convertirArray()

            self.Grupos = self.sortear_Grupos(self.Bombo1,self.Bombo2,self.Bombo3,self.Bombo4)

        self.Bombo1Titulo = ImageTk.PhotoImage(file='UEL/Bombo1Titulo.png')
        self.Bombo2Titulo = ImageTk.PhotoImage(file='UEL/Bombo2Titulo.png')
        self.Bombo3Titulo = ImageTk.PhotoImage(file='UEL/Bombo3Titulo.png')
        self.Bombo4Titulo = ImageTk.PhotoImage(file='UEL/Bombo4Titulo.png')

        self.LabelBombo1Tit = Label(self.winuel,image = self.Bombo1Titulo)
        self.LabelBombo1Tit.place(x=250, y=280, anchor='center')
        self.LabelBombo1 = Label(self.winuel,
                                 text=f'{self.Bombo1Array[0]}\n\n{self.Bombo1Array[1]}\n\n{self.Bombo1Array[2]}\n\n{self.Bombo1Array[3]}\n\n'
                                      f'{self.Bombo1Array[4]}\n\n{self.Bombo1Array[5]}\n\n{self.Bombo1Array[6]}\n\n{self.Bombo1Array[7]}')
        self.LabelBombo1.place(x=250, y=450, width=160, height=300, anchor='center')
        self.LabelBombo2Tit = Label(self.winuel, image=self.Bombo2Titulo)
        self.LabelBombo2Tit.place(x=510, y=280, anchor='center')
        self.LabelBombo2 = Label(self.winuel,
                                 text=f'{self.Bombo2Array[0]}\n\n{self.Bombo2Array[1]}\n\n{self.Bombo2Array[2]}\n\n{self.Bombo2Array[3]}\n\n'
                                      f'{self.Bombo2Array[4]}\n\n{self.Bombo2Array[5]}\n\n{self.Bombo2Array[6]}\n\n{self.Bombo2Array[7]}')
        self.LabelBombo2.place(x=510, y=450, width=160, height=300, anchor='center')
        self.LabelBombo3Tit = Label(self.winuel, image=self.Bombo3Titulo)
        self.LabelBombo3Tit.place(x=770, y=280, anchor='center')
        self.LabelBombo3 = Label(self.winuel,
                                 text=f'{self.Bombo3Array[0]}\n\n{self.Bombo3Array[1]}\n\n{self.Bombo3Array[2]}\n\n{self.Bombo3Array[3]}\n\n'
                                      f'{self.Bombo3Array[4]}\n\n{self.Bombo3Array[5]}\n\n{self.Bombo3Array[6]}\n\n{self.Bombo3Array[7]}')
        self.LabelBombo3.place(x=770, y=450, width=160, height=300, anchor='center')
        self.LabelBombo4Tit = Label(self.winuel, image=self.Bombo4Titulo)
        self.LabelBombo4Tit.place(x=1030, y=280, anchor='center')
        self.LabelBombo4 = Label(self.winuel,
                                 text=f'{self.Bombo4Array[0]}\n\n{self.Bombo4Array[1]}\n\n{self.Bombo4Array[2]}\n\n{self.Bombo4Array[3]}\n\n'
                                      f'{self.Bombo4Array[4]}\n\n{self.Bombo4Array[5]}\n\n{self.Bombo4Array[6]}\n\n{self.Bombo4Array[7]}')
        self.LabelBombo4.place(x=1030, y=450, width=160, height=300, anchor='center')

        self.GrupoATitulo = ImageTk.PhotoImage(file='UEL/GrupoATitulo.png')
        self.GrupoBTitulo = ImageTk.PhotoImage(file='UEL/GrupoBTitulo.png')
        self.GrupoCTitulo = ImageTk.PhotoImage(file='UEL/GrupoCTitulo.png')
        self.GrupoDTitulo = ImageTk.PhotoImage(file='UEL/GrupoDTitulo.png')
        self.GrupoETitulo = ImageTk.PhotoImage(file='UEL/GrupoETitulo.png')
        self.GrupoFTitulo = ImageTk.PhotoImage(file='UEL/GrupoFTitulo.png')
        self.GrupoGTitulo = ImageTk.PhotoImage(file='UEL/GrupoGTitulo.png')
        self.GrupoHTitulo = ImageTk.PhotoImage(file='UEL/GrupoHTitulo.png')

        self.BotonSortear = ImageTk.PhotoImage(file='UEL/BotonSortear.png')
        self.BotonVolver = ImageTk.PhotoImage(file='UEL/BotonVolver.png')
        Button(self.winuel, image=self.BotonSortear, command=lambda:[self.mostrar_grupos(self.Grupos,self.winuel), self.LabelBombo1.place(x=200,y=2000), self.LabelBombo2.place(x=200,y=2000),
                                                            self.LabelBombo3.place(x=200,y=2000), self.LabelBombo4.place(x=200,y=2000),
                                                            Label(self.winuel, image=self.GrupoATitulo).place(x=250, y=255, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoBTitulo).place(x=510, y=255, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoCTitulo).place(x=770, y=255, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoDTitulo).place(x=1030, y=255, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoETitulo).place(x=250, y=475, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoFTitulo).place(x=510, y=475, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoGTitulo).place(x=770, y=475, anchor='center'),
                                                            Label(self.winuel, image=self.GrupoHTitulo).place(x=1030, y=475, anchor='center')]).place(x=560, y=200, anchor='center')
        Button(self.winuel, image=self.BotonVolver, command=lambda:[self.winuel.destroy(),
                                                                    pygame.mixer.music.load('EuropaLeagueAmsterdam.mp3'),
                                                                    pygame.mixer.music.set_volume(0.3),
                                                                    pygame.mixer.music.play(1000),
                                                                    ]).place(x=720, y=200, anchor='center')

    def conference_league(self):
        query = 'SELECT * FROM equipo'
        db_rows=self.run_query(query)
        numeroEquipos=0
        for row in db_rows:
            if row[5] == 'UEFA Conference League':
                numeroEquipos=numeroEquipos+1
        if numeroEquipos!=32:
            self.message['text'] = 'Se requieren 32 equipos para sortear'
            return

        self.winucf=Toplevel()
        self.winucf.title('UEFA Conference League')
        self.winucf.geometry("1280x720")
        self.winucf.resizable(False,False)
        self.winucf.iconphoto(False, ImageTk.PhotoImage(file='UCF/logoUCF.png'))
        pygame.mixer.music.load('HimnoEuropaConference.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1000)
        self.fondoconference=Image.open('UCF/fondoConference.jpg')
        self.fondoconference=self.fondoconference.resize((1280,720), Image.ANTIALIAS)
        self.fondoconference=ImageTk.PhotoImage(self.fondoconference)
        Label(self.winucf, image=self.fondoconference).place(x=-2,y=0)

        self.LabelEquipos=ImageTk.PhotoImage(file='UCF/EquiposTitulo.png')
        Label(self.winucf, image=self.LabelEquipos).place(x=640,y=30,anchor='center')
        self.treeucf=ttk.Treeview(self.winucf,height=4,columns=('#0', '#1', '#2', '#3'))
        self.treeucf.place(x=150,y=60)
        self.treeucf.heading('#0', text='Nombre', anchor=CENTER)
        self.treeucf.heading('#1', text='Liga', anchor=CENTER)
        self.treeucf.heading('#2', text='Posicion', anchor=CENTER)
        self.treeucf.heading('#3', text='Valor', anchor=CENTER)
        self.treeucf.heading('#4', text='Ranking UEFA', anchor=CENTER)
        query = 'SELECT * FROM equipo ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[5] == 'UEFA Conference League':
                self.treeucf.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

        self.Grupos=-1
        while self.Grupos==-1:
            self.Bombo1 = self.bombos_conference_league()[0]
            self.Bombo2 = self.bombos_conference_league()[1]
            self.Bombo3 = self.bombos_conference_league()[2]
            self.Bombo4 = self.bombos_conference_league()[3]
            self.Bombo1Array = self.Bombo1.convertirArray()
            self.Bombo2Array = self.Bombo2.convertirArray()
            self.Bombo3Array = self.Bombo3.convertirArray()
            self.Bombo4Array = self.Bombo4.convertirArray()

            self.Grupos = self.sortear_Grupos(self.Bombo1,self.Bombo2,self.Bombo3,self.Bombo4)

        self.Bombo1Titulo = ImageTk.PhotoImage(file='UCF/Bombo1Titulo.png')
        self.Bombo2Titulo = ImageTk.PhotoImage(file='UCF/Bombo2Titulo.png')
        self.Bombo3Titulo = ImageTk.PhotoImage(file='UCF/Bombo3Titulo.png')
        self.Bombo4Titulo = ImageTk.PhotoImage(file='UCF/Bombo4Titulo.png')

        self.LabelBombo1Tit = Label(self.winucf,image = self.Bombo1Titulo)
        self.LabelBombo1Tit.place(x=250, y=280, anchor='center')
        self.LabelBombo1 = Label(self.winucf,
                                 text=f'{self.Bombo1Array[0]}\n\n{self.Bombo1Array[1]}\n\n{self.Bombo1Array[2]}\n\n{self.Bombo1Array[3]}\n\n'
                                      f'{self.Bombo1Array[4]}\n\n{self.Bombo1Array[5]}\n\n{self.Bombo1Array[6]}\n\n{self.Bombo1Array[7]}')
        self.LabelBombo1.place(x=250, y=450, width=160, height=300, anchor='center')
        self.LabelBombo2Tit = Label(self.winucf, image=self.Bombo2Titulo)
        self.LabelBombo2Tit.place(x=510, y=280, anchor='center')
        self.LabelBombo2 = Label(self.winucf,
                                 text=f'{self.Bombo2Array[0]}\n\n{self.Bombo2Array[1]}\n\n{self.Bombo2Array[2]}\n\n{self.Bombo2Array[3]}\n\n'
                                      f'{self.Bombo2Array[4]}\n\n{self.Bombo2Array[5]}\n\n{self.Bombo2Array[6]}\n\n{self.Bombo2Array[7]}')
        self.LabelBombo2.place(x=510, y=450, width=160, height=300, anchor='center')
        self.LabelBombo3Tit = Label(self.winucf, image=self.Bombo3Titulo)
        self.LabelBombo3Tit.place(x=770, y=280, anchor='center')
        self.LabelBombo3 = Label(self.winucf,
                                 text=f'{self.Bombo3Array[0]}\n\n{self.Bombo3Array[1]}\n\n{self.Bombo3Array[2]}\n\n{self.Bombo3Array[3]}\n\n'
                                      f'{self.Bombo3Array[4]}\n\n{self.Bombo3Array[5]}\n\n{self.Bombo3Array[6]}\n\n{self.Bombo3Array[7]}')
        self.LabelBombo3.place(x=770, y=450, width=160, height=300, anchor='center')
        self.LabelBombo4Tit = Label(self.winucf, image=self.Bombo4Titulo)
        self.LabelBombo4Tit.place(x=1030, y=280, anchor='center')
        self.LabelBombo4 = Label(self.winucf,
                                 text=f'{self.Bombo4Array[0]}\n\n{self.Bombo4Array[1]}\n\n{self.Bombo4Array[2]}\n\n{self.Bombo4Array[3]}\n\n'
                                      f'{self.Bombo4Array[4]}\n\n{self.Bombo4Array[5]}\n\n{self.Bombo4Array[6]}\n\n{self.Bombo4Array[7]}')
        self.LabelBombo4.place(x=1030, y=450, width=160, height=300, anchor='center')

        self.GrupoATitulo = ImageTk.PhotoImage(file='UCF/GrupoATitulo.png')
        self.GrupoBTitulo = ImageTk.PhotoImage(file='UCF/GrupoBTitulo.png')
        self.GrupoCTitulo = ImageTk.PhotoImage(file='UCF/GrupoCTitulo.png')
        self.GrupoDTitulo = ImageTk.PhotoImage(file='UCF/GrupoDTitulo.png')
        self.GrupoETitulo = ImageTk.PhotoImage(file='UCF/GrupoETitulo.png')
        self.GrupoFTitulo = ImageTk.PhotoImage(file='UCF/GrupoFTitulo.png')
        self.GrupoGTitulo = ImageTk.PhotoImage(file='UCF/GrupoGTitulo.png')
        self.GrupoHTitulo = ImageTk.PhotoImage(file='UCF/GrupoHTitulo.png')

        self.BotonSortear = ImageTk.PhotoImage(file='UCF/BotonSortear.png')
        self.BotonVolver = ImageTk.PhotoImage(file='UCF/BotonVolver.png')
        Button(self.winucf, image=self.BotonSortear, command=lambda:[self.mostrar_grupos(self.Grupos,self.winucf), self.LabelBombo1.place(x=200,y=2000), self.LabelBombo2.place(x=200,y=2000),
                                                            self.LabelBombo3.place(x=200,y=2000), self.LabelBombo4.place(x=200,y=2000),
                                                            Label(self.winucf, image=self.GrupoATitulo).place(x=250, y=255, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoBTitulo).place(x=510, y=255, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoCTitulo).place(x=770, y=255, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoDTitulo).place(x=1030, y=255, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoETitulo).place(x=250, y=475, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoFTitulo).place(x=510, y=475, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoGTitulo).place(x=770, y=475, anchor='center'),
                                                            Label(self.winucf, image=self.GrupoHTitulo).place(x=1030, y=475, anchor='center')]).place(x=560, y=200, anchor='center')
        Button(self.winucf, image=self.BotonVolver, command=lambda:[self.winucf.destroy(),
                                                                    pygame.mixer.music.load('EuropaLeagueAmsterdam.mp3'),
                                                                    pygame.mixer.music.set_volume(0.3),
                                                                    pygame.mixer.music.play(1000),
                                                                    ]).place(x=720, y=200, anchor='center')

    def bombos_champions_league(self):
        self.Bombo1 = Cola(8)
        self.Bombo2 = Cola(8)
        self.Bombo3 = Cola(8)
        self.Bombo4 = Cola(8)

        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        [campeonPremier, campeonLaLiga, campeonSerieA, campeonLigue1, campeonBundesliga, campeonPrimeiraLiga,
         campeonUCL, campeonUEL] = [0, 0, 0, 0, 0, 0, 0, 0]
        for row in db_rows:
            if row[1] == 'Premier League' and row[2] == 1:
                campeonPremier = row[0]
                self.Bombo1.enqueue(campeonPremier)
            elif row[1] == 'LaLiga' and row[2] == 1:
                campeonLaLiga = row[0]
                self.Bombo1.enqueue(campeonLaLiga)
            elif row[1] == 'Serie A' and row[2] == 1:
                campeonSerieA = row[0]
                self.Bombo1.enqueue(campeonSerieA)
            elif row[1] == 'Ligue 1' and row[2] == 1:
                campeonLigue1 = row[0]
                self.Bombo1.enqueue(campeonLigue1)
            elif row[1] == 'Bundesliga' and row[2] == 1:
                campeonBundesliga = row[0]
                self.Bombo1.enqueue(campeonBundesliga)
            elif row[1] == 'Primeira Liga' and row[2] == 1:
                campeonPrimeiraLiga = row[0]
                self.Bombo1.enqueue(campeonPrimeiraLiga)
            elif row[5] == 'UEFA Champions League (Campeón vigente)':
                campeonUCL = row[0]
                self.Bombo1.enqueue(campeonUCL)
            elif row[5] == 'UEFA Europa League (Campeón vigente)':
                campeonUEL = row[0]
                self.Bombo1.enqueue(campeonUEL)

        query = 'SELECT * FROM equipo ORDER BY ranking_UEFA DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[0] not in [campeonPremier, campeonLaLiga, campeonSerieA, campeonLigue1, campeonBundesliga,
                              campeonPrimeiraLiga, campeonUCL, campeonUEL] and row[5]=='UEFA Champions League':
                if not self.Bombo2.isFull():
                    self.Bombo2.enqueue(row[0])
                else:
                    if not self.Bombo3.isFull():
                        self.Bombo3.enqueue(row[0])
                    else:
                        self.Bombo4.enqueue(row[0])

        self.Bombos=[self.Bombo1,self.Bombo2,self.Bombo3,self.Bombo4]
        return self.Bombos

    def bombos_europa_league(self):
        self.Bombo1 = Cola(8)
        self.Bombo2 = Cola(8)
        self.Bombo3 = Cola(8)
        self.Bombo4 = Cola(8)

        campeonUCF=0
        query = 'SELECT * FROM equipo'
        db_rows = self.run_query(query)
        for row in db_rows:
            if  row[5] == 'UEFA Conference League (Campeón vigente)':
                campeonUCF = row[0]
                self.Bombo1.enqueue(campeonUCF)

        query = 'SELECT * FROM equipo ORDER BY ranking_UEFA DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[0]!=campeonUCF and row[5]=='UEFA Europa League':
                if not self.Bombo1.isFull():
                    self.Bombo1.enqueue(row[0])
                else:
                    if not self.Bombo2.isFull():
                        self.Bombo2.enqueue(row[0])
                    else:
                        if not self.Bombo3.isFull():
                            self.Bombo3.enqueue(row[0])
                        else:
                            self.Bombo4.enqueue(row[0])

        self.Bombos=[self.Bombo1,self.Bombo2,self.Bombo3,self.Bombo4]
        return self.Bombos

    def bombos_conference_league(self):
        self.Bombo1 = Cola(8)
        self.Bombo2 = Cola(8)
        self.Bombo3 = Cola(8)
        self.Bombo4 = Cola(8)

        query = 'SELECT * FROM equipo ORDER BY ranking_UEFA DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[5] == 'UEFA Conference League':
                if not self.Bombo1.isFull():
                    self.Bombo1.enqueue(row[0])
                else:
                    if not self.Bombo2.isFull():
                        self.Bombo2.enqueue(row[0])
                    else:
                         if not self.Bombo3.isFull():
                            self.Bombo3.enqueue(row[0])
                         else:
                            self.Bombo4.enqueue(row[0])

        self.Bombos = [self.Bombo1, self.Bombo2, self.Bombo3, self.Bombo4]
        return self.Bombos

    def sortear_Grupos(self,Bombo1,Bombo2,Bombo3,Bombo4):
        self.GrupoA = Cola(4)
        self.GrupoB = Cola(4)
        self.GrupoC = Cola(4)
        self.GrupoD = Cola(4)
        self.GrupoE = Cola(4)
        self.GrupoF = Cola(4)
        self.GrupoG = Cola(4)
        self.GrupoH = Cola(4)

        self.Grupos1 = random.sample(
            [self.GrupoA,self.GrupoB,self.GrupoC,self.GrupoD,self.GrupoE,self.GrupoF,self.GrupoG,self.GrupoH],8)
        for grupo in self.Grupos1:
            grupo.enqueue(Bombo1.dequeue())

        self.GrupoAArray = self.GrupoA.convertirArray()
        self.GrupoBArray = self.GrupoB.convertirArray()
        self.GrupoCArray = self.GrupoC.convertirArray()
        self.GrupoDArray = self.GrupoD.convertirArray()
        self.GrupoEArray = self.GrupoE.convertirArray()
        self.GrupoFArray = self.GrupoF.convertirArray()
        self.GrupoGArray = self.GrupoG.convertirArray()
        self.GrupoHArray = self.GrupoH.convertirArray()
        self.Grupos2 = random.sample(
            [self.GrupoAArray,self.GrupoBArray,self.GrupoCArray,self.GrupoDArray,self.GrupoEArray,self.GrupoFArray,self.GrupoGArray,self.GrupoHArray],8)
        self.Bombo2Array = Bombo2.convertirArray()
        indexsort=0
        indexgrup=0
        self.Grupos2sorteados=[]
        self.Equipos2sorteados=[]
        self.indexaux=0
        while len(self.Grupos2sorteados)<8 and indexgrup<8:
            compest=True
            equiposort=self.Bombo2Array[indexsort]
            ligasgrupo=[]
            gruposort=[self.Grupos2[indexgrup][0]]
            equipoorig1=gruposort[0]
            query = 'SELECT * FROM equipo'
            db_rows = self.run_query(query)
            for row in db_rows:
                if equipoorig1==row[0]:
                    ligasgrupo.append(row[1])
            for indexcomp in range (len(ligasgrupo)):
                query = 'SELECT * FROM equipo'
                db_rows = self.run_query(query)
                for row in db_rows:
                    if equiposort==row[0]:
                        if row[1]==ligasgrupo[indexcomp]:
                            compest=False
                            indexgrup=indexgrup+1
            if compest and gruposort not in self.Grupos2sorteados:
                self.Equipos2sorteados.append(equiposort)
                self.Grupos2sorteados.append(gruposort)
                indexgrup=indexgrup+1
                indexsort=indexsort+1
            elif gruposort in self.Grupos2sorteados:
                indexgrup = indexgrup + 1
            self.indexaux = self.indexaux + 1
            if self.indexaux > 64:
                return -1
            if indexsort==8:
                indexsort=0
            if indexgrup==8:
                indexgrup=0
        [self.sortA2, self.sortB2, self.sortC2, self.sortD2, self.sortE2, self.sortF2, self.sortG2, self.sortH2]=[0,0,0,0,0,0,0,0]
        try:
            for index in range(8):
                if self.Grupos2sorteados[index] == [self.GrupoAArray[0]]:
                    self.GrupoA.enqueue(self.Equipos2sorteados[index])
                    self.sortA1 = self.GrupoAArray[0]
                    self.sortA2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoBArray[0]]:
                    self.GrupoB.enqueue(self.Equipos2sorteados[index])
                    self.sortB1 = self.GrupoBArray[0]
                    self.sortB2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoCArray[0]]:
                    self.GrupoC.enqueue(self.Equipos2sorteados[index])
                    self.sortC1 = self.GrupoCArray[0]
                    self.sortC2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoDArray[0]]:
                    self.GrupoD.enqueue(self.Equipos2sorteados[index])
                    self.sortD1 = self.GrupoDArray[0]
                    self.sortD2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoEArray[0]]:
                    self.GrupoE.enqueue(self.Equipos2sorteados[index])
                    self.sortE1 = self.GrupoEArray[0]
                    self.sortE2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoFArray[0]]:
                    self.GrupoF.enqueue(self.Equipos2sorteados[index])
                    self.sortF1 = self.GrupoFArray[0]
                    self.sortF2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoGArray[0]]:
                    self.GrupoG.enqueue(self.Equipos2sorteados[index])
                    self.sortG1 = self.GrupoGArray[0]
                    self.sortG2 = self.Equipos2sorteados[index]
                elif self.Grupos2sorteados[index] == [self.GrupoHArray[0]]:
                    self.GrupoH.enqueue(self.Equipos2sorteados[index])
                    self.sortH1 = self.GrupoHArray[0]
                    self.sortH2 = self.Equipos2sorteados[index]
        except:
            return -1

        self.Grupos3 = random.sample(
            [self.GrupoAArray, self.GrupoBArray, self.GrupoCArray, self.GrupoDArray, self.GrupoEArray, self.GrupoFArray,
             self.GrupoGArray, self.GrupoHArray], 8)
        self.Bombo3Array = Bombo3.convertirArray()
        indexsort = 0
        indexgrup = 0
        self.Grupos3sorteados = []
        self.Equipos3sorteados = []
        self.indexaux = 0
        while len(self.Grupos3sorteados) < 8 and indexgrup < 8:
            compest = True
            equiposort = self.Bombo3Array[indexsort]
            ligasgrupo = []
            gruposort = [self.Grupos3[indexgrup]]
            equipoorig1 = ''
            equipoorig2 = ''
            if gruposort == [self.GrupoAArray]:
                equipoorig1=self.sortA1
                equipoorig2=self.sortA2
            elif gruposort == [self.GrupoBArray]:
                equipoorig1=self.sortB1
                equipoorig2=self.sortB2
            elif gruposort == [self.GrupoCArray]:
                equipoorig1=self.sortC1
                equipoorig2=self.sortC2
            elif gruposort == [self.GrupoDArray]:
                equipoorig1=self.sortD1
                equipoorig2=self.sortD2
            elif gruposort == [self.GrupoEArray]:
                equipoorig1=self.sortE1
                equipoorig2=self.sortE2
            elif gruposort == [self.GrupoFArray]:
                equipoorig1=self.sortF1
                equipoorig2=self.sortF2
            elif gruposort == [self.GrupoGArray]:
                equipoorig1=self.sortG1
                equipoorig2=self.sortG2
            elif gruposort == [self.GrupoHArray]:
                equipoorig1=self.sortH1
                equipoorig2=self.sortH2
            query = 'SELECT * FROM equipo'
            db_rows = self.run_query(query)
            for row in db_rows:
                if equipoorig1 == row[0] or equipoorig2 == row[0]:
                    ligasgrupo.append(row[1])
            for indexcomp in range(len(ligasgrupo)):
                query = 'SELECT * FROM equipo'
                db_rows = self.run_query(query)
                for row in db_rows:
                    if equiposort == row[0]:
                        if row[1] == ligasgrupo[indexcomp]:
                            compest = False
                            indexgrup = indexgrup + 1
            if compest and gruposort not in self.Grupos3sorteados:
                self.Equipos3sorteados.append(equiposort)
                self.Grupos3sorteados.append(gruposort)
                indexgrup = indexgrup + 1
                indexsort = indexsort + 1
            elif gruposort in self.Grupos3sorteados:
                indexgrup = indexgrup + 1
            self.indexaux = self.indexaux + 1
            if self.indexaux >64:
                return -1
            if indexsort == 8:
                indexsort = 0
            if indexgrup == 8:
                indexgrup = 0

        [self.sortA3, self.sortB3, self.sortC3, self.sortD3, self.sortE3, self.sortF3, self.sortG3, self.sortH3] = [0,0,0,0,0,0,0,0]
        for index in range(8):
            if self.Grupos3sorteados[index] == [self.GrupoAArray]:
                self.GrupoA.enqueue(self.Equipos3sorteados[index])
                self.sortA3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoBArray]:
                self.GrupoB.enqueue(self.Equipos3sorteados[index])
                self.sortB3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoCArray]:
                self.GrupoC.enqueue(self.Equipos3sorteados[index])
                self.sortC3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoDArray]:
                self.GrupoD.enqueue(self.Equipos3sorteados[index])
                self.sortD3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoEArray]:
                self.GrupoE.enqueue(self.Equipos3sorteados[index])
                self.sortE3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoFArray]:
                self.GrupoF.enqueue(self.Equipos3sorteados[index])
                self.sortF3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoGArray]:
                self.GrupoG.enqueue(self.Equipos3sorteados[index])
                self.sortG3 = self.Equipos3sorteados[index]
            elif self.Grupos3sorteados[index] == [self.GrupoHArray]:
                self.GrupoH.enqueue(self.Equipos3sorteados[index])
                self.sortH3 = self.Equipos3sorteados[index]

        self.Grupos4 = random.sample(
            [self.GrupoAArray, self.GrupoBArray, self.GrupoCArray, self.GrupoDArray, self.GrupoEArray, self.GrupoFArray,
             self.GrupoGArray, self.GrupoHArray], 8)
        self.Bombo4Array = Bombo4.convertirArray()
        indexsort = 0
        indexgrup = 0
        self.Grupos4sorteados = []
        self.Equipos4sorteados = []
        self.indexaux = 0
        while len(self.Grupos4sorteados) < 8 and indexgrup < 8:
            compest = True
            equiposort = self.Bombo4Array[indexsort]
            ligasgrupo = []
            gruposort = [self.Grupos4[indexgrup]]
            equipoorig1 = ''
            equipoorig2 = ''
            equipoorig3 = ''
            if gruposort == [self.GrupoAArray]:
                equipoorig1 = self.sortA1
                equipoorig2 = self.sortA2
                equipoorig3 = self.sortA3
            elif gruposort == [self.GrupoBArray]:
                equipoorig1 = self.sortB1
                equipoorig2 = self.sortB2
                equipoorig3 = self.sortB3
            elif gruposort == [self.GrupoCArray]:
                equipoorig1 = self.sortC1
                equipoorig2 = self.sortC2
                equipoorig3 = self.sortC3
            elif gruposort == [self.GrupoDArray]:
                equipoorig1 = self.sortD1
                equipoorig2 = self.sortD2
                equipoorig3 = self.sortD3
            elif gruposort == [self.GrupoEArray]:
                equipoorig1 = self.sortE1
                equipoorig2 = self.sortE2
                equipoorig3 = self.sortE3
            elif gruposort == [self.GrupoFArray]:
                equipoorig1 = self.sortF1
                equipoorig2 = self.sortF2
                equipoorig3 = self.sortF3
            elif gruposort == [self.GrupoGArray]:
                equipoorig1 = self.sortG1
                equipoorig2 = self.sortG2
                equipoorig3 = self.sortG3
            elif gruposort == [self.GrupoHArray]:
                equipoorig1 = self.sortH1
                equipoorig2 = self.sortH2
                equipoorig3 = self.sortH3
            query = 'SELECT * FROM equipo'
            db_rows = self.run_query(query)
            for row in db_rows:
                if equipoorig1 == row[0] or equipoorig2 == row[0] or equipoorig3 == row[0]:
                    ligasgrupo.append(row[1])
            for indexcomp in range(len(ligasgrupo)):
                query = 'SELECT * FROM equipo'
                db_rows = self.run_query(query)
                for row in db_rows:
                    if equiposort == row[0]:
                        if row[1] == ligasgrupo[indexcomp]:
                            compest = False
                            indexgrup = indexgrup + 1
            if compest and gruposort not in self.Grupos4sorteados:
                self.Equipos4sorteados.append(equiposort)
                self.Grupos4sorteados.append(gruposort)
                indexgrup = indexgrup + 1
                indexsort = indexsort + 1
            elif gruposort in self.Grupos4sorteados:
                indexgrup = indexgrup + 1
            self.indexaux = self.indexaux + 1
            if self.indexaux > 64:
                return -1
            if indexsort == 8:
                indexsort = 0
            if indexgrup == 8:
                indexgrup = 0


        for index in range(8):
            if self.Grupos4sorteados[index] == [self.GrupoAArray]:
                self.GrupoA.enqueue(self.Equipos4sorteados[index])
                self.sortA4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoBArray]:
                self.GrupoB.enqueue(self.Equipos4sorteados[index])
                self.sortB4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoCArray]:
                self.GrupoC.enqueue(self.Equipos4sorteados[index])
                self.sortC4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoDArray]:
                self.GrupoD.enqueue(self.Equipos4sorteados[index])
                self.sortD4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoEArray]:
                self.GrupoE.enqueue(self.Equipos4sorteados[index])
                self.sortE4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoFArray]:
                self.GrupoF.enqueue(self.Equipos4sorteados[index])
                self.sortF4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoGArray]:
                self.GrupoG.enqueue(self.Equipos4sorteados[index])
                self.sortG4 = self.Equipos4sorteados[index]
            elif self.Grupos4sorteados[index] == [self.GrupoHArray]:
                self.GrupoH.enqueue(self.Equipos4sorteados[index])
                self.sortH4 = self.Equipos4sorteados[index]
            self.Grupos = [self.GrupoA, self.GrupoB, self.GrupoC, self.GrupoD, self.GrupoE, self.GrupoF, self.GrupoG,
                       self.GrupoH]

        return self.Grupos

    def mostrar_grupos(self,Grupos,window):
        self.GrupoAArray = Grupos[0].convertirArray()
        self.GrupoBArray = Grupos[1].convertirArray()
        self.GrupoCArray = Grupos[2].convertirArray()
        self.GrupoDArray = Grupos[3].convertirArray()
        self.GrupoEArray = Grupos[4].convertirArray()
        self.GrupoFArray = Grupos[5].convertirArray()
        self.GrupoGArray = Grupos[6].convertirArray()
        self.GrupoHArray = Grupos[7].convertirArray()
        Label(window, text=f'{self.GrupoAArray[0]}\n\n{self.GrupoAArray[1]}\n\n{self.GrupoAArray[2]}\n\n{self.GrupoAArray[3]}').place(x=250, y=350, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoBArray[0]}\n\n{self.GrupoBArray[1]}\n\n{self.GrupoBArray[2]}\n\n{self.GrupoBArray[3]}').place(x=510, y=350, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoCArray[0]}\n\n{self.GrupoCArray[1]}\n\n{self.GrupoCArray[2]}\n\n{self.GrupoCArray[3]}').place(x=770, y=350, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoDArray[0]}\n\n{self.GrupoDArray[1]}\n\n{self.GrupoDArray[2]}\n\n{self.GrupoDArray[3]}').place(x=1030, y=350, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoEArray[0]}\n\n{self.GrupoEArray[1]}\n\n{self.GrupoEArray[2]}\n\n{self.GrupoEArray[3]}').place(x=250, y=570, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoFArray[0]}\n\n{self.GrupoFArray[1]}\n\n{self.GrupoFArray[2]}\n\n{self.GrupoFArray[3]}').place(x=510, y=570, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoGArray[0]}\n\n{self.GrupoGArray[1]}\n\n{self.GrupoGArray[2]}\n\n{self.GrupoGArray[3]}').place(x=770, y=570, width=160, height=150, anchor='center')
        Label(window, text=f'{self.GrupoHArray[0]}\n\n{self.GrupoHArray[1]}\n\n{self.GrupoHArray[2]}\n\n{self.GrupoHArray[3]}').place(x=1030, y=570, width=160, height=150, anchor='center')

if __name__ == "__main__":
    window = Tk()
    appplication = main(window)
    window.mainloop()
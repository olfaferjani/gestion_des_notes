# encoding: utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
import pymysql
Window.clearcolor = (.0,.255,.255,150)
#coding:utf-8
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    surnamee = ObjectProperty(None)
    email1 = ObjectProperty(None)
    passwd = ObjectProperty(None)
    nomEtudiant=StringProperty('')
    prenomEtudiant=StringProperty('')
    email=StringProperty('')
    password=StringProperty('')

    def submit(self):
        nomEtudiant= self.surnamee.text
        prenomEtudiant=self.namee.text
        email=self.email1.text
        password=self.passwd.text
        if self.namee.text != "" and self.surnamee.text!="" and self.email1.text != "" and self.email1.text.count("@") == 1 and self.email1.text.count(".") > 0:
            if self.passwd.text != "":
                conx= pymysql.connect(host="localhost",user="root",passwd="",db="login")
                myCursor=conx.cursor()
                myCursor.execute("INSERT INTO etudiant(nomEtudiant,prenomEtudiant,email,password) VALUES(%s,%s,%s,%s)",(nomEtudiant,prenomEtudiant,email,password))
                conx.commit()
                conx.close()
                self.reset()
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()
    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email1.text = ""
        self.passwd.text = ""
        self.namee.text = ""
        self.surnamee.text=""    
class LoginWindow(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    email = StringProperty('')
    pwd=StringProperty('')
    
    def loginCheck(self):
        email = self.username.text
        pwd=self.password.text
        conx= pymysql.connect(host="localhost",user="root",passwd="",db="login")
        myCursor=conx.cursor()
        if email=='admin@admin.com':
                admincheck=myCursor.execute("SELECT idEtudiant FROM etudiant where email=%s AND password=%s",(email,pwd))
                if admincheck>0:
                    print(admincheck)
                    self.reset()
                    sm.current = "admin"
                
        else:
            result = myCursor.execute("SELECT * FROM etudiant WHERE email = %s AND password = %s",(email,pwd))
            if(result > 0):
                print("user found")
                MainWindow.current = email
                self.reset()
                sm.current = "main"
            else:
                print("user not found")
                invalidLogin()
        conx.close()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.username.text = ""
        self.password.text = ""

    def checkAdmin(self):
        sm.current = "admin"

class MainWindow(Screen):
    n = ObjectProperty(None)
    b = ObjectProperty(None)
    c = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self):
         rowList=list()
         conx= pymysql.connect(host="localhost",user="root",passwd="",db="login")
         myCursor=conx.cursor()
         
         result= myCursor.execute("SELECT prenomEtudiant FROM etudiant WHERE email = %s ",(self.current))
         for row in myCursor.fetchall():
             print(result)
         self.n.text = "Hello " + str(row[0])+" there is your transcript for this semester"
         r=myCursor.execute("SELECT note FROM notes WHERE idEtudiant=(SELECT idEtudiant FROM etudiant WHERE email=%s)",(self.current))
         records = myCursor.fetchall()
         for row in records:
             rowList.append(row[0])
         self.b.text = "Français: "+ str(rowList[0])+"\n\n"+"Anglais: "+str(rowList[1])+"\n\n"+"programmation c: "+str(rowList[2])+"\n\n"+"Python: "+str(rowList[3])+"\n\n"+"Base de donnée: "+ str(rowList[4])+"\n\n"+"Tech multimedia: "+ str(rowList[5])
         m=myCursor.execute("SELECT SUM(note*coefficient)/SUM(coefficient) FROM module,notes WHERE notes.idEtudiant=(SELECT idEtudiant FROM etudiant WHERE email=%s) AND module.idModule=notes.idModule",(self.current))
         for row in myCursor.fetchall():
            print(m)
         self.c.text = "Moyenne: " + str(row[0])
         conx.close()

class WindowManager(ScreenManager):
    pass
def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()
kv = Builder.load_file("my.kv")

sm = WindowManager()

#db=pymysql.connect("dataBase.py")
class AdminWindow(Screen):
    nomEtudiant=ObjectProperty()
    prenomEtudiant=ObjectProperty()
    nomEtudiant1=StringProperty('')
    prenomEtudiant1=StringProperty('')
    notefrancais=ObjectProperty()
    notefrancais1=float()
    noteanglais=ObjectProperty()
    noteanglais1=float()
    
    def logOut(self):
        sm.current = "login"
    def ajoutNotes(self):
        moduleList=list()
        lesNotes=list()
        i = 0
        nomEtudiant1=self.nomEtudiant.text
        prenomEtudiant1=self.prenomEtudiant.text

        notefrancais1=self.notefrancais.text
        noteanglais1=self.noteanglais.text
        notec1=self.notec.text
        notepython1=self.notepython.text
        notedb1=self.notebd.text
        notemultimedia1=self.notemultimedia.text
        lesNotes=['français','anglais','programmation c','python','base de donnée','tech multimedia']
        print("les notes :",lesNotes[0])
        
        conx= pymysql.connect(host="localhost",user="root",passwd="",db="login")
        myCursor=conx.cursor()
        resIdEtudiant=myCursor.execute("SELECT idEtudiant from etudiant where nomEtudiant=%s AND prenomEtudiant=%s",(nomEtudiant1,prenomEtudiant1))
        recordsIdEtudiant=myCursor.fetchall()
        if resIdEtudiant > 0 :
            for row in recordsIdEtudiant :
              myIdEtudiant=row[0]
            while i < lesNotes.__len__():
                resIdModule=myCursor.execute("SELECT idModule from module where nomModule=%s",(lesNotes[i]))
                recordsIdModule=myCursor.fetchall()
                if resIdModule > 0 :
                    for row in recordsIdModule :
                        moduleList.append(row[0])
                    resNoteExists=myCursor.execute("SELECT note from notes where idModule=%s AND idEtudiant=%s",(moduleList[i],myIdEtudiant))
                    recordsNoteExists=myCursor.fetchall()
                    if resNoteExists>0:
                        print("note français", notefrancais1)
                        print("id etudiant", myIdEtudiant)
                        print("id module", moduleList[i])
                        modifyNote=myCursor.execute("UPDATE notes SET note=%s where idModule=%s AND idEtudiant=%s",(notefrancais1,moduleList[i],myIdEtudiant))
                        conx.commit()
                        print("res modif note",modifyNote)
                        if modifyNote>0:
                            # pop = Popup(title='ajout note',
                            #             content=Label(text='note ajouter avec succée'),
                            #             size_hint=(None, None), size=(400, 400))
                            # pop.open()
                            i=i+1
                        else:
                            pop = Popup(title='ajout note echouer',
                                        content=Label(text='l\'ajout note a échoué)'),
                                        size_hint=(None, None), size=(400, 400))
                            pop.open()
                            break
                    else :
                        print("note français1", notefrancais1)
                        print("id etudiant1", myIdEtudiant)
                        print("id module1", moduleList[i])
                        modifyNote = myCursor.execute("INSERT INTO notes (idEtudiant, idModule, note) VALUES (%s,%s,%s)",(myIdEtudiant, moduleList[i], notefrancais1))
                        conx.commit()
                        print("res insert note", modifyNote)
                        if modifyNote>0:
                            # pop = Popup(title='ajout note',
                            #             content=Label(text='note ajouter avec succée'),
                            #             size_hint=(None, None), size=(400, 400))
                            # pop.open()
                            i=i+1
                        else:
                            pop = Popup(title='ajout note echouer',
                                        content=Label(text='l\'ajout note a échoué)'),
                                        size_hint=(None, None), size=(400, 400))
                            pop.open()
                            break
                else :
                    print("erreur serveur")
            print("moduleList :", moduleList)
            pop = Popup(title='ajout avec succes',
                        content=Label(text='les notes sont ajoutées avec succès'),
                        size_hint=(None, None), size=(400, 400))
            pop.open()
        else :
            pop = Popup(title='Invalid Login',
              content=Label(text='cet etudiant n\'existe pas'),
              size_hint=(None, None), size=(400, 400))
            pop.open()
        # myCursor.execute("INSERT INTO notes() VALUES(%f,%f,%f,%f;%f,%f) where idEtudiant = ",())
        # conx.commit()
        conx.close()
    
    def reset(self):
        self.nomEtudiant.text = ""
        self.prenomEtudiant.text = ""
        self.notefrancais.text = ""
        self.noteanglais.text = ""
        self.notec.text= ""
        self.notepython.text = ""
        self.notebd.text= ""
        self.notemultimedia.text = ""
        



screens = [LoginWindow(name="login"),CreateAccountWindow(name="create"),MainWindow(name="main"),AdminWindow(name="admin")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

# class Test(TabbedPanel):
#     pass


# class TabbedPanelApp(App):
#     def build(self):
#         return Test()



class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
    #je suis la oussi

# je suis la olfa

from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()
root.geometry("900x500")
root.title("Gestion des étudiants")
style= ttk.Style ()



class E(object):

    def __init__(self,nom,email,age):
        self.id = None
        self.nom = nom
        self.email = email
        self.age = age
        self.conn = sqlite3.connect ('mabase. db')
        self.cur = self.conn.cursor ()

    def get_nom(self):
        return self.nom

    def get_email(self):
        return self.email
    def get_age(self):
        return self.age

    def get_id(self):
        return self.id

    def set_nom(self,nnom):
        self.nom = nnom
    def set_email(self,ne):
        self.email = ne
    def set_age(self,na):
        self.age = na
    def set_id(self,ni):
        self.id = ni

    def save(self):

        try:
            rs = self.cur.execute(
                f"INSERT INTO students(Nom,Age,Email) VALUES('{self.get_nom()}','{self.get_age()}','{self.get_email()}');"
            )

            self.conn.commit()
        except Exception as e:
            print(f"Couldn't connect to {e}")
    def delete(self):
        try:
            rs = self.cur.execute(
                f"DELETE FROM students WHERE ID = {self.get_id()}"
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting students : {e}")
    def update(self):
        try:
            rs = self.cur.execute(
                f"UPDATE students SET Nom='{self.get_nom()}',Email ='{self.get_email()}',Age='{self.get_age()}' WHERE ID = {self.get_id()}"
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error updating students : {e}")

class Etudiant(object):

    def __init__(self, obj=None):
        self.obj = obj
        self.fenetre = Tk()
        self.fenetre.geometry("550x350")
        self.fenetre.title("Ajouter un étudiant")
    def ajouter_form(self):
        text = Label (self.fenetre, text = "Ajouter un nouvel étudiant",font="Algerian 16 bold" )
        Nom = Label (self.fenetre, text = "Nom : " )
        Email = Label (self.fenetre, text="Email : ")
        Age = Label (self.fenetre, text="Age : ")
        champNom = Entry (self.fenetre)
        champEmail = Entry (self.fenetre)
        champAge = Entry (self.fenetre)
        a = ttk.Button(self.fenetre,text="Enregistrer",style="BW.TButton")
        #Application de la méthode place () aux widget
        text.place(x=75, y=20)
        Nom. place (x=5, y=75, width=160, height=25)
        champNom. place (x=175, y=75, width=160, height=25)
        Email. place (x=5, y=120, width=160, height=25)
        champEmail. place (x=175, y=120, width=160, height=25)

        Age.place(x=5, y=165, width=160, height=25)
        champAge.place (x=175, y=165, width=160, height=25)
        a.place(x=175, y=205)

        def champs(event):
            nom = champNom.get()
            email = champEmail.get()
            age = champAge.get()

            etudiant = E(
                nom=nom,
                email=email,
                age=age
            )
            etudiant.save()
            self.fenetre.destroy()

        a.bind('<Button-1>', champs)
        self.fenetre.mainloop()
        #cancel.bind('<Button-1>',self.fenetre.mainloop())
        self.fenetre.mainloop()

def add_btn_(event):
    e = Etudiant()
    e.ajouter_form()
style.configure("BW.TButton" , foreground="blue" , background="#ccc")
# === Création de l ’ objet Treeview ===
tree = ttk.Treeview(root , columns = (1 ,2 ,3 ,4) , height = 5 ,show = "headings")
tree. place (x=100,y=100, width=750)
add_btn =ttk.Button(text="Nouvel Etudiant" , style="BW.TButton")
add_btn.place(x=100,y=50)
edit_btn =ttk.Button(text="Modifier" , style="BW.TButton")
edit_btn.place(x=230,y=50)
delete_btn =ttk.Button(text="Supprimer" , style="BW.TButton")
delete_btn.place(x=330,y=50)
update_btn =ttk.Button(text="Actualiser" , style="BW.TButton")
update_btn.place(x=430,y=50)


add_btn.bind ("<Button-1>", add_btn_)
# === dimension des colonnes ===
tree.column(1 , width = 10)
tree.column(2 , width = 160)
tree.column(3 , width = 130)
tree.column(4 , width=10)
# === Création de l ’ entête ===
tree.heading(1 , text="ID")
tree.heading(2 , text="Nom")
tree.heading(3 , text="Email")
tree.heading(4 , text="Age")
def clear_all():
   for item in tree.get_children():
      tree.delete(item)
def list_student():
    conn = sqlite3.connect ('mabase. db') # Connexion à la base de données mabase.db
# === Création d ’un cursor et sélection des données ===
    cur = conn.cursor ()
    try:
        result= cur.execute ("select* from students ")
        conn .commit()
    except:
        result = cur.execute ("""create table if not exists students(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom VARCHAR(50),
            Email VARCHAR(50),
            Age VARCHAR(50)
            );""")
    clear_all()
    # Insertion des données au sein de l ’ objet Treeview
    for row in result:
        tree.insert( '' , 'end' , values =(row[0] , row[1] , row[2] ,row[3]) )
    conn.close ()
list_student()
def edit (event) :
    e = Etudiant()
    e.modifier_form()


def delete (event) :
    select = tree .item(tree.selection())['values']
    etudiant = E(
        nom=select[1],
        email=select[2],
        age=select[3]
    )
    etudiant.set_id(select[0])
    etudiant.delete()

def update_list(event):
    print("Hello")
edit_btn.bind ("<Button-1>" ,  edit)
delete_btn.bind ("<Button-1>" , delete)
update_btn.bind ("<Button-1>" , update_list)
root . mainloop ()

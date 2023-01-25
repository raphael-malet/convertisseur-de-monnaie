# convertisseur de monnaie

# liste des imports
from tkinter import *
from tkinter import ttk
import tkinter as tk
from datetime import datetime
import requests

# varible global du distionnaire des taux en fonction des devises
donne = ''


# fonction qui permet de convertir
def convertion(fenetre_devise, fenetre_direction, donne, convertir, fenetre_final):
    # on essait de convertir la somme de départ
    try:
        # on arrondit la somme de départ a deux chiffre apres la virgule
        somme_convertion = float(convertir.get())
        somme_convertion = round(somme_convertion, 2)
        # boucle qui permet d'avoir le taux de depart en focntion de la devise choisit
        for i in donne:
            if i == fenetre_devise.get():
                taux_depart = donne.get(i)
                break
        # boucle permet d'avoir le taux de la devise d'arrivé
        for j in donne:
            if j == fenetre_direction.get():
                taux_arrive = donne.get(j)
                break

        # variable du resulatat final arrondit a 2 chiffre apres la virgule et mis en str
        final = somme_convertion / taux_depart * taux_arrive
        final = round(final, 2)
        final = str(final) + ' ' + j


    # si impossible le resultat retournera erreur
    except:
        for i in donne:
            if i == fenetre_devise.get():
                taux_depart = donne.get(i)
                break

        for j in donne:
            if j == fenetre_direction.get():
                taux_arrive = donne.get(j)
                break
        somme_convertion = convertir.get()
        final = 'ERREUR'

    taux_de_change = 1 / taux_depart * taux_arrive
    taux_de_change = round(taux_de_change, 2)
    taux_de_change = str(taux_de_change)
    # on ajoute le resultat dans le fichier txt
    stockage_historique(somme_convertion, i, j, final, taux_de_change)
    # on fait apparaitre le résultat dans la fenetre de l'application
    fenetre_final.config(text=final)


# focntion qui permet d'écrire dans le fichier hsitorique
def stockage_historique(convertion, devise_depart, devise_arrive, resulat, taux):
    ouverture_historique = open('historique.txt', 'a')

    date = str(datetime.now().date()).split('-')
    date.reverse()
    date = "-".join(date)
    # ajout du résultat dans le fichier historique.txr
    ajout_contenu = (
            str(convertion) + ' ' + devise_depart + ' vers ' + devise_arrive + ' le ' + date + ' avec un taux de ' +
            taux + ' donne ' + str(resulat) + '\n')
    ouverture_historique.write(ajout_contenu)
    ouverture_historique.close()
    lecture_historique()


# fonction qui lit l'historique lors d'un nouveau calcul
def lecture_historique():
    # condition qui voit si l'historique et vide ou pas pour ne pas avoir message d'erreur dans la console
    try:
        donnee_historique = open('historique.txt', 'r')
        # permet d'assigner la lecture de l'historique a une variable.
        donnee_historique = donnee_historique.readlines()
        donnee_historique = donnee_historique[-1]
        afficher_historique(historique, donnee_historique)
    # si historique vide on qui la focntion
    except:
        return


# fonction qui ajoute le nouveau calcul dans la section historique de la fenetre
def afficher_historique(historique, expression):
    historique.insert(0, expression)


def affichage_historique_ouverture_appli(historique):
    historique_ouverture = open('historique.txt', 'r')
    historique_ouverture = historique_ouverture.readlines()

    for i in range(len(historique_ouverture)):
        historique.insert(0, historique_ouverture[i])


# focntion qui supprime le contenu dans la section historique de la fenetre
def supprimer_historique(historique):
    historique.delete(0, END)
    # on retrourne vers la fonction pour supprimer le contenu du fichier historique
    effacer_historique_fichier()


# focntion pour effacer l'historique
def effacer_historique_fichier():
    historique_effacement = open('historique.txt', 'w')
    historique_effacement.write('')  # permet d'effacer le contenu de l'historique
    historique_effacement.close()


# focntion qui permet de prendre les taux d'échange lors de l'ouverture de l'application
def prendre_taux_echange():
    # on met la liste des taux d'échange dans une vriable global
    global donne
    # requette pour avoir les taux d'échange
    reponse = requests.get("https://openexchangerates.org/api/latest.json",
                           params={"app_id": "973969dc42df4db4bb1ad9d53a89a13c"})

    # varible qui prends le taux d'échange
    taux = reponse.json()

    # devise et lerus taux d'échange dans une liste
    donne = {"EUR": taux["rates"]["EUR"],
             "USD": taux["rates"]["USD"],
             "JPY": taux["rates"]["JPY"],
             "GBP": taux["rates"]["GBP"],
             "CAD": taux["rates"]["CAD"],
             "CHF": taux["rates"]["CHF"],
             "DZD": taux["rates"]["DZD"],
             "RUB": taux["rates"]["RUB"],
             }


# -----------------------
# AFFICHAGE DE LA FENETRE
# -----------------------
if __name__ == '__main__':
    fenetre = Tk()
    fenetre.geometry("400x380")
    fenetre.title("convertisseur de monnaie")
    fenetre.configure(bg='#000000')

    fenetre.__name = StringVar()

    titre = Label(fenetre, text="Entrer la somme que vous \nvoulez convertir", bg='#000000', fg='WHITE')
    titre.grid(column=0, row=1)

    somme_a_convertir = Entry(fenetre, bg='#000000', fg='WHITE')
    somme_a_convertir.focus_set()
    somme_a_convertir.grid(column=1, row=1)

    # liste des devises disponnible
    liste_devise = ['EUR', 'USD', "JPY", "GBP", "CAD", "CHF", "DZD", "RUB"]

    devise_de_depart = Label(fenetre, text="Devise de départ", bg='#000000', fg='WHITE')
    devise_de_depart.grid(column=0, row=2)
    # menu deroulant des devises
    fenetre_liste_devise = ttk.Combobox(fenetre, values=liste_devise, background='#000000')
    fenetre_liste_devise.current(0)
    fenetre_liste_devise.grid(column=1, row=2)

    devise_arrive = Label(fenetre, text="Devise d'arrivé", bg='#000000', fg='WHITE')
    devise_arrive.grid(column=0, row=3)

    # menu deroulant des devises
    fenetre_liste_devise_direction = ttk.Combobox(fenetre, values=liste_devise)
    fenetre_liste_devise_direction.current(1)
    fenetre_liste_devise_direction.grid(column=1, row=3)

    # bouton convertir
    bouton_convertir = Button(fenetre, text="Convertir", bg='#000000', fg='WHITE')
    bouton_convertir.bind("<Button-1>",
                          lambda e: convertion(fenetre_liste_devise, fenetre_liste_devise_direction, donne,
                                               somme_a_convertir, somme_final_fenetre))
    bouton_convertir.grid(column=1, row=4)

    # section texte somme final:
    final_texte = Label(fenetre, text="Résultat:", bg='#000000', fg='WHITE')
    final_texte.grid(row=5, column=0)

    # section somme final
    somme_final_fenetre = Label(fenetre, text='', height=2, bg='#000000', fg='WHITE')
    somme_final_fenetre.focus_set()
    somme_final_fenetre.grid(row=5, column=1, sticky=EW)

    # fenetre historique
    historique = tk.Listbox(fenetre, height=10, bg='#000000', fg='WHITE')
    historique.grid(row=6, columnspan=2, sticky=EW)

    # Scrollbarr vertical  relier a l'historique
    scrollbar_vertical = ttk.Scrollbar(fenetre, orient='vertical', command=historique.yview)
    scrollbar_vertical.grid(row=6, column=2, sticky='nsw')
    # communication entre la scrollbarr et le fenetre de l'historique
    historique['yscrollcommand'] = scrollbar_vertical.set

    # scrollbar horizontal
    scrollbar_horizonral = ttk.Scrollbar(fenetre, orient='horizontal', command=historique.xview)
    scrollbar_horizonral.grid(row=7, columnspan=3, sticky='ews')
    historique['xscrollcommand'] = scrollbar_horizonral.set

    boutton_supprimer_historique = Button(fenetre, text='Supprimer historique', bg='#000000', fg='WHITE')
    boutton_supprimer_historique.bind("<Button-1>",
                                      lambda e: supprimer_historique(historique))
    boutton_supprimer_historique.grid(columnspan=2, row=8)

    # on prend les taux de change lors de l'ouverture de l'application
    prendre_taux_echange()
    # focntion qui affiche l'historique lors de l'ouverture le l'application
    affichage_historique_ouverture_appli(historique)
    # ouverture de la fenetre
    fenetre.mainloop()

from tkinter import * #* per importare tutto, cioè tutti i moduli di tkinter
from time import sleep
import threading 
import random

#--------------variabili globali----------------
colpi = 0
buco = 0

#--------------configurazione della finestra----------------
finestra = Tk()
finestra.config(bg="#016911", width=500, height=520) # colore di sfondo e dimensioni della finestra
finestra.resizable(0, 0) #0,0 perchè non voglio che la finestra possa essere ridimensionata, 0 per x e 0 per y
finestra.attributes('-topmost', True) #rebde la finestra sempre in primo piano, conosco solo topmost per ora
finestra.title("Acchiappa la Talpa by cuom0_") #nome della finestra e cuom0_ è il mio nickname
finestra.iconbitmap("moleico.ico") #icona della finestra, un'immagine di una talpa (Mole in inglese) (Ha lo stile dei Monty Mole di Super Mario World [SNES], trovato su Google.)

titolo = Label(text="ACCHIAPPA LA TALPA!", font=("Arial", 24, "bold"), bg='#444444', fg='#FFFFFF') #titolo del gioco (magari potrei rimpiazzarlo con un logo?)
titolo.place(x=0, y=10) #Avendo una risoluzione certa e non modificabile, ho preferito risparmiare tempo e non usare pack(), dopotutto non serve che un gioco come Whack-A-Mole sia responsive o simili

punteggio_label = Label(text=colpi, width=7, font=('Arial', 24, "bold"), bg='#666666', fg='white') #punteggio del giocatore
punteggio_label.place(x=0, y=52)

commento = Label(text="", width=20, bg='#555555', fg='white', font=("Arial", 14, "bold")) #commento finale, inizialmente vuoto e poi riempito in base al punteggio
commento.place(x=139, y=52)

#--------------il gioco in sé----------------
def preparazione(): #firma iniziale, countdown e inizio del gioco. Appena il gioco inizia, punteggio_label sarà degno del suo nome.
    punteggio_label.config(text="cuom0_")
    sleep(2)
    punteggio_label.config(text="3..")
    sleep(1)
    punteggio_label.config(text="2..")
    sleep(1)
    punteggio_label.config(text="1..")
    sleep(1)
    punteggio_label.config(text="VIA!")
    sleep(1)
    punteggio_label.config(text="0")

def valutazione(): #Essendo un numero definito di talpe, volevo fare che il giocatore venisse giudicato alla fine del gioco. (Basato sul punteggio) 
    #03/03/2025: ho dovuto fixare l'interpolazione, avevo mispellato
    if colpi < 10:
        commento.config(text=f"TERRIBILE... {colpi} colpi!")
    elif colpi < 20:
        commento.config(text=f"PESSIMO {colpi} colpi!")
    elif colpi < 30:
        commento.config(text=f"PUOI MIGLIORARE! {colpi} colpi!")
    elif colpi < 40:
        commento.config(text=f"BUONO {colpi} colpi!")
    elif colpi < 50:
        commento.config(text=f"OTTIMO! {colpi} colpi!")
    elif colpi < 75:
        commento.config(text=f"ECCEZIONALE! {colpi} colpi!")
    elif colpi == 80:
        commento.config(text=f"PERFETTO! {colpi} colpi!")

def colpisci():
    global buco, colpi #Global per poter modificare le variabili globali, corrisponde in C# a public
    if buco: #if buco è true (1), cioè se c'è una talpa
        bottoni[buco - 1].config(text='X', bg='#990000', fg='white',state='disabled') #lo rende rosso e con una X (#990000 è un rosso scuro)
        colpi += 1 #incremento del punteggio
        punteggio_label.config(text=str(colpi)) #aggiornamento del punteggio

def avvia(): #funzione per iniziare il gioco, resetta il punteggio e il commento, disabilita il bottone di riprova e avvia il thread
    global colpi
    colpi = 0
    commento.config(text="")
    bottone_riprova.config(state='disabled') #stato iniziale disabilitato
    t = threading.Thread(target=gioco) #threading per non bloccare l'interfaccia grafica, il thread ha un target che è la funzione gioco()
    t.start() #avvio del thread

def gioco():
    preparazione() #Il conto alla rovescia e spam del mio nickname di qualche riga fa
    global buco 
    for _ in range(80): #80 talpe da colpire, il cilco for è di 80 giri. _ sarebbe il nome perchè tanto non verrà usato da nulla. range è da 0 a 79
        buco = random.randint(1, 9) #buco sarebbe l'indice della posizione randomica della talpa
        bottoni[buco - 1].config(text='O', state='normal', bg='#9E4400', fg='white')
        sleep(1) #pausa prima di nascondere la talpa
        bottoni[buco - 1].config(state='disabled', text='', bg='#009e18')
    bottone_riprova.config(state='normal') #normal per abilitare il bottone di riprova (inizialmente disabilitato)
    valutazione()


dimensione_bottone = 6
bottoni = [] #lista di bottoni, inizialmente vuota ovviamente
for i in range(9):
    btn = Button(width=dimensione_bottone, height=3, bg='#009e18', state='disabled', command=colpisci) #inizialmente sonoi disabilitati, poi abilitati da gioco(). ma se abilitati e poi cliccati, richiamano colpisci()
    btn.place(x=20 + (i % 3) * 150, y=160 + (i // 3) * 130) 
    #EPICO RAGIONAMENTO INCREDIBILEEE:
    #posizionamento dei bottoni, è in un ciclo di 9 giri, quindi 3x3, con (i % 3) che divide l'indice e può essere 0, 1 o 2 (cioè il resto). 
    #Lo stesso anche per (i // 3) che divide l'indice e può essere 0, 1 o 2 (cioè la parte intera). 
    #Le moltiplicazioni (150 e 130) sono per la distanza tra i bottoni.
    #20 e 160 sono le coordinate iniziali, per non farli partire da 0,0.
    bottoni.append(btn) #aggiungo il bottone alla lista

# Bottone per riavviare
bottone_riprova = Button(text="Gioca di nuovo", command=avvia, font=("Arial", 10, "bold"), bg='#777777', fg='white') #In tutto questo, fg sarebbe il foreground, cioè il colore del testo
bottone_riprova.place(x=390, y=470) 

#--------------gestione avvio----------------
avvia() #Il primo avvia() per iniziare il gioco, poi il bottone_riprova si occuperà di chiamare avvia() per ricominciare il gioco (senza farlo in automatico)

finestra.mainloop() #il classico mainloop() per far partire la finestra e il gioco

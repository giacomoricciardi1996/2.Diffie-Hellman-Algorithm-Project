from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pickle
import os
import sys
import random
import datetime

lingua = 0
def azzera_lingua():
    global lingua
    lingua = 0

def aumenta_lingua():
    global lingua
    lingua += 1
    
lista = []
def MCD(a, b):
    while b:
        a, b = b, a%b
    return a

def righe_file_primi():
    righe = 0
    primi = open("primi.txt","r")
    testo = ""
    while (testo != "EOF"):
        testo = primi.readline()
        righe = righe + 1
    primi.close()
    return (righe - 3) 

def generazione_chiavi():
    chiavi = []
    random.seed()
    a = random.randint(0, righe_file_primi())
    b = a
    while (b == a):
        b = random.randint(0, righe_file_primi())

    primi = open("primi.txt","r")
    content = primi.readlines()
    content[a] = content[a].rstrip('\n')
    content[b] = content[b].rstrip('\n')
    chiavi.append(int(float(content[a])))
    chiavi.append(int(float(content[b])))
    chiavi.append(int(float(content[righe_file_primi()+1])))
    primi.close()
    return chiavi

def apri_file_cripta():
    finestra.geometry("650x500")
    #Pulitura schermo
    mess_start.grid_remove()
    mess_diffie.grid_remove()
    mess_limite_sinistro.grid_remove()
    mess_limite_destro.grid_remove()
    limitesinistro.grid_remove()
    limitedestro.grid_remove()
    setlimits.grid_remove()
    separatori.grid_remove()
    mess_separatori.grid_remove()
    translate.grid_remove()
    riga0.grid_remove()
    riga2.grid_remove()
    label.grid_remove()
    label2.grid_remove()
    label3.grid_remove()
    #Messaggio di wait
    mess_wait.grid(row = 0,column = 0)
    
    #Selezionare il file
    filename = filedialog.askopenfile().name

    #Legge tutto il file
    with open(filename, errors = 'ignore') as file:
        content = file.readlines()
    
    #Generazione delle chiavi
    p = generazione_chiavi()[0]
    q = generazione_chiavi()[1]
    n_separatori = generazione_chiavi()[2]
                  
    n = p * q
    x = (p-1)*(q-1)
    
    indice2 = 1
    for indice2 in range(x):
        if ((indice2 != p) and (indice2 != q) and (indice2 != (x-1)) and (MCD(x,indice2) == 1)):
            e = indice2
    
    i = -1
    while ((i*x+1)%e) != 0:
        if ((i*x+1)%e) != 0:
            i = i + 1
    d = (int) ((i*x+1) / e)
    
    #print("Esponenete pubblico e: ",e)
    #print("Esponenete privato d: ",d)
    #print ('Chiave pubblica: (',e,',',n,')')
    #print ('Chiave privata: (',d,',',n,')')

    caratteri = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",">","<","?","!",",",".","-","_",";",":","à","ò","è","ì","ù",")","(","%","$","£","'","ç","°","§","*","+","[","]","{","}"]
    stringa = ""
    separatore = ""
    finale = 0
    
    #Creazione del file e salvataggio dei dati del criptaggio del file selezionato: |percorsofile|data|d|n|
    presente = 0
    try:
        archivio = open("Archivio.txt","r")
        with open("Archivio.txt") as file2:
            content2 = file2.readlines()
            
        data = datetime.datetime.now()
        for i in range(len(content2)):
            content2[i] = content2[i].rstrip('\n')
            if (content2[i] == filename):
                presente = 1
        archivio.close()
        
        if (presente == 0):
            data = datetime.datetime.now()
            archivio = open("Archivio.txt","a")
            archivio.write(filename + "\n")
            archivio.write(str(data) + "\n")
            archivio.write(str(d) + "\n")
            archivio.write(str(n) + "\n")
            archivio.close()
    except (IOError, OSError):
        data = datetime.datetime.now()
        archivio = open("Archivio.txt","w")
        archivio.write(filename + "\n")
        archivio.write(str(data) + "\n")
        archivio.write(str(d) + "\n")
        archivio.write(str(n) + "\n")
        archivio.close()

    if (presente == 0):
        for i in range(len(content)):
            content[i] = content[i].rstrip('\n')
            b = [ord(c) for c in content[i]]
            for x in range(len(content[i])):
                finale = (b[x]**e)%n
                print ("b[x]",b[x])
                print ("finale",finale)
                if (x == (len(content[i]) - 1)):
                    stringa = stringa + (str(finale) + "\n")
                else:
                    lung = random.randint(1, n_separatori)
                    for y in range(lung):    
                        cas = random.randint(0, (len(caratteri)-1))
                        separatore = separatore + caratteri[cas]
                    stringa = stringa + (str(finale) + separatore)
                    separatore = ""
                finale2 = (finale**d)%n
                print ("finale2",finale2)
                
            print (stringa)
            lista.append(stringa)
            stringa = ""
            
        #archivio = open("Archivio.txt","a")
        #archivio.write(filename + "\n")
        #archivio.write(str(data) + "\n")
        #archivio.write(str(d) + "\n")
        #archivio.write(str(n) + "\n")
        #archivio.close()
        
        #Posizionamento
        mess_wait.grid_remove()
        mess_open.grid(row = 0,column = 0)
        save.grid(row = 1,column = 0)
    else:
        mess_wait.grid_remove()
        messagebox.showerror(title = "ERROR", message = "THIS FILE HAS ALREADY BEEN ENCRYPTED!")
    
def salva_file():
    percorso = filedialog.asksaveasfile().name
    nuovo_file = open(percorso,"w")
    for i in range(len(lista)):
        nuovo_file.write(lista[i])
    nuovo_file.close()

    archivio = open("Archivio.txt","a")
    archivio.write(percorso + "\n")
    archivio.write("???\n")
    archivio.close()
        
def apri_file_decripta():
    finestra.geometry("650x500")
    #Pulitura schermo
    mess_start.grid_remove()
    mess_diffie.grid_remove()
    mess_limite_sinistro.grid_remove()
    mess_limite_destro.grid_remove()
    separatori.grid_remove()
    mess_separatori.grid_remove()
    limitesinistro.grid_remove()
    limitedestro.grid_remove()
    setlimits.grid_remove()
    mess_open.grid_remove()
    save.grid_remove()
    translate.grid_remove()
    riga0.grid_remove()
    riga2.grid_remove()
    label.grid_remove()
    label2.grid_remove()
    label3.grid_remove()

    #Selezionare il file
    filename = filedialog.askopenfile().name
    with open(filename, errors = 'ignore') as file:
        content = file.readlines()
    
    with open("Archivio.txt") as file2:
        content2 = file2.readlines()

    #Recuperate le chiavi d e n    
    d = 0
    n = 0
    percorso_vecchio = ""
    for i in range(len(content2)):
        content2[i] = content2[i].rstrip('\n')
        n_registrazioni = int(len(content2) / 5)
        cont = 4
        for x in range(n_registrazioni):
            if (content2[cont] == filename):
                d = int(content2[cont-2])
                n = int(content2[cont-1])
                break
            else:
                cont = cont + 6
    
    
    #Riarrangiamento del file ed eliminazione caratteri inutili
    numero = ""
    lista2 = []
    lista1 = []
    for i in range(len(content)): 
        for x in range(len(content[i])):
            carattere = content[i][x]
            while ((carattere == "0") or (carattere == "1") or (carattere == "2") or (carattere == "3") or (carattere == "4") or (carattere == "5") or (carattere == "6") or (carattere == "7") or (carattere == "8") or (carattere == "9")):
                numero = numero + carattere
                break
            if ((carattere != "0") and (carattere != "1") and (carattere != "2") and (carattere != "3") and (carattere != "4") and (carattere != "5") and (carattere != "6") and (carattere != "7") and (carattere != "8") and (carattere != "9")):
                if (numero != ''):
                    lista2.append(int(numero))
                numero = ""
        lista1.append(lista2)
        lista2 = []
        numero = ""

    nome = os.path.split(filename)
    
    base1 = os.path.basename(nome[1])  #solo nome + estensione
    base=base1[:(len(base1)-4)]  #solo nome (ho dovuto tagliarlo)
    f,ext=os.path.splitext(filename)  #con ext ho solo l'estensione (con f tutto il file)
    
    nuovo_nome = f + "_decrypted" + ext
    print (nuovo_nome)
    
    decriptato = open(nuovo_nome,"a")
    lista3 = []
    for h in lista1:
        for t in h:
            finale2 = (t**d)%n
            lista3.append(finale2)
        s = "".join([chr(c) for c in lista3])
        lista3 = []
        decriptato.write(s + "\n")
    decriptato.close()

    nome_visualizzato = os.path.split(nuovo_nome)
    messagebox.showinfo(title = "NEW DECRYPTED FILE CRETED", message = (nome_visualizzato[1] + " has been created!!!"))
    
def chiavi():
    finestra.geometry("650x500")
    #Pulitura schermo
    mess_start.grid_remove()
    mess_open.grid_remove()
    save.grid_remove()
    translate.grid_remove()
    riga0.grid_remove()
    riga2.grid_remove()
    label.grid_remove()
    label2.grid_remove()
    label3.grid_remove()
    
    #Posizionamento
    mess_diffie.grid(row = 0,column = 0)
    mess_limite_sinistro.grid(row = 1,column = 0)
    mess_limite_destro.grid(row = 2,column = 0)
    mess_separatori.grid(row = 3,column = 0)
    separatori.grid(row = 3,column = 1)
    limitesinistro.grid(row = 1,column = 1)
    limitedestro.grid(row = 2,column = 1)
    setlimits.grid(row = 4,column = 1)

def setta_chiavi():
    primi = open("primi.txt","w")
    limite_sinistro = int(limitesinistro.get("1.0",END))
    limite_destro = int(limitedestro.get("1.0",END))
    sep = int(separatori.get("1.0",END))
    if ((limite_sinistro < limite_destro) and (limite_destro >= 1) and (limite_sinistro > 0)):
        primo = 0
        for n in range(limite_sinistro,limite_destro):
            for d in range(2,n+1):
                primo = 1
                if ((n % d) == 0) and (n != d):
                    primo = 0
                    break
            if (primo):
                num = repr(n)
                num = num + "\n"
                primi.write(num)
        primi.write(str(sep) + "\n")
        primi.write("EOF")
        primi.close()

        messagebox.showinfo(title = "SET LIMITS", message = "RIGHT AND LEFT LIMITS SET PROPERLY!")
        mess_diffie.grid_remove()
        mess_limite_sinistro.grid_remove()
        mess_limite_destro.grid_remove()
        mess_separatori.grid_remove()
        limitesinistro.grid_remove()
        limitedestro.grid_remove()
        setlimits.grid_remove()
        separatori.grid_remove()
    else:
        messagebox.showerror(title = "ERROR", message = "LEFT LIMIT LESS THAN THE RIGHT ONE OR ZERO INSERTED!")
        limitedestro.delete("1.0",END)
        limitesinistro.delete("1.0",END)

def informazioni():
    finestra.geometry("900x500")
    #Pulitura schermo
    mess_start.grid_remove()
    mess_diffie.grid_remove()
    mess_limite_sinistro.grid_remove()
    mess_limite_destro.grid_remove()
    separatori.grid_remove()
    mess_separatori.grid_remove()
    limitesinistro.grid_remove()
    limitedestro.grid_remove()
    setlimits.grid_remove()
    mess_open.grid_remove()
    save.grid_remove()
    
    translate.grid(row = 3,column = 0)
    riga0.grid(row = 0,column = 0)
    riga2.grid(row = 1,column = 0)
    label.grid(row = 1, column = 1)
    label2.grid(row = 1,column = 2)
    label3.grid(row = 2,column = 0)
    
def traduci():
    if (lingua == 0):
        riga2.grid_remove()
        riga1.grid(row = 1,column = 0)
        aumenta_lingua()
    else:
        riga1.grid_remove()
        riga2.grid(row = 1,column = 0)
        azzera_lingua()
def uscita():
    risposta = messagebox.askokcancel(title = "Exit", message = "Are you really sure you want to quit?")
    if (risposta):
        finestra.destroy()

#Creazione della finestra        
finestra = Tk()
finestra.geometry("650x500")
finestra.title("DIFFIE HELMANN ALGORITHM ENCRYPTION")
finestra.configure(bg = 'cyan')
finestra.resizable(False,False)

#Creazione della pagina iniziale
mess_start = Message(finestra,aspect = 1500)
mess_start["text"] = "WELCOME TO THE DIFFIE HELLMAN ALGORITHM ENCRYPTION PROGRAM!!!"
mess_start["bg"] = "cyan"
mess_start["font"] = "Verdena 12 bold"
mess_start["fg"] = "red"
mess_start.grid(row = 0,column = 0)

##crypt = Button(finestra)
##crypt["text"] = "OPEN A FILE AND CRYPT IT"
##crypt["bg"] = "yellow"
##crypt["font"] = "Verdena 10 bold"
##crypt["command"] = apri_file_cripta
##crypt.grid(row = 1,column = 0)
##
##decrypta = Button(finestra)
##decrypta["text"] = "OPEN A FILE AND DECRYPT IT"
##decrypta["bg"] = "yellow"
##decrypta["font"] = "Verdena 10 bold"
##decrypta["command"] = apri_file_decripta
##decrypta.grid(row = 3,column = 0)

#Creazione del menu con aggiunta delle opzioni
barra_menu = Menu(finestra)
menu_file = Menu(barra_menu, tearoff = 0)
barra_menu.add_cascade(label = "File", menu = menu_file)
menu_file.add_command(label = "Open & Encrypt", command = apri_file_cripta)
menu_file.add_command(label = "Open & Decrypt", command = apri_file_decripta)
menu_file.add_command(label = "Diffie Hellman Settings", command = chiavi)
menu_file.add_command(label = "About Diffie Helmann", command = informazioni)
menu_file.add_command(label = "Exit", command = uscita)

#Creazione pagina: Diffie Holmann Settings
limitesinistro = Text(finestra,height = 1,width = 20)
limitedestro = Text(finestra,height = 1,width = 20)
separatori = Text(finestra,height = 1,width = 20)

mess_diffie = Message(finestra,aspect = 700)
mess_diffie["text"] = "DIFFIE HELLMAN ALGORITHM SETTINGS"
mess_diffie["fg"] = "red"
mess_diffie["bg"] = "cyan"

mess_limite_sinistro = Message(finestra,aspect = 1200)
mess_limite_sinistro["text"] = "Insert LEFT limit of the primary numbers to generate:"
mess_limite_sinistro["bg"] = "cyan"

mess_limite_destro = Message(finestra,aspect = 1200)
mess_limite_destro["text"] = "Insert RIGHT limit of the primary numbers to generate:"
mess_limite_destro["bg"] = "cyan"

mess_separatori = Message(finestra,aspect = 800)
mess_separatori["text"] = "Insert how many separator character you want to generate: (ADVICE: Don't insert too big numbers. 2/3 it's perfect)"
mess_separatori["bg"] = "cyan"

mess_diffie = Message(finestra,aspect = 1200)
mess_diffie["text"] = "DIFFIE HELLMAN ALGORITHM SETTINGS"
mess_diffie["font"] = "Verdena 12 bold"
mess_diffie["fg"] = "red"
mess_diffie["bg"] = "cyan"

setlimits = Button(finestra)
setlimits["text"] = "SET LIMITS"
setlimits["bg"] = "red"
setlimits["command"] = setta_chiavi

#Creazione pagina: Open & Encrypt
mess_open = Message(finestra,aspect = 700)
mess_open["text"] = "FILE PROPERLY ENCRYPTED!!!"
mess_open["font"] = "Verdena 12 bold"
mess_open["fg"] = "red"
mess_open["bg"] = "cyan"

save = Button(finestra)
save["text"] = "SAVE FILE AS"
save["bg"] = "red"
save["font"] = "Verdena 12 bold"
save["command"] = salva_file

mess_wait = Message(finestra,aspect = 1000)
mess_wait["text"] = "WAIT A FEW MINUTES, ENCRYPTION IN PROGRESS..."
mess_wait["font"] = "Verdena 12 bold"
mess_wait["fg"] = "blue"
mess_wait["bg"] = "cyan"

#Creazione pagina informazioni
riga0 = Message(finestra,aspect = 900)
riga0["text"] = "HISTORY AND GENERAL INFORMATION\n"
riga0["font"] = "Verdena 14 bold"
riga0["fg"] = "red"
riga0["bg"] = "cyan"

riga1 = Message(finestra,aspect = 350)
riga1["text"] = "Lo schema del protocollo Diffie-Hellman fu pubblicato per la prima volta nel 1976 nell'ambito di una collaborazione tra Whitfield Diffie e Martin Hellman e fu il primo metodo pratico per due interlocutori di accordarsi su un segreto condiviso (la chiave) utilizzando un canale di comunicazione non protetto.Lo scambio di chiavi Diffie-Hellman (Diffie-Hellman key exchange) è un protocollo crittografico che consente a due entità di stabilire una chiave condivisa e segreta utilizzando un canale di comunicazione insicuro (pubblico) senza la necessità che le due parti si siano scambiate informazioni o si siano incontrate in precedenza. La chiave ottenuta mediante questo protocollo può essere successivamente impiegata per cifrare le comunicazioni successive tramite uno schema di crittografia simmetrica.Sebbene l'algoritmo in sé sia anonimo (cioè non autenticato) è alla base di numerosi protocolli autenticati ed è usato anche in alcune modalità di funzionamento del protocollo TLS. E' anche alla base del protocollo S/MIME, utile per la gestione della sicurezza nelle mail."
riga1["font"] = "Verdena 10 bold"
riga1["bg"] = "cyan"

riga2 = Message(finestra,aspect = 350)
riga2["text"] = "The scheme was first published by Whitfield Diffie and Martin Hellman in 1976.Diffie–Hellman key exchange (D–H) is a specific method of securely exchanging cryptographic keys over a public channel and was one of the first public-key protocols as originally conceptualized by Ralph Merkle.D–H is one of the earliest practical examples of public key exchange implemented within the field of cryptography. The Diffie–Hellman key exchange method allows two parties that have no prior knowledge of each other to jointly establish a shared secret key over an insecure channel. This key can then be used to encrypt subsequent communications using a symmetric key cipher.It's also importante for the protocol S/MIME, used to ensure the mail's safety.\n"
riga2["font"] = "Verdena 10 bold"
riga2["bg"] = "cyan"

translate = Button(finestra)
translate["text"] = "TRANSLATE"
translate["bg"] = "orange"
translate["font"] = "Verdena 10 bold"
translate["command"] = traduci

path = "diffie.png"
photo = PhotoImage(file = path)
label = Label(image = photo)
label.image = photo

path2 = "helmann.png"
photo2 = PhotoImage(file = path2)
label2 = Label(image = photo2)
label2.image = photo2

path3 = "images.png"
photo3 = PhotoImage(file = path3)
label3 = Label(image = photo3)
label3.image = photo3

#Assegnazione della barra del menu alla finestra
finestra.config(menu = barra_menu)

finestra.mainloop()

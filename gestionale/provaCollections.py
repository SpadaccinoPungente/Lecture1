import copy
from collections import Counter, deque # Aggiunto deque dai tuoi appunti

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord
from gestionale.vendite.ordini import Ordine

# --- LISTE ---
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20.0)
p3 = ProdottoRecord("Auricolari", 250.0)

# Se creo un oggetto direttamente internamente alla lista sarà "senza nome proprio" (anonimo)
carrello = [p1, p2, p3, ProdottoRecord("Tablet", 700.0)]

print("Prodotti nel carrello:")
# enumerate() prende una lista e restituisce una tupla ad ogni iterazione: (indice, oggetto)
for i, p in enumerate(carrello):
    print(f"{i}) {p.name} - {p.prezzo_unitario}")

print("=" * 60)

# Aggiungere a una lista
carrello.append(ProdottoRecord("Monitor", 150.0))

# Sorting personalizzato tramite funzione lambda (Ordiniamo per prezzo CRESCENTE - dai tuoi appunti)
carrello.sort(key=lambda x: x.prezzo_unitario)

print("Prodotti nel carrello (ordinati per prezzo crescente):")
for i, p in enumerate(carrello):
    print(f"{i}) {p.name} - {p.prezzo_unitario}")

print("=" * 60)

# Ordinamento per prezzo DECRESCENTE (aggiunta del reverse=True - dal codice del prof)
carrello.sort(key=lambda x: x.prezzo_unitario, reverse=True)

print("Prodotti nel carrello (ordinati per prezzo decrescente):")
for i, p in enumerate(carrello):
    print(f"{i}) {p.name} - {p.prezzo_unitario}")

print("=" * 60)

# Totale carrello
tot = sum(p.prezzo_unitario for p in carrello)
print(f"Totale del carrello: {tot}")

print("=" * 60)

# --- METODI VARI PER LE LISTE ---
# Aggiungere
carrello.append(ProdottoRecord("Propdo", 100.0))
carrello.extend([ProdottoRecord("aaa", 100.0), ProdottoRecord("bbb", 100.0)])
carrello.insert(2, ProdottoRecord("ccc", 100.0))

# Rimuovere
carrello.pop() # Rimuove SOLO l'ultimo elemento
carrello.pop(2) # Ammette argomento con l'indice da rimuovere (es. elemento in posizione 2)
carrello.remove(p1) # Elimina la PRIMA occorrenza di p1 (solleva ValueError se non esiste)
# carrello.clear() # Svuota completamente la lista

# Sorting (Attenzione: manca metodo __lt__() base, quindi sort() naturale non funziona al momento)
# carrello.sort() # Utilizza l'ordinamento naturale degli oggetti
# carrello.sort(reverse=True) # Ordina al contrario
# carrello.sort(key = someFunction)
# carrello_ordinato = sorted(carrello) # Prende carrello, lo riordina senza modificare l'originale e lo salva in una nuova lista

# Copie ed altro
carrello.reverse() # Inverte l'ordine
carrello_copia = carrello.copy() # SHALLOW COPY: copia la lista, ma gli oggetti dentro sono gli stessi. Modifiche agli oggetti si riflettono sull'originale.
carrello_copia2 = copy.deepcopy(carrello) # DEEP COPY: copia sia la lista che gli oggetti contenuti. Sono completamente indipendenti.

# --- TUPLE ---
sede_principale = (45, 8) # Lat e long della sede di Torino
sede_milano = (45, 9) # Lat e long della sede di Milano

print(f"Sede principale lat: {sede_principale[0]}, long: {sede_principale[1]}")
print(f"Sede Milano lat: {sede_milano[0]}, long: {sede_milano[1]}")

AliquoteIVA = (
    ("Standard", 0.22),
    ("Ridotta", 0.10),
    ("Alimentari", 0.04),
    ("Esente", 0.0)
)

print("=" * 60)
for descr, valore in AliquoteIVA:
    print(f"{descr}: {valore*100}%")
print("=" * 60)


def calcola_statistiche_carrello(carr):
    """Restituisce prezzo totale, prezzo medio, massimo e minimo"""
    prezzi = [p.prezzo_unitario for p in carr]
    return (sum(prezzi), sum(prezzi)/len(prezzi), max(prezzi), min(prezzi))

# Unpacking (funziona solo se a sinistra ho lo stesso numero di elementi che la funzione restituisce)
tot, media, massimo, minimo = calcola_statistiche_carrello(carrello)

# Unpacking con l'asterisco: il primo valore va in 'other_tot', tutto il resto finisce in una lista chiamata 'altri_campi'
other_tot, *altri_campi = calcola_statistiche_carrello(carrello)
print(f"Totale spacchettato: {other_tot}")


# --- SET (INSIEMI) ---
categorie = {"Gold", "Silver", "Bronze", "Gold"} # Non considera i duplicati (memorizza solo istanze distinte)
print(categorie)
print(len(categorie))

categorie2 = {"Platinum", "Elite", "Gold"}

# Unione
# categorie_all = categorie.union(categorie2) # Equivalente a |
categorie_all = categorie | categorie2
print(categorie_all)

# Intersezione (solo elementi comuni)
categorie_comuni = categorie & categorie2
print(categorie_comuni)

# Differenza (elementi presenti in 'categorie' ma NON in 'categorie2')
categorie_esclusive = categorie - categorie2
print(categorie_esclusive)

# Differenza simmetrica (solo elementi presenti in uno O nell'altro, ma NON in entrambi)
categorie_esclusive_symm = categorie ^ categorie2
print(categorie_esclusive_symm)

prodotti_ordine_A = {
    ProdottoRecord("Laptop", 1200),
    ProdottoRecord("Mouse", 20),
    ProdottoRecord("Tablet", 700)
}

prodotti_ordine_B = {
    ProdottoRecord("Laptop2", 1200),
    ProdottoRecord("Mouse2", 20),
    ProdottoRecord("Tablet", 700)
}

# Metodi utili per i set
s = set()
s1 = set()

# Aggiungere
s.add(ProdottoRecord("aaa", 20.0)) # Aggiunge un singolo elemento
s.update([ProdottoRecord("aaa", 20.0), ProdottoRecord("bbb", 20.0)]) # Aggiunge più elementi passando un iterabile (es. lista)

# Togliere
# s.remove(elem) # Rimuove un elemento. Raise KeyError se non esiste (come nei dict).
# s.discard(elem) # Rimuove un elemento senza "arrabbiarsi" (non dà errore) se questo non esiste.
s.pop() # Rimuove e restituisce un elemento casuale (i set non sono ordinati).
s.clear()

# Operazioni insiemistiche tramite metodi (alternative agli operatori |, &, -, ^)
s.union(s1) # Genera un set che unisce i due set
s.intersection(s1) # Dà solo gli elementi comuni
s.difference(s1) # Elementi di s che non sono contenuti in s1
s.symmetric_difference(s1) # Elementi esclusivi dell'uno o dell'altro

s1.issubset(s) # True se gli elementi di s1 sono interamente contenuti in s
s1.issuperset(s) # True se gli elementi di s sono interamente contenuti in s1
s1.isdisjoint(s) # True se gli elementi di s e s1 sono tutti diversi tra loro (insiemi disgiunti)


# --- DICTIONARY (DIZIONARI) ---
catalogo = {
    "LAP001": ProdottoRecord("Laptop", 1200),
    "LAP002": ProdottoRecord("Laptop Pro", 2300.0),
    "MAU001": ProdottoRecord("Mouse", 20.0),
    "AUR001": ProdottoRecord("Auricolari", 250.0)
}

cod = "LAP002"
prod = catalogo[cod]
print(f"Il prodotto con codice {cod} è {prod}")

# print(f"Cerco un altro oggetto: {catalogo['NonEsiste']}") # Questo darebbe KeyError

# Il metodo .get() legge senza rischiare KeyError. Se non esiste restituisce None (o il default indicato)
prod1 = catalogo.get("NonEsiste")
if prod1 is None:
    print("Prodotto non trovato")

prod2 = catalogo.get("NonEsiste2", ProdottoRecord("Sconosciuto", 0))
print(prod2)

# Ciclare su un dizionario
keys = list(catalogo.keys())
values = list(catalogo.values())

for k in keys:
    print(k)

for v in values:
    print(v)

for key, val in catalogo.items(): # Restituisce le coppie chiave-valore
    print(f"Cod {key} è associata a: {val}")

# Rimuovere dal dizionario
rimosso = catalogo.pop("LAP002") # Restituisce il valore e lo cancella dal dizionario
print(rimosso)

# Dict comprehension
prezzi = {codice: prod.prezzo_unitario for codice, prod in catalogo.items()}

# --- RECAP DA RICORDARE PER DICT ---
# d[key] = v # scrivo sul dizionario
# v = d[key] # leggere -- restituisce KeyError se non esiste
# v = d.get(key, default) # legge senza rischiare KeyError. Se non esiste rende il default (None se non specificato)
# d.pop(key) # restituisce un valore e lo cancella dal diz
# d.clear() # elimina tutto.
# d.keys() # mi restituisce tutte le chiavi definite nel diz
# d.values() # mi restituisce tutti i valori salvati nel diz
# d.items() # restituisce le coppie (chiave, valore).
# key in d # condizione che verifica se key è presente nel diz


# --- ESERCIZIO LIVE ---
print("\n=== Esercizio live: Scelta della collezione ===")
"""1) Memorizzare una elenco di ordini che dovranno poi essere processati in ordine di arrivo"""
# Collection? Lista
ordini_da_processare = []
o1 = Ordine([], ClienteRecord("Mario Rossi", "mario@polito.it", "Gold"))
o2 = Ordine([], ClienteRecord("Mario Bianchi", "bianchi@polito.it", "Silver"))
o3 = Ordine([], ClienteRecord("Fulvio Rossi", "fulvio@polito.it", "Bronze"))
o4 = Ordine([], ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"))

ordini_da_processare.append((o1, 0))
ordini_da_processare.append((o2, 10))
ordini_da_processare.append((o3, 3))
ordini_da_processare.append((o4, 45))

"""2) Memorizzare i CF dei clienti (univoco)"""
# Collection? Set
codici_fiscali = {"ajnfkefioe231", "ajnsow241", "njknaskm1094", "ajnsow241"}
print(codici_fiscali)

"""3) Creare un database di prodotti che posso cercare con un codice univoco"""
# Collection? Dizionario (Dict)
listino_prodotti = {
    "LAP0001" : ProdottoRecord("Laptop", 1200.0),
    "KEY001" : ProdottoRecord("Keyboard", 20.0)
}

"""4) Memorizzare le coordinate gps della nuova sede di Roma"""
# Collection? Tupla
magazzino_roma = (45, 6)

"""5) Tenere traccia delle categorie di clienti che hanno fatto un ordine in un certo range temporale"""
# Collection? Set
categorie_periodo = set()
categorie_periodo.add("Gold")
categorie_periodo.add("Bronze")

print("=============================================================")

# --- COUNTER (Dalla libreria collections) ---
lista_clienti = [
    ClienteRecord("Mario Rossi", "mario@polito.it", "Gold"),
    ClienteRecord("Mario Bianchi", "bianchi@polito.it", "Silver"),
    ClienteRecord("Fulvio Rossi", "fulvio@polito.it", "Bronze"),
    ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"),
    ClienteRecord("Mario Bianchi", "mario@polito.it", "Gold"),
    ClienteRecord("Giuseppe Averta", "bianchi@polito.it", "Silver"),
    ClienteRecord("Francesca Pistilli", "fulvio@polito.it", "Bronze"),
    ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"),
    ClienteRecord("Fulvio Corno", "carlo@polito.it", "Silver")
]

categorie = [c.categoria for c in lista_clienti]
categorie_counter = Counter(categorie)

print("Distribuzione categorie clienti")
print(categorie_counter)

print("2 Categorie più frequenti")
print(categorie_counter.most_common(2)) # Restituisce gli N elementi più frequenti

print("Totale conteggi:")
print(categorie_counter.total()) # Somma di tutti i conteggi

vendite_gennaio = Counter({"Laptop": 13, "Tablet": 15})
vendite_febbraio = Counter({"Laptop": 3, "Stampante": 1})

# Aggregare informazioni (somma tra Counter)
vendite_bimestre = vendite_gennaio + vendite_febbraio

print(f"Vendite Gennaio: {vendite_gennaio}")
print(f"Vendite Febbraio: {vendite_febbraio}")
print(f"Vendite bimestre (somma): {vendite_bimestre}")

# Fare la differenza
print(f"Differenza di vendite (Gen - Feb): {vendite_gennaio - vendite_febbraio}")

# Modificare il valore on-the-fly
vendite_gennaio["Laptop"] += 4
print(f"Vendite Gennaio aggiornate: {vendite_gennaio}")

# Defaultdicts (Argomento accennato dal prof ma non approfondito)

# --- CODA / DEQUE (Aggiunto dai tuoi appunti) ---
print("\n=== Esempio Coda (Deque) ===")
# Creiamo la coda degli ordini
coda_ordini = deque()

# Arrivano nuovi ordini (Enqueue)
coda_ordini.append({"id": 101, "prodotto": "Pizza Margherita"})
coda_ordini.append({"id": 102, "prodotto": "Birra Ichnusa"})
coda_ordini.append({"id": 103, "prodotto": "Tiramisù"})

print(f"Ordini in attesa: {len(coda_ordini)}")

# Processiamo il primo ordine (Dequeue - FIFO: First In, First Out)
ordine_corrente = coda_ordini.popleft()
print(f"Sto preparando l'ordine: {ordine_corrente['prodotto']}")

# Il prossimo sarà l'ordine 102


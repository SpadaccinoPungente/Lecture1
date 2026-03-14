"""
================================================================================
RECAP LEZIONE 1 (Dagli appunti)
================================================================================
Scriviamo un codice python che modelli un semplice gestionale aziendale.
Dovremo prevedere la possibilità di definire entità che modellano i prodotti,
i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati...

# ESEMPIO SENZA CLASSI:
prodotto1_nome = "Laptop"
prodotto1_prezzo = 1200.0
prodotto1_quantita = 5
valore_magazzino = prodotto1_prezzo * prodotto1_quantita
print(f"Valore totale magazzino : {valore_magazzino}")

# PER CREARE LO STESSO CON MENO RIGHE, FACCIO UNA CLASSE:
class Prodotto:
    aliquota_iva = 0.22 # Variabile di classe (uguale per tutte le istanze)

    def __init__(self, name: str, price: float, quantity: int, supplier = None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.price * self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        return netto * (1 + self.aliquota_iva)

    @classmethod # Lo rende metodo di classe e non d'istanza
    def costruttore_con_quantita_uno(cls, name: str, price: float, supplier: str):
        return cls(name, price, 1, supplier) # cls è il riferimento alla classe

    @staticmethod # Metodo statico: non passo né self nè cls!
    def applica_sconto(prezzo, percentuale):
        return prezzo * (1 - percentuale)

# --- Creazione Cliente ---
class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail
        self.categoria = categoria

    def descrizione(self): # Equivalente a to_string()
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}"
================================================================================
"""

# --- INIZIO SCRIPT PRINCIPALE ---
from gestionale.vendite.ordini import Ordine, RigaOrdine, OrdineConSconto
from gestionale.core.prodotti import Prodotto, crea_prodotto_standard, ProdottoRecord
from gestionale.core.clienti import Cliente, ClienteRecord

# import networkx as nx # Dà errore perché il package non è installato nel nostro ambiente!

"""
# --- NOTE SULLE IMPORTAZIONI ---
# Modi per importare moduli e classi in Python:
# 1) from prodotti import ProdottoScontato
# 2) from prodotti import ProdottoScontato as ps # rinomina la classe (alias)
#    p3 = ps("Auricolari", 230, 1, "ABC", 10)
# 3) import prodotti # mi importa tutto ciò che c'è in prodotti
#    p4 = prodotti.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
# 4) import prodotti as p # posso rinominarlo (alias del modulo intero)
#    p5 = p.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
"""

print("=======================================================")

p1 = Prodotto("Ebook Reader", 120.0, 1, "AAA")
p2 = crea_prodotto_standard("Tablet", 750)

print(p1)
print(p2)

print("=======================================================")

c1 = Cliente("Mario Rossi", "mail@mail.com", "Gold")

print("-------------------------------------------------------------------")

cliente1 = ClienteRecord("Mario Rossi", "mariorossi@example.com", "Gold")
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20)

ordine = Ordine([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1)

# I parametri passati nell'ordine:
ordine_scontato = OrdineConSconto([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1, 0.1)

# La dataclass scrive automaticamente un __repr__ che è quello che viene mostrato quando stampo l'oggetto intero
print(ordine)
print("Numero di righe nell'ordine: ", ordine.numero_righe())
print("Totale netto: ", ordine.totale_netto())
print("Totale lordo (IVA 22%): ", ordine.totale_lordo(0.22))

print(ordine_scontato)
print("Totale netto sconto: ", ordine_scontato.totale_netto())
print("Totale lordo scontato: ", ordine_scontato.totale_lordo(0.22))
# NOTA: totale_lordo() non esiste esplicitamente in OrdineConSconto,
# ma è definito nella classe padre (Ordine) e viene richiamato tramite ereditarietà.

print("-------------------------------------------------------------------")

# --- PROSSIMI PASSI ---
# Codice lungo ma che "fa poco" --> voglio suddividerlo in più file --> uso i moduli!
# Sono collezioni di classi, funzioni, variabili, ...
# È lo stesso modo in cui funzionano le librerie, o moduli tipo dataclass (possono essere propri o pubblici scaricati).

# Da farsi poi (mercoledì 4/3):
# Nel package gestionale, scriviamo un modulo fatture.py che contenga:
# - una classe Fattura che contiene un Ordine, un numero_fattura e una data
# - un metodo genera_fattura() che restituisce una stringa formattata con tutte le info della fattura

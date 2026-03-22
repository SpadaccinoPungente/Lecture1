"""
================================================================================
RECAP LEZIONE 1 (Dagli appunti)
================================================================================
Scriviamo un codice python che modelli un semplice gestionale aziendale.
Dovremo prevedere la possibilità di definire entità che modellano i prodotti,
i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati...

# ESEMPIO PROCEDURALE (SENZA CLASSI):
prodotto1_nome = "Laptop"
prodotto1_prezzo = 1200.0
prodotto1_quantita = 5
valore_magazzino = prodotto1_prezzo * prodotto1_quantita
print(f"Valore totale magazzino: {valore_magazzino}")

# PER CREARE LO STESSO CON MENO RIGHE E PIÙ LOGICA, FACCIO UNA CLASSE:
class Prodotto:
    aliquota_iva = 0.22 # Variabile di classe (uguale per tutte le istanze)

    def __init__(self, name: str, price: float, quantity: int, supplier=None):
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

    @staticmethod # Metodo statico: non passo né self né cls!
    def applica_sconto(prezzo, percentuale):
        return prezzo * (1 - percentuale)

# --- Creazione Cliente ---
class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail
        self.categoria = categoria

    def descrizione(self): # Equivalente a to_string() in altri linguaggi
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}"
================================================================================
"""

# --- INIZIO SCRIPT PRINCIPALE ---
from gestionale.vendite.ordini import Ordine, RigaOrdine, OrdineConSconto
from gestionale.core.prodotti import Prodotto, crea_prodotto_standard, ProdottoRecord
from gestionale.core.clienti import Cliente, ClienteRecord

# import networkx as nx # (Dal codice del prof) Dà errore perché il package non è installato nel nostro ambiente!

"""
# --- NOTE SULLE IMPORTAZIONI ---
# Modi per importare moduli e classi in Python:
# 1) from prodotti import ProdottoScontato
# 2) from prodotti import ProdottoScontato as ps # Rinomina la classe (alias)
#    p3 = ps("Auricolari", 230, 1, "ABC", 10)
# 3) import prodotti # Mi importa tutto ciò che c'è nel modulo 'prodotti'
#    p4 = prodotti.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
# 4) import prodotti as p # Rinomina l'intero modulo (alias del modulo intero)
#    p5 = p.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
"""

print("=" * 60)

# Test creazione prodotti tradizionali
p1 = Prodotto("Ebook Reader", 120.0, 1, "AAA")
p2 = crea_prodotto_standard("Tablet", 750)

print(p1)
print(p2)

print("=" * 60)

# Test creazione cliente tradizionale
c1 = Cliente("Mario Rossi", "mail@mail.com", "Gold")

# Test creazione con Dataclasses (Record)
cliente1 = ClienteRecord("Mario Rossi", "mariorossi@example.com", "Gold")
p_rec_1 = ProdottoRecord("Laptop", 1200.0)
p_rec_2 = ProdottoRecord("Mouse", 20.0)

# Creazione Ordini
ordine = Ordine([RigaOrdine(p_rec_1, 2), RigaOrdine(p_rec_2, 10)], cliente1)
ordine_scontato = OrdineConSconto([RigaOrdine(p_rec_1, 2), RigaOrdine(p_rec_2, 10)], cliente1, 0.1)

print("-" * 60)

# La dataclass scrive automaticamente un metodo __repr__ che formatta l'output quando stampo l'oggetto
print(ordine)
print(f"Numero di righe nell'ordine: {ordine.numero_righe()}")
print(f"Totale netto: {ordine.totale_netto()}")
print(f"Totale lordo (IVA 22%): {ordine.totale_lordo(0.22)}")

print("\n" + "-" * 60 + "\n")

print(ordine_scontato)
print(f"Totale netto sconto: {ordine_scontato.totale_netto()}")
print(f"Totale lordo scontato: {ordine_scontato.totale_lordo(0.22)}")
# NOTA STUDIO: totale_lordo() non esiste esplicitamente in OrdineConSconto,
# ma è definito nella classe padre (Ordine) e viene richiamato grazie all'ereditarietà.

print("\n" + "=" * 60)

# --- PROSSIMI PASSI (Esercizio del Prof per mercoledì 4/3) ---
# Il codice sta diventando lungo --> vogliamo suddividerlo in più file usando i moduli.
#
# OBIETTIVO ESERCIZIO:
# Nel package 'gestionale', creare un modulo 'fatture.py' che contenga:
# 1. Una classe Fattura che contiene un Ordine, un numero_fattura e una data.
# 2. Un metodo genera_fattura() che restituisce una stringa formattata con tutte le info.

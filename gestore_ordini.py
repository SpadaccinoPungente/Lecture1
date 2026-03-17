# scrivere un software gestionale che abbia le seguenti funzionalità:
# 1) supportare l'arrivo e la gestione di ordini
# 1bis) quando arriva un nuovo ordine lo aggiungo a una coda assicurandomi che sia eseguito solo dopo gli altri
# 2) avere delle funzionalità per raccogliere statistiche sugli ordini
# 3) fornire statistiche sulla distribuzione di ordini per categoria di cliente

from collections import deque, Counter, defaultdict

from gestionale.core.clienti import ClienteRecord
from gestionale.vendite.ordini import Ordine


class GestoreOrdini:
    def __init__(self):
        self._ordini_da_processare = deque()
        self._ordini_processati = [] # visto che dopo averli processati non mi interessa più l'ordine
        self._statistiche_prodotti = Counter()
        self._ordini_per_categoria = defaultdict(list)

    # metodo per aggiungere ordini a ordini_da_processare:
    def add_ordine(self, ordine: Ordine):
        self._ordini_da_processare.append(ordine)
        print(f"Ricevuto un nuovo ordine da parte di {ordine.cliente}.")
        print(f"Ordini ancora da evadere: {len(self.ordini_da_processare)}")

    # metodo per leggere il prossimo ordine in coda e gestirlo:
    def processa_prossimo_ordine(self):

        # assicuriamoci che un ordine da processare esista, se sì gestiamo il primo
        if not self._ordini_da_processare:
            print("Non ci sono ordini in coda.")
            return False

        ordine = self._ordini_da_processare.popleft() # logica FIFO

        print(f"Sto processando l'ordine di {ordine.cliente}:")
        print(ordine.riepilogo())

        # per aggiornare statistiche sui prodotti venduti
        # Laptop 10 (+1), Mouse 5 (+2), ...
        for riga in ordine.righe:
            self._statistiche_prodotti[riga.prodotto.name] += riga.quantita

        # raggruppare gli ordini per categoria
        self._ordini_per_categoria[ordine.cliente.categoria].append(ordine)

        # archiviamo l'ordine
        self._ordini_processati.append(ordine)

        print("Ordine correttamente processato.")
        return True

    def processa_tutti_ordini(self):
        # processa tutti gli ordini attualmente presenti in coda

        print(f"Processando {len(self._ordini_da_processare)} ordini.")

        while self._ordini_da_processare: # finché ci sono ordini da gestire
            self.processa_prossimo_ordine() # gestisci il successivo

        print("Tutti gli ordini sono stati processati.")

    def get_statistiche_prodotti(self, top_n: int = 5):
        # questo metodo restituisce info sui prodotti più venduti
        valori = []
        for prodotto, quantita in self._statistiche_prodotti.most_common(top_n): # valori più comuni del contatore
            # potrei accedere da fuori e fare most_common() da là, ma così ottengo un migliore incapsulamento delle
            # informazioni (accedo alle statistiche solo da dentro la classe
            valori.append((prodotto, quantita)) # lista di tuple
        return valori

    def get_distribuzione_categorie(self):
        # questo metodo restituisce info sul totale fatturato per ogni categoria presente
        valori = []
        for cat in self._ordini_per_categoria.keys(): # cicla sulle chiavi del defaultdict
            ordini = self._ordini_per_categoria[cat] # recupera la lista degli ordini effettuati
            totale_fatturato = sum([o.totale_lordo(0.22) for o in ordini]) # calcola il totale lordo e lo somma
            valori.append((cat, totale_fatturato)) # lo aggiunge a una lista e lo ritorna
        return valori

    def stampa_riepilogo(self):
        # stampa info di massima
        print("\n" + "=" * 60)
        print("Stato attuale del business: ")
        print(f"Ordini correttamente gestiti: {len(self._ordini_processati)}")
        print(f"Ordini in coda: {len(self._ordini_da_processare)}")

        print("Prodotti più venduti:")
        for prod, quantita in self.get_statistiche_prodotti():
            print(f"{prod}: {quantita}")

        print(f"Fatturato per categoria:")
        for cat, fatturato in self.get_distribuzione_categorie():
            print(f"{cat}: {fatturato}")

def test_modulo():
    # copiare da repo
    pass

if __name__ == "__main__":
    test_modulo()
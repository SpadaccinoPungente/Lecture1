"""
Scrivere un software gestionale che abbia le seguenti funzionalità:
1) Supportare l'arrivo e la gestione di ordini.
1bis) Quando arriva un nuovo ordine, lo aggiungo ad una coda,
      assicurandomi che sia eseguito solo dopo gli altri (FIFO).
2) Avere delle funzionalità per raccogliere statistiche sugli ordini.
3) Fornire statistiche sulla distribuzione di ordini per categoria di cliente.
"""
from collections import deque, Counter, defaultdict

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord
from gestionale.vendite.ordini import Ordine, RigaOrdine


class GestoreOrdini:

    def __init__(self):
        # Utilizziamo deque per la coda FIFO degli ordini in arrivo
        self._ordini_da_processare = deque()
        # Usiamo una semplice lista per lo storico, visto che dopo averli processati non ci interessa più l'ordine di arrivo
        self._ordini_processati = []
        # Counter è perfetto per tenere i conteggi aggiornati (es. quantità per nome prodotto)
        self._statistiche_prodotti = Counter()
        # defaultdict(list) ci permette di appendere direttamente ordini a una chiave che magari non esiste ancora
        self._ordini_per_categoria = defaultdict(list)

    def add_ordine(self, ordine: Ordine):
        """Aggiunge un nuovo ordine agli elementi da gestire mettendolo in coda."""
        self._ordini_da_processare.append(ordine)
        print(f"Ricevuto un nuovo ordine da parte di {ordine.cliente.nome}.")
        print(f"Ordini ancora da evadere: {len(self._ordini_da_processare)}")

    def crea_ordine(self, nomeP, prezzoP, quantitaP, nomeC, mailC, categoriaC):
        """
        Metodo helper (dal codice del prof): crea rapidamente un Ordine
        composto da una singola riga prodotto e lo restituisce.
        """
        return Ordine([RigaOrdine(ProdottoRecord(nomeP, prezzoP), quantitaP)],
                      ClienteRecord(nomeC, mailC, categoriaC))

    def processa_prossimo_ordine(self):
        """Questo metodo legge il prossimo ordine in coda e lo gestisce seguendo la logica FIFO."""
        print("-" * 60)

        # Assicuriamoci che un ordine da processare esista. Se la coda è vuota, usciamo.
        if not self._ordini_da_processare:
            print("Non ci sono ordini in coda.")
            return False

        # Se esiste, estraiamo il primo in coda (Logica FIFO: First In, First Out)
        ordine = self._ordini_da_processare.popleft()

        print(f"Sto processando l'ordine di {ordine.cliente.nome}:")
        print(ordine.riepilogo())

        # 1. Aggiornare statistiche sui prodotti venduti
        # Es: se la chiave "Laptop" ha già 10, e ne vendiamo 1, fa 10 + 1
        for riga in ordine.righe:
            self._statistiche_prodotti[riga.prodotto.name] += riga.quantita

        # 2. Raggruppare gli ordini per categoria cliente (Gold, Silver, ecc.)
        self._ordini_per_categoria[ordine.cliente.categoria].append(ordine)

        # 3. Archiviamo l'ordine spostandolo nello storico
        self._ordini_processati.append(ordine)

        print("Ordine correttamente processato.")
        return True

    def processa_tutti_ordini(self):
        """Processa in blocco tutti gli ordini attualmente presenti in coda."""
        print("\n" + "=" * 60)
        print(f"Processando {len(self._ordini_da_processare)} ordini...")

        # Un ciclo while su un iterable gira finché questo non diventa vuoto
        while self._ordini_da_processare:
            self.processa_prossimo_ordine()

        print("-" * 60)
        print("Tutti gli ordini sono stati processati.")

    def get_statistiche_prodotti(self, top_n: int = 5):
        """
        Restituisce una lista di tuple con i prodotti più venduti.

        NOTA STUDIO: Potrei accedere a _statistiche_prodotti dall'esterno e chiamare
        most_common() direttamente da là, ma facendolo qui dentro ottengo un migliore
        INCAPSULAMENTO delle informazioni (nascondo i dettagli implementativi).
        """
        valori = []
        for prodotto, quantita in self._statistiche_prodotti.most_common(top_n):
            valori.append((prodotto, quantita))
        return valori

    def get_distribuzione_categorie(self):
        """Restituisce il totale fatturato diviso per ogni categoria di cliente presente."""
        valori = []
        # Ciclo sulle chiavi del defaultdict (es. "Gold", "Silver")
        for cat in self._ordini_per_categoria.keys():
            # Recupero l'intera lista di ordini per quella categoria
            ordini = self._ordini_per_categoria[cat]
            # Uso una list comprehension per calcolare i totali lordi e li sommo
            totale_fatturato = sum([o.totale_lordo(0.22) for o in ordini])

            valori.append((cat, totale_fatturato))
        return valori

    def stampa_riepilogo(self):
        """Stampa le informazioni di massima sullo stato del business."""
        print("\n" + "=" * 60)
        print("STATO ATTUALE DEL BUSINESS")
        print("=" * 60)
        print(f"Ordini correttamente gestiti: {len(self._ordini_processati)}")
        print(f"Ordini in coda: {len(self._ordini_da_processare)}")

        print("\nProdotti più venduti:")
        for prod, quantita in self.get_statistiche_prodotti():
            print(f" - {prod}: {quantita} unità")

        print(f"\nFatturato per categoria:")
        for cat, fatturato in self.get_distribuzione_categorie():
            print(f" - {cat} : € {fatturato:.2f}")


def test_modulo():
    sistema = GestoreOrdini()

    ordini = [
        Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
                RigaOrdine(ProdottoRecord("Mouse", 10.0), 3)],
               ClienteRecord("Mario Rossi", "mario@mail.it", "Gold")),
        Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
                RigaOrdine(ProdottoRecord("Mouse", 10.0), 2),
                RigaOrdine(ProdottoRecord("Tablet", 500.0), 1),
                RigaOrdine(ProdottoRecord("Cuffie", 250.0), 3)],
               ClienteRecord("Fulvio Bianchi", "bianchi@gmail.com", "Gold")),
        Ordine([
            RigaOrdine(ProdottoRecord("Laptop", 1200.0), 2),
            RigaOrdine(ProdottoRecord("Mouse", 10.0), 2)],
            ClienteRecord("Giuseppe Averta", "giuseppe.averta@polito.it", "Silver")),
        Ordine([
            RigaOrdine(ProdottoRecord("Tablet", 900.0), 1),
            RigaOrdine(ProdottoRecord("Cuffie", 250.0), 3)],
            ClienteRecord("Carlo Masone", "carlo@mail.it", "Gold")),
        Ordine([
            RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
            RigaOrdine(ProdottoRecord("Mouse", 10.0), 3)],
            ClienteRecord("Francesca Pistilli", "francesca@gmail.com", "Bronze"))
    ]

    print("--- FASE 1: RICEZIONE ORDINI ---")
    for o in ordini:
        sistema.add_ordine(o)

    print("\n--- FASE 2: ELABORAZIONE ---")
    sistema.processa_tutti_ordini()

    sistema.stampa_riepilogo()


if __name__ == "__main__":
    test_modulo()
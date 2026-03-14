# Scriviamo un codice python che modelli un semplice gestionale aziendale.
# Dovremo prevedere la possibilità di definire entità che modellano i prodotti, i clienti,
# offrire interfacce per calcolare i prezzi, eventualmente scontati, ...

from dataclasses import dataclass
from typing import Protocol  # Spostato in alto: in Python le importazioni vanno sempre a inizio file


class Prodotto:
    # Variabile di classe: è condivisa e uguale per tutte le istanze che verranno create
    aliquota_iva = 0.22

    def __init__(self, name: str, price: float, quantity: int, supplier=None):
        self.name = name
        # Inizializzo a None la variabile "protetta" a cui applicherò i controlli nel setter
        self._price = None
        # Chiamo il setter: così mi assicuro che il prezzo non possa essere negativo già in fase di creazione
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self._price * self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto * (1 + self.aliquota_iva)
        return lordo

    @classmethod
    def costruttore_con_quantita_uno(cls, name: str, price: float, supplier: str):
        # NOTA: Aggiunto il return (assente nel codice originale del prof)
        # altrimenti l'assegnazione a variabili (es. p3) non funzionerebbe!
        return cls(name, price, 1, supplier)

    @staticmethod
    def applica_sconto(prezzo, percentuale):
        return prezzo * (1 - percentuale)

    @property
    def price(self):  # Equivalente a un GETTER
        return self._price

    @price.setter
    # Posso crearlo solo dopo aver definito @property. Si attiva in automatico con: self.price = valore
    def price(self, valore):
        if valore < 0:
            raise ValueError("Attenzione, il prezzo non può essere negativo.")
        self._price = valore

    def __str__(self):
        # Esattamente equivalente al metodo toString() di Java.
        # Se definito, stampando l'oggetto (print) uso direttamente questa formattazione.
        return f"{self.name} - disponibili {self.quantity} pezzi a {self.price} $"

    def __repr__(self):
        # Simile a __str__ ma orientato al programmatore (mostra la struttura dell'oggetto).
        # Viene utilizzato ad es. in debug mode per vedere cosa c'è all'interno delle variabili.
        # Se non è definito, di default si stampa l'indirizzo della cella di memoria dell'oggetto.
        return f"Prodotto(name={self.name}, price={self.price}, quantity={self.quantity}, supplier={self.supplier})"

    def __eq__(self, other: object):
        # Analogo al metodo equals() di Java, permette di confrontare il contenuto delle istanze (implementa l'operatore ==)
        if not isinstance(other, Prodotto):  # Analogo a instanceof di Java
            return NotImplemented
        return (self.name == other.name
                and self.price == other.price
                and self.quantity == other.quantity
                and self.supplier == other.supplier)

    def __lt__(self, other: "Prodotto") -> bool:
        # Analogo a compareTo() di Java (lt = lower than). Implementa l'operatore <.
        # Python deduce in automatico gli altri metodi di confronto (es. >) se necessario.
        # 'other: "Prodotto"': specifica che other debba essere di tipo Prodotto (le "" servono per riferirsi alla classe stessa mentre la si sta definendo).
        # '-> bool': type hinting, anticipa al programmatore/IDE che il valore di ritorno è booleano.
        return self.price < other.price

    def prezzo_finale(self) -> float:
        return self.price * (1 + self.aliquota_iva)


class ProdottoScontato(Prodotto):
    # EREDITARIETÀ -> ProdottoScontato è classe figlia di Prodotto
    # (In Python è possibile l'ereditarietà multipla, ma qui non la usiamo)

    def __init__(self, name: str, price: float, quantity: int, supplier: str, sconto_percento: float):
        # Chiamata al costruttore della classe padre.
        # In alternativa si poteva usare Prodotto.__init__(self, ...), ma super() è più sicuro e moderno.
        super().__init__(name, price, quantity, supplier)
        self.sconto_percento = sconto_percento  # Aggiungo un attributo specifico per la classe figlia

    def prezzo_finale(self) -> float:
        # POLIMORFISMO: stesso nome del metodo della classe padre, ma comportamento diverso!
        return self.valore_lordo() * (1 - self.sconto_percento / 100)


class Servizio(Prodotto):
    # Eredita da prodotto: non è qualcosa di fisico che vendo, ma lo adatto a nuovi obiettivi
    def __init__(self, name: str, tariffa_oraria: float, ore: int):
        super().__init__(name=name, price=tariffa_oraria, quantity=1, supplier=None)
        self.ore = ore

    def prezzo_finale(self) -> float:
        # POLIMORFISMO
        return self.price * self.ore


# Definire una classe Abbonamento che abbia come attributi: nome, prezzo_mensile, mesi
# Abbonamento dovrà avere un metodo per calcolare il prezzo finale ottenuto come prezzo_mensile*mesi
class Abbonamento:
    def __init__(self, nome: str, prezzo_mensile: float, mesi: int):
        self.name = nome
        self.prezzo_mensile = prezzo_mensile
        self.mesi = mesi

    def prezzo_finale(self) -> float:
        return self.prezzo_mensile * self.mesi


@dataclass
# Decoratore che indica che questa classe contiene principalmente dati.
# Genera in automatico __init__, __repr__, __eq__, ecc. "Classe automaticamente civile".
class ProdottoRecord:
    name: str
    prezzo_unitario: float

    def __hash__(self):
        return hash((self.name, self.prezzo_unitario))

    def __str__(self):
        return f"{self.name} -- {self.prezzo_unitario}"


# Dentro il modulo posso avere costanti, metodi, classi, ...
MAX_QUANTITA = 1000


def crea_prodotto_standard(nome: str, prezzo: float):
    # Metodo di factory per la creazione rapida di prodotti base
    return Prodotto(nome, prezzo, 1, None)


def _test_modulo():
    print("Sto testando il modulo prodotti.py\n")

    # --- TEST BASE ---
    myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
    print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")
    print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}")  # Uso un metodo di istanza

    p3 = Prodotto.costruttore_con_quantita_uno("Auricolari", 200.0, "ABC")  # Uso un metodo di CLASSE
    print(f"Prezzo scontato di myproduct1: {Prodotto.applica_sconto(myproduct1.price, 0.15)}")  # Uso un metodo STATICO

    myproduct2 = Prodotto("Mouse", 10, 25, "CDE")

    # Se cambio il valore di una variabile di classe, l'effetto vale per tutte le istanze:
    print(f"Valore lordo pre-modifica IVA: {myproduct1.valore_lordo()}")
    Prodotto.aliquota_iva = 0.24
    print(f"Valore lordo post-modifica IVA: {myproduct1.valore_lordo()}")
    print(myproduct1)

    # --- TEST UGUAGLIANZA E ORDINAMENTO ---
    p_a = Prodotto("Laptop", price=1200.0, quantity=12, supplier="ABC")
    p_b = Prodotto("Mouse", 10, 14, "CDE")

    print("\nmyproduct1 == p_a?", myproduct1 == p_a)  # Chiama __eq__, mi aspetto True
    print("p_a == p_b?", p_a == p_b)  # Chiama __eq__, mi aspetto False

    mylist = [p_a, p_b, myproduct1]
    mylist.sort()  # Utilizza il metodo __lt__ per ordinare
    print("\nLista di prodotti ordinata in ordine crescente (basato su __lt__):")
    for p in mylist:
        print(f"- {p}")

    # --- TEST DUCK TYPING E POLIMORFISMO ---
    print("\n--- TEST DUCK TYPING ---")
    my_product_scontato = ProdottoScontato(name="Auricolari", price=320, quantity=1, supplier="ABC", sconto_percento=10)
    my_service = Servizio(name="Consulenza", tariffa_oraria=100.0, ore=3)

    # Inserisco nella lista elementi non omogenei. In Python è permesso!
    mylist.append(my_product_scontato)
    mylist.append(my_service)

    abb = Abbonamento("Software gestionale", prezzo_mensile=30, mesi=24)
    # L'IDE potrebbe dare un warning perché 'abb' non eredita da 'Prodotto', ma secondo
    # il principio del Duck Typing il codice funzionerà finché l'oggetto ha il metodo richiesto.
    mylist.append(abb)

    # Sort fallirebbe qui se provassimo a riordinare perché Abbonamento non ha __lt__,
    # ma possiamo ciclare e chiamare prezzo_finale() su tutti.
    for elem in mylist:
        print(elem.name, " -> ", elem.prezzo_finale())

    # --- PROTOCOLLI (Interfacce in Python) ---
    # Come ci assicuriamo di comunicare quali metodi ci aspettiamo siano implementati? Usiamo i Protocol.

    class HaPrezzoFinale(Protocol):
        def prezzo_finale(self) -> float:
            ...  # I tre puntini (Ellipsis) fungono da placeholder, simile a 'pass'. Non serve implementarlo qui.

    # Usiamo il protocollo come Type Hinting: array di oggetti che implementano HaPrezzoFinale
    def calcola_totale(elementi: list[HaPrezzoFinale]) -> float:
        # Comprehension per sommare tutto rapidamente
        return sum(e.prezzo_finale() for e in elementi)

    print(f"\nIl totale calcolato tramite funzione con Protocol è: {calcola_totale(mylist)}")


if __name__ == "__main__":
    _test_modulo()  # Eseguo i test solo se il file viene eseguito in maniera standalone
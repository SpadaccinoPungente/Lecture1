# Scriviamo un codice Python che modelli un semplice gestionale aziendale.
# Prevediamo la possibilità di definire entità che modellano i prodotti, i clienti,
# e offriamo interfacce per calcolare i prezzi, eventualmente scontati.

from dataclasses import dataclass
from typing import Protocol  # In Python le importazioni vanno sempre a inizio file


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
        # NOTA STUDIO: Aggiunto il return (assente nel codice originale del prof),
        # altrimenti l'assegnazione a variabili non funzionerebbe e restituirebbe None!
        return cls(name, price, 1, supplier)  # cls è il riferimento alla classe stessa

    @staticmethod
    def applica_sconto(prezzo, percentuale):
        return prezzo * (1 - percentuale)

    @property
    def price(self):  # Equivalente a un GETTER
        return self._price

    @price.setter
    def price(self, valore):
        # Si attiva in automatico ogni volta che faccio: self.price = valore
        if valore < 0:
            raise ValueError("Attenzione, il prezzo non può essere negativo.")
        self._price = valore

    def __str__(self):
        # Esattamente equivalente al metodo toString() di Java.
        # Definisce come l'oggetto viene mostrato quando uso print()
        return f"{self.name} - disponibili {self.quantity} pezzi a {self.price} $"

    def __repr__(self):
        # Simile a __str__ ma orientato al programmatore.
        # Utilizzato in debug per vedere l'esatto stato interno dell'oggetto.
        return f"Prodotto(name={self.name}, price={self.price}, quantity={self.quantity}, supplier={self.supplier})"

    def __eq__(self, other: object):
        # Analogo al metodo equals() di Java. Implementa l'operatore ==
        if not isinstance(other, Prodotto):  # Analogo a instanceof di Java
            return NotImplemented
        return (self.name == other.name
                and self.price == other.price
                and self.quantity == other.quantity
                and self.supplier == other.supplier)

    def __lt__(self, other: "Prodotto") -> bool:
        # Analogo a compareTo() di Java (lt = lower than). Implementa l'operatore <
        # Type hinting 'other: "Prodotto"': le virgolette servono per riferirsi alla classe mentre la si sta ancora definendo
        return self.price < other.price

    def prezzo_finale(self) -> float:
        return self.price * (1 + self.aliquota_iva)


class ProdottoScontato(Prodotto):
    # EREDITARIETÀ -> ProdottoScontato è classe figlia di Prodotto
    def __init__(self, name: str, price: float, quantity: int, supplier: str, sconto_percento: float):
        # super() chiama il costruttore della classe padre in modo sicuro
        super().__init__(name, price, quantity, supplier)
        self.sconto_percento = sconto_percento  # Attributo specifico della classe figlia

    def prezzo_finale(self) -> float:
        # POLIMORFISMO (Overriding): stesso nome del metodo della classe padre, ma comportamento diverso!
        return self.valore_lordo() * (1 - self.sconto_percento / 100)


class Servizio(Prodotto):
    # Eredita da Prodotto: non è un bene fisico, ma sfrutto la struttura base
    def __init__(self, name: str, tariffa_oraria: float, ore: int):
        super().__init__(name=name, price=tariffa_oraria, quantity=1, supplier=None)
        self.ore = ore

    def prezzo_finale(self) -> float:
        # POLIMORFISMO
        return self.price * self.ore


class Abbonamento:
    # Classe indipendente, non eredita da Prodotto
    def __init__(self, nome: str, prezzo_mensile: float, mesi: int):
        self.name = nome
        self.prezzo_mensile = prezzo_mensile
        self.mesi = mesi

    def prezzo_finale(self) -> float:
        return self.prezzo_mensile * self.mesi


@dataclass
class ProdottoRecord:
    # Il decoratore @dataclass genera in automatico __init__, __repr__, __eq__.
    # È perfetto per classi che devono solo contenere dati strutturati.
    name: str
    prezzo_unitario: float

    def __hash__(self):
        return hash((self.name, self.prezzo_unitario))

    def __str__(self):
        return f"{self.name} -- {self.prezzo_unitario}"


MAX_QUANTITA = 1000


def crea_prodotto_standard(nome: str, prezzo: float):
    # Metodo Factory esterno alla classe per la creazione rapida
    return Prodotto(nome, prezzo, 1, None)


def _test_modulo():
    print("=" * 60)
    print("TEST MODULO PRODOTTI.PY")
    print("=" * 60)

    # --- TEST BASE ---
    myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
    print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")

    # Uso un metodo di istanza
    print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}")

    # Uso un metodo di CLASSE
    p3 = Prodotto.costruttore_con_quantita_uno("Auricolari", 200.0, "ABC")

    # Uso un metodo STATICO
    print(f"Prezzo scontato di myproduct1: {Prodotto.applica_sconto(myproduct1.price, 0.15)}")

    myproduct2 = Prodotto("Mouse", 10, 25, "CDE")

    # --- TEST VARIABILI DI CLASSE ---
    print("\n--- Modifica Variabile di Classe (IVA) ---")
    print(f"Valore lordo myproduct1 pre-modifica: {myproduct1.valore_lordo()}")
    Prodotto.aliquota_iva = 0.24  # Cambia per TUTTE le istanze
    print(f"Valore lordo myproduct1 post-modifica: {myproduct1.valore_lordo()}")
    print(myproduct1)

    # --- TEST UGUAGLIANZA E ORDINAMENTO ---
    print("\n--- Test __eq__ e __lt__ ---")
    p_a = Prodotto("Laptop", price=1200.0, quantity=12, supplier="ABC")
    p_b = Prodotto("Mouse", 10, 14, "CDE")

    print(f"myproduct1 == p_a? {myproduct1 == p_a}")  # Chiama __eq__, True
    print(f"p_a == p_b? {p_a == p_b}")  # Chiama __eq__, False

    mylist = [p_a, p_b, myproduct1]

    # Il prof ha aggiunto reverse=True per testare l'ordinamento decrescente
    mylist.sort(reverse=True)
    print("\nLista di prodotti ordinata in ordine decrescente (basato su __lt__):")
    for p in mylist:
        print(f"- {p}")

    # --- TEST DUCK TYPING E POLIMORFISMO (Aggiunta studio) ---
    print("\n" + "=" * 60)
    print("TEST DUCK TYPING E PROTOCOLLI")
    print("=" * 60)

    my_product_scontato = ProdottoScontato(name="Auricolari", price=320, quantity=1, supplier="ABC", sconto_percento=10)
    my_service = Servizio(name="Consulenza", tariffa_oraria=100.0, ore=3)
    abb = Abbonamento("Software gestionale", prezzo_mensile=30, mesi=24)

    # Inserisco nella lista elementi di classi diverse. In Python è permesso!
    elementi_misti = [myproduct1, my_product_scontato, my_service, abb]

    # Abbonamento non eredita da Prodotto, ma per il Duck Typing funzionerà
    # finché l'oggetto ha il metodo "prezzo_finale()" che stiamo chiamando.
    for elem in elementi_misti:
        print(f"{elem.name} -> € {elem.prezzo_finale():.2f}")

    # --- PROTOCOLLI (Interfacce in Python) ---
    class HaPrezzoFinale(Protocol):
        # Dichiaro un'interfaccia: chiunque voglia far parte di questo gruppo DEVE avere questo metodo
        def prezzo_finale(self) -> float:
            ...  # I tre puntini (Ellipsis) fungono da placeholder, simile a 'pass'

    # Usiamo il protocollo come Type Hinting per rendere il codice più robusto
    def calcola_totale(elementi: list[HaPrezzoFinale]) -> float:
        return sum(e.prezzo_finale() for e in elementi)

    print(f"\nIl totale calcolato tramite funzione con Protocol è: € {calcola_totale(elementi_misti):.2f}")


if __name__ == "__main__":
    _test_modulo()  # Eseguo i test solo se il file viene eseguito direttamente
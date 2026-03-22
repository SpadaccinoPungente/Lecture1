from dataclasses import dataclass

"""
--- TESTO DELL'ESERCIZIO ---
Scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze").
Vorremmo che questa classe avesse un metodo che chiamiamo "descrizione" 
che deve restituire una stringa formattata ad esempio:
"Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

Si modifichi la classe cliente in maniera tale che la proprietà categoria sia "protetta"
e accetti solo ("Gold", "Silver", "Bronze")
-----------------------------
"""

# Categorie valide definite a livello di modulo.
# NOTA STUDIO: Questo rappresenta un SET.
# L'uso delle graffe {} senza i ":" crea un Set; se ci fossero i ":" sarebbe un Dizionario.
categorie_valide = {"Gold", "Silver", "Bronze"}


class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail

        # Inizializziamo a None la variabile "protetta" (la convenzione impone l'underscore iniziale)
        self._categoria = None

        # L'assegnazione qui sotto non crea una nuova variabile, ma chiama in automatico
        # il setter definito più in basso, garantendo che il controllo avvenga fin dalla creazione!
        self.categoria = categoria

    @property
    def categoria(self):
        # GETTER: permette di leggere il valore di _categoria dall'esterno
        # nascondendo l'implementazione interna
        return self._categoria

    @categoria.setter
    def categoria(self, categoria):
        # SETTER: convalida l'input prima di permettere l'assegnazione alla proprietà protetta
        if categoria not in categorie_valide:
            raise ValueError("Attenzione, categoria non valida. Scegliere fra Gold, Silver, Bronze")
        self._categoria = categoria

    def descrizione(self):
        # Equivalente a una sorta di to_string() personalizzata
        # Output atteso: "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}"


@dataclass
class ClienteRecord:
    # Le dataclass generano in automatico __init__, __repr__ ecc.,
    # ottime per oggetti che devono solo contenere dati.
    nome: str
    mail: str
    categoria: str

    def __str__(self):
        # Dal codice del prof: possiamo comunque sovrascrivere i metodi magici
        # all'interno di una dataclass se vogliamo un output personalizzato diverso dal __repr__ di default.
        return f"{self.nome} -- {self.mail} ({self.categoria})"


def _test_modulo():
    print("=" * 60)
    print("TEST MODULO CLIENTI")
    print("=" * 60)

    c1 = Cliente("Mario Bianchi", "mario.bianchi@polito.it", "Gold")
    print(c1.descrizione())

    # c2 = Cliente("Carlo Masone", "carlo.masone@polito.it", "Platinum")
    # NOTA STUDIO: Se scommentata, la riga sopra solleverebbe un ValueError
    # perché la categoria "Platinum" non esiste nel Set 'categorie_valide'.


if __name__ == "__main__":
    # Eseguo la funzione di test solo se il file viene eseguito in maniera "standalone" (cioè direttamente).
    # Se questo file venisse importato in un altro script (es. nel main), _test_modulo() NON verrebbe avviata in automatico.
    _test_modulo()
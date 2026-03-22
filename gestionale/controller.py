import flet as ft
from gestionale.gestoreOrdini import GestoreOrdini


class Controller:
    def __init__(self, v):
        self._view = v
        # Il controller inizializza il Model (il "motore" del nostro gestionale)
        self._model = GestoreOrdini()

    # NOTA STUDIO: Tutti i metodi collegati a un evento Flet (come on_click)
    # devono ricevere un parametro 'e' (che sta per "event"), anche se poi non lo usiamo.
    def add_ordine(self, e):

        # 1. Recupero Dati Prodotto
        nomePstr = self._view._txtInNomeP.value

        # VALIDAZIONE: Cerchiamo di convertire il prezzo in un numero.
        # Se l'utente ha scritto "ciao" invece di un numero, la conversione fallisce (ValueError).
        try:
            prezzo = float(self._view._txtInPrezzo.value)
        except ValueError:
            # Stampiamo l'errore in rosso nella ListView e interrompiamo la funzione con 'return'
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! Il prezzo deve essere un numero.", color="red")
            )
            self._view.update_page()
            return

        try:
            quantita = int(self._view._txtInQuantita.value)
        except ValueError:
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! La quantità deve essere un intero.", color="red")
            )
            self._view.update_page()
            return

        # 2. Recupero Dati Cliente
        nomeC = self._view._txtInNomeC.value
        mail = self._view._txtInMail.value
        categoria = self._view._txtInCategoria.value

        # 3. Interazione con il Model
        # Usiamo il metodo "comodo" che avevamo visto nel GestoreOrdini
        ordine = self._model.crea_ordine(nomePstr, prezzo, quantita, nomeC, mail, categoria)
        self._model.add_ordine(ordine)

        # 4. Pulizia dell'interfaccia (svuotiamo i campi di testo dopo l'inserimento)
        self._view._txtInNomeP.value = ""
        self._view._txtInPrezzo.value = ""
        self._view._txtInQuantita.value = ""
        self._view._txtInNomeC.value = ""
        self._view._txtInMail.value = ""
        self._view._txtInCategoria.value = ""

        # 5. Conferma visiva all'utente
        self._view._lvOut.controls.append(
            ft.Text("Ordine correttamente inserito.", color="green")
        )
        self._view._lvOut.controls.append(ft.Text("Dettagli dell'ordine:"))
        self._view._lvOut.controls.append(ft.Text(ordine.riepilogo()))

        # Diciamo alla View di aggiornarsi per mostrare i cambiamenti
        self._view.update_page()

    # --- METODI DA IMPLEMENTARE ---
    def gestisci_ordine(self, e):
        pass

    def gestisci_all_ordini(self, e):
        pass

    def stampa_sommario(self, e):
        pass
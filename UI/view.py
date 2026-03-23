import flet as ft


class View:
    def __init__(self, page):
        self._page = page
        self._controller = None
        # Impostazioni generali della finestra
        self._page.title = "TdP 2025 - Software Gestionale"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self.update_page()
        # In teoria dovremmo definire tutte le variabili di classe qui
        # ma in Python non è necessario

    def carica_interfaccia(self):
        # --- RIGA 1: Dati del Prodotto ---
        self._txtInNomeP = ft.TextField(label="Nome prodotto", width=200)
        self._txtInPrezzo = ft.TextField(label="Prezzo", width=200)
        self._txtInQuantita = ft.TextField(label="Quantità", width=200)

        # Inserisco i 3 campi in una Row (Riga) allineata al centro
        row1 = ft.Row(controls=[self._txtInNomeP, self._txtInPrezzo, self._txtInQuantita],
                      alignment=ft.MainAxisAlignment.CENTER)

        # --- RIGA 2: Dati del Cliente ---
        self._txtInNomeC = ft.TextField(label="Nome Cliente", width=200)
        self._txtInMail = ft.TextField(label="Mail", width=200)
        self._txtInCategoria = ft.TextField(label="Categoria", width=200)

        row2 = ft.Row(controls=[self._txtInNomeC, self._txtInMail, self._txtInCategoria],
                      alignment=ft.MainAxisAlignment.CENTER)

        # --- RIGA 3: Bottoni di azione ---
        # NOTA STUDIO: Il parametro 'on_click' collega il bottone al metodo del Controller.
        # Non stiamo eseguendo la funzione (non ci sono le parentesi ()), la stiamo solo "passando".
        self._btnAdd = ft.ElevatedButton(text="Aggiungi ordine",
                                         on_click=self._controller.add_ordine,
                                         width=200)
        self._btnGestisciOrdine = ft.ElevatedButton(text="Gestisci prox ordine",
                                                    on_click=self._controller.gestisci_ordine,
                                                    width=200)
        self._btnGestisciAllOrdini = ft.ElevatedButton(text="Gestisci tutti gli ordini",
                                                       on_click=self._controller.gestisci_all_ordini,
                                                       width=200)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa sommario",
                                                on_click=self._controller.stampa_sommario,
                                                width=200)

        row3 = ft.Row(controls=[self._btnAdd, self._btnGestisciOrdine,
                                self._btnGestisciAllOrdini, self._btnStampaInfo],
                      alignment=ft.MainAxisAlignment.CENTER)

        # --- ZONA OUTPUT ---
        # ListView funziona come una sorta di console/terminale interno all'app.
        # expand=True le permette di occupare tutto lo spazio verticale rimanente.
        self._lvOut = ft.ListView(expand=True)

        # Aggiungiamo fisicamente tutto alla pagina
        self._page.add(row1, row2, row3, self._lvOut)

    def set_controller(self, c):
        self._controller = c

    def update_page(self):
        """Metodo di comodità per forzare l'aggiornamento visivo della pagina"""
        self._page.update()

import flet as ft

from UI.controller import Controller
from UI.view import View


def main(page: ft.Page):
    # 1. Crea la View (l'interfaccia grafica passandogli la pagina)
    v = View(page)

    # 2. Crea il Controller passandogli la View (così il controller sa chi deve comandare)
    c = Controller(v)

    # 3. Dice alla View chi è il suo Controller (così la View sa a chi inviare i click dei bottoni)
    v.set_controller(c)

    # 4. Disegna effettivamente i bottoni e i campi di testo sullo schermo
    v.carica_interfaccia()


# Lancia l'applicazione Flet indicando 'main' come funzione di partenza
ft.app(target=main)
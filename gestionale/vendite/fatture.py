from dataclasses import dataclass
from datetime import date

from gestionale.core.clienti import Cliente, ClienteRecord
from gestionale.core.prodotti import ProdottoRecord
from gestionale.vendite.ordini import Ordine, RigaOrdine


@dataclass
class Fattura:
    # Uso i doppi apici per "Ordine" come forward reference,
    # nel caso in cui la classe non fosse ancora pienamente caricata
    ordine: "Ordine"
    numero_fattura: str
    data: date

    # --- VERSIONE AVANZATA (Spaziata e allineata meglio) ---
    def genera_fattura(self) -> str:
        """Genera il testo della fattura formattato come un vero scontrino."""

        # Inizializzo una lista di stringhe che poi unirò alla fine
        linee = [
            "=" * 60,
            # .center(60) centra la stringa rispetto alla larghezza di 60 caratteri
            f"FATTURA N. {self.numero_fattura}".center(60),
            f"Data: {self.data.strftime('%d/%m/%Y')}".center(60),
            "=" * 60,
            "",
            # Dettagli del cliente (pescati esplorando l'oggetto Ordine -> Cliente)
            f"Cliente: {self.ordine.cliente.nome}",
            f"Email: {self.ordine.cliente.mail}",
            f"Categoria: {self.ordine.cliente.categoria}",
            "",
            "-" * 60,
            "DETTAGLIO PRODOTTI",
            "-" * 60,
        ]

        # L'utilizzo di enumerate() restituisce 2 valori a ogni ciclo: (indice, oggetto associato).
        # NOTA STUDIO: Passando '1' come secondo argomento forziamo enumerate a far partire
        # l'indice da 1 invece che dal classico 0.
        for i, riga in enumerate(self.ordine.righe, 1):
            linee.append(
                # Formattazione stringhe complessa:
                # :<22 allinea a sinistra occupando 22 spazi
                # :>3 allinea a destra occupando 3 spazi
                # :>8.2f allinea a destra in 8 spazi e formatta come float a 2 decimali
                f"{i}. {riga.prodotto.name:<22} "
                f"Q.tà {riga.quantita:>3} x {riga.prodotto.prezzo_unitario:>8.2f}€ = "
                f"{riga.totale_riga():>10.2f}€"
            )

        linee.extend([
            "-" * 60,
            "",
            f"{'Totale netto:':<40} {self.ordine.totale_netto():>18.2f}€",
            f"{'IVA 22%:':<40} {self.ordine.totale_netto() * 0.22:>18.2f}€",
            f"{'TOTALE FATTURA:':<40} {self.ordine.totale_lordo(0.22):>18.2f}€",
            "",
            "=" * 60
        ])

        # Join unisce tutti gli elementi della lista usando "\n" (a capo) come separatore
        return "\n".join(linee)

    # --- VERSIONE BASE SCRITTA IN CLASSE DAL PROF ---
    # (Mantenuta come riferimento di come farlo in modo più semplice e rapido)
    #
    # def genera_fattura_base(self):
    #     linee = [
    #         f"=" * 60,
    #         f"Fattura no. {self.numero_fattura} del {self.data}",
    #         f"=" * 60,
    #         f"Cliente: {self.ordine.cliente.nome}",
    #         f"Categoria: {self.ordine.cliente.categoria}",
    #         f"Mail: {self.ordine.cliente.mail}",
    #         f"-" * 60,
    #         f"DETTAGLIO ORDINE"
    #     ]
    #     for i, riga in enumerate(self.ordine.righe):
    #         linee.append(
    #             f"{i+1}. " # Qui l'indice partiva da 0, quindi aggiungevamo +1 a mano
    #             f"{riga.prodotto.name} "
    #             f"Q.tà {riga.quantita} x {riga.prodotto.prezzo_unitario} = "
    #             f"Tot. {riga.totale_riga()}"
    #         )
    #     linee.extend([
    #         f"-" * 60,
    #         f"Totale Netto: {self.ordine.totale_netto()}",
    #         f"IVA(22%): {self.ordine.totale_netto()*0.22}",
    #         f"Totale Lordo: {self.ordine.totale_lordo(0.22)}",
    #         f"=" * 60
    #         ]
    #     )
    #     return "\n".join(linee)


def _test_modulo():
    print("Test generazione Fattura:\n")

    # 1. Creiamo i prodotti in f-string
    p1 = ProdottoRecord("Laptop", 1200.0)
    p2 = ProdottoRecord("Mouse", 20.0)
    p3 = ProdottoRecord("Tablet", 600.0)

    # 2. Creiamo il cliente
    cliente = ClienteRecord("Mario Bianchi", "mario.bianchi@polito.it", "Gold")

    # 3. Assembliamo l'ordine
    ordine = Ordine(
        righe=[
            RigaOrdine(p1, 1),
            RigaOrdine(p2, 5),
            RigaOrdine(p3, 2)
        ],
        cliente=cliente
    )

    # 4. Creiamo la fattura passando l'ordine completo
    fattura = Fattura(ordine, "2026/01", date.today())

    # 5. Stampiamo il risultato della stringa generata
    print(fattura.genera_fattura())


if __name__ == "__main__":
    _test_modulo()
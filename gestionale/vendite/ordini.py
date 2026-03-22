from dataclasses import dataclass

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord


@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantita: int

    # NOTA STUDIO: Possiamo tranquillamente aggiungere dei metodi "ad hoc"
    # direttamente dentro una dataclass, non servono solo a contenere variabili!
    def totale_riga(self):
        """Calcola il costo della singola riga dell'ordine (prezzo unitario * quantità)"""
        return self.prodotto.prezzo_unitario * self.quantita


@dataclass
class Ordine:
    # NOTA STUDIO: Cos'è la sintassi list[RigaOrdine]? Si chiama "Type Hinting".
    # Indica semplicemente che l'attributo 'righe' è una lista e che al suo interno
    # contiene (o dovrebbe contenere) esclusivamente oggetti di tipo 'RigaOrdine'.
    righe: list[RigaOrdine]
    cliente: ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo(self, aliquota_iva):
        return self.totale_netto() * (1 + aliquota_iva)

    def numero_righe(self):
        return len(self.righe)

    def riepilogo(self) -> str:
        """Restituisce un riepilogo testuale dell'ordine."""
        linee = [
            f"Ordine per: {self.cliente.nome} ({self.cliente.mail})",
            f"Categoria cliente: {self.cliente.categoria}",
            "-" * 50
        ]

        for i, riga in enumerate(self.righe, 1):
            linee.append(
                f"{i}. {riga.prodotto.name} - "
                f"Q.tà {riga.quantita} x {riga.prodotto.prezzo_unitario}€ = "
                f"{riga.totale_riga()}€"
            )

        linee.append("-" * 50)
        linee.append(f"Totale netto: {self.totale_netto():.2f}€")
        linee.append(f"Totale lordo (IVA 22%): {self.totale_lordo(0.22):.2f}€")

        return "\n".join(linee)


@dataclass
class OrdineConSconto(Ordine):
    # NOTA STUDIO: Anche utilizzando le dataclass è possibile sfruttare l'ereditarietà!
    # OrdineConSconto eredita tutto da Ordine e aggiunge questo nuovo attributo.
    sconto_percentuale: float

    def totale_scontato(self):
        # BUG FIX dal codice del prof:
        # 1. Mancava il "return".
        # 2. Il metodo totale_lordo() definito nella classe padre richiede l'argomento 'aliquota_iva'.
        # Scritto senza argomento avrebbe generato un TypeError.
        return self.totale_lordo(0.22) * (1 - self.sconto_percentuale)

    def totale_netto(self):
        # BUG FIX / OVERRIDE:
        # L'icona del "bersaglio" a margine nel tuo IDE (es. PyCharm o VSCode) indica gli OVERRIDE:
        # - Freccia in alto: ti porta al metodo originale della classe padre.
        # - Freccia in basso: ti porta al metodo ridefinito nella classe figlia.

        # super().totale_netto() chiama il metodo della classe padre (Ordine) per non riscrivere la logica
        netto_base = super().totale_netto()
        return netto_base * (1 - self.sconto_percentuale)

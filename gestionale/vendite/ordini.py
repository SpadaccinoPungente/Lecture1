from dataclasses import dataclass

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord


@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantita: int

    # Possiamo anche aggiungere dei metodi "ad hoc" direttamente dentro una dataclass
    def totale_riga(self):
        # Costo della riga dell'ordine (prezzo unitario * quantità)
        return self.prodotto.prezzo_unitario * self.quantita


@dataclass
class Ordine:
    # Com'è la sintassi qui? (list[RigaOrdine]) -> Si chiama "Type Hinting".
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
# Anche utilizzando le dataclass è possibile sfruttare l'ereditarietà!
class OrdineConSconto(Ordine):
    sconto_percentuale: float

    def totale_scontato(self):
        # NOTA: Nel codice del prof mancava il "return" qui, l'abbiamo recuperato dai tuoi appunti.
        # ATTENZIONE: Il metodo totale_lordo() definito nella classe padre richiede l'argomento 'aliquota_iva'.
        # Scritto così (sia dal prof che nei tuoi appunti) genererà un TypeError quando chiamato.
        # Dovrebbe essere ad es: self.totale_lordo(0.22) * (1 - self.sconto_percentuale)
        return self.totale_lordo(0.22) * (1 - self.sconto_percentuale)

    def totale_netto(self):
        # L'icona del "bersaglio" a margine nel tuo IDE (es. PyCharm o VSCode) indica gli OVERRIDE:
        # - Freccia/icona in alto: ti porta al metodo originale della classe padre (specifica).
        # - Freccia/icona in basso: ti porta al metodo ridefinito nella classe figlia (specificato).
        netto_base = super().totale_netto()
        return netto_base * (1 - self.sconto_percentuale)

def lies_verkaeufe(dateiname):
    verkaeufe = []
    with open(dateiname, "r", encoding="utf-8") as datei:
        datei.readline()  # erste Zeile ist die Überschrift, die überspringen wir
        zeilennummer = 1
        for zeile in datei:
            zeilennummer = zeilennummer + 1
            zeile = zeile.strip()
            if zeile == "":
                continue  # leere Zeilen ignorieren

            teile = zeile.split(",")
            if len(teile) != 4:
                print(f"Zeile {zeilennummer} übersprungen: 4 Werte erwartet, {len(teile)} gefunden.")
                continue

            datum = teile[0].strip()
            produkt = teile[1].strip()
            if produkt == "":
                print(f"Zeile {zeilennummer} übersprungen: Produktname fehlt.")
                continue

            # Menge und Preis müssen Zahlen sein, sonst gibt es einen ValueError
            try:
                menge = int(teile[2])
                preis = float(teile[3])
            except ValueError:
                print(f"Zeile {zeilennummer} übersprungen: Menge oder Preis ist keine gültige Zahl.")
                continue

            if menge <= 0 or preis < 0:
                print(f"Zeile {zeilennummer} übersprungen: Menge oder Preis ist negativ bzw. 0.")
                continue

            verkaeufe.append([datum, produkt, menge, preis])
    return verkaeufe


def umsatz_pro_produkt(verkaeufe):
    umsatz = {}  # Produkt -> Umsatz
    for datum, produkt, menge, preis in verkaeufe:
        if produkt not in umsatz:
            umsatz[produkt] = 0
        # runden, damit keine Kommazahlen-Ungenauigkeiten wie 19.599999 entstehen
        umsatz[produkt] = round(umsatz[produkt] + menge * preis, 2)
    return umsatz


def nach_umsatz(eintrag):
    # eintrag ist ein Paar (Produkt, Umsatz), sortiert wird nach dem Umsatz
    return eintrag[1]


def main():
    try:
        verkaeufe = lies_verkaeufe("verkaeufe.csv")
    except FileNotFoundError:
        print("Fehler: Die Datei verkaeufe.csv wurde nicht gefunden.")
        return

    if len(verkaeufe) == 0:
        print("Es wurden keine gültigen Verkäufe gefunden.")
        return

    umsatz = umsatz_pro_produkt(verkaeufe)
    sortiert = sorted(umsatz.items(), key=nach_umsatz, reverse=True)

    print("Umsatz pro Produkt:")
    for produkt, betrag in sortiert:
        print(f"  {produkt:<10} {betrag:>8.2f} €")

    # Es kann mehrere Top-Produkte mit dem gleichen Umsatz geben
    top_umsatz = sortiert[0][1]
    top_produkte = []
    for produkt, betrag in sortiert:
        if betrag == top_umsatz:
            top_produkte.append(produkt)
    print(f"Top-Produkt: {', '.join(top_produkte)} mit {top_umsatz:.2f} €")


if __name__ == "__main__":
    main()

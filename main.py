class Buch:
    def __init__(self, titel, autor):
        # Titel und Autor müssen Texte sein und dürfen nicht leer sein
        if not isinstance(titel, str) or titel.strip() == "":
            raise ValueError("Der Titel darf nicht leer sein.")
        if not isinstance(autor, str) or autor.strip() == "":
            raise ValueError("Der Autor darf nicht leer sein.")

        self.titel = titel.strip()
        self.autor = autor.strip()
        self.ausgeliehen = False  # ein neues Buch ist immer verfügbar

    def __str__(self):
        if self.ausgeliehen:
            status = "ausgeliehen"
        else:
            status = "verfügbar"
        return self.titel + " von " + self.autor + " (" + status + ")"


class Bibliothek:
    def __init__(self):
        self.buecher = []  # Liste aller Bücher in der Bibliothek

    def hinzufuegen(self, buch):
        if not isinstance(buch, Buch):
            raise TypeError("Es können nur Buch-Objekte hinzugefügt werden.")
        # Da wir beim Ausleihen über den Titel suchen, darf jeder Titel nur einmal vorkommen
        for vorhandenes_buch in self.buecher:
            if vorhandenes_buch.titel.lower() == buch.titel.lower():
                raise ValueError("Das Buch '" + buch.titel + "' gibt es schon in der Bibliothek.")
        self.buecher.append(buch)

    def suche_autor(self, autor):
        # Groß-/Kleinschreibung und Leerzeichen am Rand sollen egal sein
        gesucht = autor.strip().lower()
        ergebnis = []
        for buch in self.buecher:
            if buch.autor.lower() == gesucht:
                ergebnis.append(buch)
        return ergebnis

    def ausleihen(self, titel):
        gesucht = titel.strip().lower()
        for buch in self.buecher:
            if buch.titel.lower() == gesucht:
                if buch.ausgeliehen:
                    raise ValueError("Das Buch '" + buch.titel + "' ist schon ausgeliehen.")
                buch.ausgeliehen = True
                return buch
        # Wenn die Schleife ohne Treffer durchläuft, gibt es das Buch nicht
        raise ValueError("Das Buch '" + titel + "' gibt es nicht in der Bibliothek.")


if __name__ == "__main__":
    bib = Bibliothek()
    bib.hinzufuegen(Buch("Faust", "Goethe"))
    bib.hinzufuegen(Buch("Die Leiden des jungen Werther", "Goethe"))
    bib.hinzufuegen(Buch("Die Räuber", "Schiller"))

    print("Bücher von Goethe:")
    for buch in bib.suche_autor("goethe"):
        print(" ", buch)

    gefunden = bib.suche_autor("Kafka")
    if len(gefunden) == 0:
        print("Keine Bücher von Kafka gefunden.")

    bib.ausleihen("Faust")
    print("Faust wurde ausgeliehen.")

    # Fehlerfall: Buch ist schon ausgeliehen
    try:
        bib.ausleihen("faust")
    except ValueError as fehler:
        print("Fehler:", fehler)

    # Fehlerfall: Buch gibt es nicht
    try:
        bib.ausleihen("Harry Potter")
    except ValueError as fehler:
        print("Fehler:", fehler)

    # Fehlerfall: Buch wird doppelt hinzugefügt
    try:
        bib.hinzufuegen(Buch("Die Räuber", "Schiller"))
    except ValueError as fehler:
        print("Fehler:", fehler)

    # Fehlerfall: Buch ohne Titel
    try:
        bib.hinzufuegen(Buch("", "Unbekannt"))
    except ValueError as fehler:
        print("Fehler:", fehler)

    # Fehlerfall: etwas anderes als ein Buch hinzufügen
    try:
        bib.hinzufuegen("Faust")
    except TypeError as fehler:
        print("Fehler:", fehler)

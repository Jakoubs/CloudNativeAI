# Übung 1 · Das Modell als Baustein

 oplö:

- **Start:** Übung am Dienstag, 13.10.2026, 11:30, O/201
- **Abgabe:** Montag, 19.10.2026, 23:59, in Moodle
- **Arbeitsform:** einzeln oder zu zweit, wie in der Moodle-Gruppeneinteilung eingetragen
- **Aufwand:** etwa 6 Stunden für den Kern, dazu etwa 2 Stunden für den Zusatz

---

## Worum es geht

In dieser Übung legt ihr das Fundament für euer System im Praktikum: eine kleine Anwendung, die ein Sprachmodell aufruft, ohne zu wissen, welches. Das Modell steckt hinter einer Schnittstelle und wird nur über Konfiguration ausgewählt. Danach macht ihr sichtbar, was in VL 2 Theorie war: Wie stark streuen Antworten bei verschiedenen Temperaturen, was kostet Deutsch im Vergleich zu Englisch, und wie bringt ihr ein Modell dazu, verlässlich Daten statt Fließtext zu liefern?

Am Ende steht der erste Baustein des Campus-Assistenten: Er ordnet Mails von Studierenden strukturiert ein.

Grundlage sind die Skripte zu **VL 1** (Was ist Cloud-native AI?) und **VL 2** (Foundation Models verstehen).


| Teil  | Inhalt                                      | Aufwand    |        |
| ----- | ------------------------------------------- | ---------- | ------ |
| **1** | Setup und erster Modellaufruf               | ca. 1 h    | Kern   |
| **2** | Modell austauschen, nur über Konfiguration | ca. 45 min | Kern   |
| **3** | Sampling und Tokens messen                  | ca. 1 h    | Kern   |
| **4** | Anfragen strukturiert einordnen             | ca. 2,5 h  | Kern   |
| **5** | README mit Ergebnissen und Reflexion        | ca. 45 min | Kern   |
| **Z** | Zusatz: Ausgaben inhaltlich absichern       | ca. 2 h    | Zusatz |

Das Starter-Projekt liegt im Ordner `starter/`.

---

## Teil 1 · Setup und erster Modellaufruf (Kern)

1. **Docker** installieren, falls noch nicht vorhanden (Docker Desktop oder Docker Engine). Test: `docker run --rm hello-world`
2. Ein **eigenes Git-Repository** anlegen und das Starter-Projekt hineinkopieren. Bei Zweiergruppen arbeitet ihr in einem gemeinsamen Repository.
3. `.env.example` nach `.env` kopieren. Die Standardwerte nutzen das lokale Modell, ihr müsst nichts ändern.
4. Starten:

```bash
docker compose up --build app
```

Beim ersten Start lädt der Dienst `modell-laden` zwei Modelle herunter: `llama3.2:3b` (ca. 2 GB) und `qwen2.5:0.5b` (ca. 400 MB). Das dauert einmalig ein paar Minuten. Danach beantwortet die Anwendung eine Standardfrage und gibt Messwerte aus.

Eigene Frage stellen. Der Ordner `app/` ist in den Container eingebunden, Änderungen am Code wirken also sofort ohne neuen Build:

```bash
docker compose run --rm app hallo_llm.py "Wie melde ich mich zu einer Prüfung an?"
```

**Aufgaben:**

1. Lest `compose.yaml`, `app/llm.py` und `app/hallo_llm.py`. Beschreibt im README in drei, vier Sätzen: Welche Container laufen, und wie findet die Anwendung das Modell?
   In der `compose.yaml` wird einmal `ollama` gestartet, das ist der Container des Modells, für die API. Als zweiten Container gibt es `modell-laden`, diese Container führt nur kurz Befehle aus um die Modelle einmal zu laden, sobald diese geladen sind beendet er sich, der dritte Container `app` startet erst, wenn `modell-laden` erfolgreich beendet ist. Die App findet den Ollama-Container über seinen Namen im Compose-Netzwerk. Die Adresse und der Modelname stehen in der  `.env`. Darüber wird das Model gewählt und lässt sich immer austauschen.
2. Stellt drei verschiedene Fragen an den Campus-Assistenten. Notiert jeweils **Time to First Token** und **Gesamtdauer**.

   Frage 1: "Wann hat die Mensa an der HTWG Konstanz geöffnet"
   TTFT: 703ms
   Gesamtdauer: 2523ms
   Notiz: Antwort war, wann die Mensa gegründet wurde und nichts zu den Öffnungszeiten.

   Frage 2: "Wie lautet die Adresse der HTWG Konstanz?"
   TTFT: 621ms
   Gesamtdauer 2660ms
   Notiz: Falsche Adresse: Hebelstraße 71 78538 Konstanz

   Frage 3: "Wann hat die Bibliothek an der HTWG Konstanz geöffnet?"
   TTFT: 531 ms
   Gesamtdauer: 8874ms
   Notiz: Wenigsten kommt hier als Antwort auch die (falsche) Geschichte der Bib raus.

---

## Teil 2 · Modell austauschen (Kern)

Ändert in `.env` nur die Zeile `LLM_MODEL` auf `qwen2.5:0.5b` und stellt dieselben drei Fragen noch einmal. **Am Code ändert ihr nichts.**

**Aufgaben:**

1. Füllt im README die Tabelle aus:


| Frage                                                   | Modell       | TTFT (ms) | Gesamt (ms) | Antwort brauchbar?                                                       |
| ------------------------------------------------------- | ------------ | --------- | ----------- | ------------------------------------------------------------------------ |
| Wann hat die Mensa an der HTWG Konstanz geöffnet       | llama3.2:3b  | 703       | 2523        | Jein, gibt Gründung und keine Öffnungszeiten (gibt aber Falsches Jahr) |
|                                                         | qwen2.5:0.5b | 117       | 483         | Nein, komplett falsch (was ist angefranst?)                             |
| Wie lautet die Adresse der HTWG Konstanz?               | llama3.2:3b  | 621       | 2660        | Nein, falsch                                                             |
|                                                         | qwen2.5:0.5b | 177       | 581         | Nein, auch falsch, PLZ nicht in BW                                       |
| Wann hat die Bibliothek an der HTWG Konstanz geöffnet? | llama3.2:3b  | 531       | 8874        | Nein, auch nicht das gewollte, wie bei 1.                                |
|                                                         | qwen2.5:0.5b | 67        | 423         | Auch falsch                                                              |

2. Fragt beide Modelle: „Ist die HTWG Konstanz eine private oder eine staatliche Hochschule?“ Was fällt euch auf?

Wenn man direkt nach dem wechsel das Modell laufen lässt, braucht die erste Anfrage immer länger, daher hab ich immer dann erst bei der 2. Frage drauf geachtet.

**qwen2.5:0.5b:** Antwortet ist flasch, da es laut diesem Modell sowohl eine private und eine staatliche Hochschule sein soll.

**llama3.2:3b:**  Die 1. Anwort (direkt nach dem laden) ist richtig, hat aber falsche Grammatik, die 2. ist auch inhaltlich richtig, hier ist die Abkürzung HTWG falsch ausgeschrieben.

**Optional, wenn die Academic Cloud erreichbar ist:** Mit einem API-Key über [KISSKI](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/) tragt ihr Variante B aus `.env.example` ein und nutzt `qwen3-30b-a3b-instruct-2507` als drittes Modell im Vergleich. Wer keinen Key hat oder wenn der Dienst nicht läuft, verliert dadurch nichts. Alle Teile funktionieren komplett lokal.

---

## Teil 3 · Sampling und Tokens messen (Kern)

Stellt `LLM_MODEL` zurück auf `llama3.2:3b`.

### Sampling

```bash
docker compose run --rm app sampling.py
```

Das Skript stellt dieselbe Frage je fünfmal bei Temperature 0, 0,7 und 1,2 und zählt die verschiedenen Antworten.

1. Wie viele verschiedene Antworten bekommt ihr bei jeder Temperature?
   0: 5x das gleiche
   0.7: 4 verschiede Antworten bei 5 durchläufen
   1.2: 5 verschiedene Antworten
2. Liefert Temperature 0 wirklich fünfmal dieselbe Antwort? Wenn nicht: Woran könnte das liegen? (Skript VL 2, Abschnitt „Inkonsistenz“.)
   Hier hat es tatsächlich 5x die gleiche Antwort geliefert, tatsächlich müsste das aber nicht immer so sein. Durch die niedrige Temperatur wird zwar die Antwort konsistenter, jedoch kann selbst die Hardware durch unterschiedliche Rechenoperationen das Ergebnis beeinflussen. 
3. Startet das Skript mit einer Faktenfrage, z. B. `sampling.py "Ist die HTWG Konstanz eine private oder staatliche Hochschule? Antworte mit einem Satz."`. Achtet nicht nur auf „privat oder staatlich“, sondern auf jedes Detail, etwa wofür die Abkürzung HTWG steht. Welche Fehler kommen schon bei Temperature 0 vor, welche erst bei höheren Werten? Was sagt das über die Ursache (Sampling oder Trainingsdaten)?

Schon bei Temperature 0 fehlt der Gestaltungs-Part in der Abkürzung. Bei Temperatur 0.7 gab es 5 verschiedene Antworten, doch auch hier war keine 100% richtig, obwohl es hier auch weiß, dass die HTWG staatlich ist, gibt es trotzdem fehlerhafte Abkürzungs-Übersetzungen. Tatsächlich weiß es über alle Temperaturen in den meisten Anworten den ersten Teil der Bezeichnung: "für Technik, Wirtschaft und.." doch danach habert es. Diesmal weiß das Modell aber, dass es eine staatliche Hochschule ist. Die Fehler, die schon bei Temperatur 0 vorkommen, hält das Modell wohl für das wahrscheinlichste. Das kann daher kommen, das es in früheren Anfragen schon falsch geantwortet hat und nun seine eigenen Antworten als "wahr" annimmt. Dies nennt man Snowballing. 



### Tokens

```bash
docker compose run --rm app tokens.py
```

1. Wie viele Tokens braucht der deutsche Text, wie viele der englische? Um wie viel Prozent ist Deutsch teurer?
Deutsch braucht 63 Tokens, während Englisch nur 49 Tokens braucht. Damit braucht Deutsch 14 Tokens mehr und ist somit 29% teurer. 
2. Ersetzt in `tokens.py` die Texte durch eine eigene Frage mit langen zusammengesetzten Wörtern (z. B. „Prüfungsanmeldungsfrist“). Wird der Unterschied größer?

Wir haben uns für folgenden Frage entschieden: 

        "Deutsch": "Wie melde ich mich im Bachlor-Studiengang Angewandte Informatik "
               "für das Prüfungsfach in Mathematik 3 an, und bis wann ist "
               "die Prüfungsanmeldungsfrist).?",
        "Englisch": "How do I register for the Mathematics 3 exam in the "
                "Applied Computer Science program, and what is the "
                "registration deadline?",

Hier wird der Unterschiedgrößer, denn der deutsche Text ist mit 73 Tokens hier um 49% teurer, als der englische Text mit 49 Tokens. 
---

## Teil 4 · Anfragen strukturiert einordnen (Kern)

Der Campus-Assistent soll jede Mail zuerst einordnen: Um welches **Anliegen** geht es (Prüfung, Mensa, Bibliothek, Sonstiges), welcher **Studiengang**, welche **Frist**? Das Ergebnis verarbeitet ein Programm weiter. Es muss also immer dieselbe Form haben.

Öffnet `app/einordnen.py`. Die Klasse `Anfrage` und die Hilfsfunktion `schema_von` sind vorgegeben. Eure Aufgaben stehen an den `TODO`-Kommentaren:

1. **TODO 1:** Ruft das Modell mit `response_format=schema_von(Anfrage)` auf. Wählt eine passende Temperature und begründet sie im Code mit einem Kommentar.
2. **TODO 2:** Prüft die Antwort mit `Anfrage.model_validate_json(...)`.
3. **TODO 3:** Ist die Antwort ungültig, versucht es erneut, höchstens dreimal. Danach soll das Programm mit einem klaren Fehler abbrechen, statt mit kaputten Daten weiterzuarbeiten.
4. **TODO 4:** Wertet alle Test-Mails aus `mails.json` aus und zählt, wie viele Anliegen richtig erkannt sind.

```bash
docker compose run --rm app einordnen.py
docker compose run --rm app einordnen.py "Eure eigene Mail"
```

**Aufgaben zur Auswertung:**

1. Wie viele der acht Mails ordnen `llama3.2:3b` und `qwen2.5:0.5b` jeweils richtig ein?
Bei `llama3.2:3b` ordnet es 7 von 8 Mails richtig ein und bei `qwen2.5:0.5b` ordnet es nur 2 von 8 Mails richtig ein. 

2. Schaut euch die Fehler an. Ist das Anliegen falsch, oder stimmen Studiengang und Frist nicht?
`llama3.2:3b`: Hier ist in der Falschen Mail das anliegen falsch. 
`qwen2.5:0.5b`: hier ist das Anliegen eigentlich immer pruefung, die zwei richtigen sind nur durch Zufall richtig.

3. Schaut auch bei den „richtigen“ Fällen genau hin: Steht bei `studiengang` manchmal der **Text** `"null"` statt eines echten leeren Werts? Nennt das Modell eine **Frist, die gar nicht in der Mail steht**? Warum lässt das Schema beides durch?

Bei `llama3.2:3b`: 
    eduroam-Mail: frist und studiengang ist null als Text
    Master MSI-Mail: Frist ist erfunden
    Gedicht-Mail: Studiengang erfunden

Bei `qwen2.5:0.5b`:
    Master-MSI-Mail: Studiengang ist erfunden 

Das Schema lässt beides durch, da es Studiengang und frist nur als str | None definiert hat, "null" sowie erfundene Werte sind gütlige Strings und werden dadurch durchgelassen

4. Die letzte Mail in `mails.json` versucht, das Modell umzulenken. Was passiert? (Darum geht es in VL 3.)
Die Modelle können nicht vom Schema abweichen, daher auch kein Gedicht schreiben, `llama3.2:3b` erkennt zwar als Anliegen Sonstiges, `qwen2.5:0.5b` wählt wie in den meisten Fällen Prüfung und AIN
5. Entfernt testweise `response_format` und verlasst euch nur auf den System-Prompt. Gebt die Rohantwort des Modells mit `print` aus. Was geht schief? Warum bringt euer erneuter Versuch bei Temperature 0 nichts, und was könntet ihr ändern? Stellt `response_format` danach wieder her.
Die Felder sind falsch, es wird das Feld "Antwort" erfunden, in dem das Modell die Email versucht zu beantworten, außerdem wird das JSON als Markdown gegeben, wodurch es nciht gelesen werden kann und einen Fehler gibt. Der System-Prompt alleine reicht also nicht aus, auch eine höhere Temperatur ändert daran nichts, abhilfe würde also das repsone_format geben

---

## Teil 5 · README (Kern)

Euer README ist die Abgabe. Es enthält:

1. **Namen** und Matrikelnummern
2. **Start:** den einen Befehl, mit dem man euer System startet, und welche `.env` es braucht
3. **Ergebnisse** aus Teil 1 bis 4: Beschreibung der Container, Tabelle aus Teil 2, Messwerte aus Teil 3, Trefferquote aus Teil 4
4. **Reflexion**, je zwei bis vier Sätze:
   1. Warum steht das Modell in `.env` und nicht im Code?
   2. Welche Temperature habt ihr in `einordnen.py` gewählt, und warum?
   3. Was garantiert `response_format` mit Schema, und was nicht?
   4. Wann würdet ihr ein lokales Modell, wann einen Cloud-Dienst wählen? Nennt je zwei Gründe.

---

## Zusatz · Ausgaben inhaltlich absichern

Dieser Teil **entfällt**, wenn ihr am Semesterende mindestens 80 % Anwesenheit nachweist. Wer nicht sicher ist, gibt ihn mit ab. Zusatzteile sind nicht nachreichbar.

Das Schema garantiert die Form, nicht den Inhalt. In Teil 4 habt ihr gesehen, dass das Modell trotzdem `"null"` als Text schreibt oder Fristen erfindet. Fangt das ab:

1. Ergänzt `Anfrage` um **Pydantic-Validatoren** (`field_validator`):
   - Der Text `"null"`, `"None"` oder eine leere Zeichenkette wird zu einem echten `None`.
   - `studiengang` ist nur gültig, wenn es ein Kürzel aus einer festen Liste ist (z. B. AIN, WIN, MSI, und weitere, die ihr für sinnvoll haltet). Alles andere wird zu `None`.
2. Prüft **im Code, nicht im Modell**, ob die erkannte Frist tatsächlich in der Mail vorkommt. Findet ihr sie nicht, setzt ihr sie auf `None` und gebt eine Warnung aus.
3. Messt die Wirkung: Wie viele der acht Mails haben vorher und nachher **alle drei Felder** richtig? Anliegen und Studiengang vergleicht ihr exakt. Eine Frist zählt als richtig, wenn die erwartete Frist im Ergebnis enthalten ist, „Freitag, 16.10.“ passt also zu „16.10.“. Tragt beide Zahlen ins README ein.

---

## Was ihr abgebt

**In Moodle**, Aufgabe „Übung 1 (P1)“: den **Link zu eurem Repository** und den Commit-Hash eures Abgabestands. Das Repository muss für mich lesbar sein: öffentlich, oder ihr ladet meinen GitHub-Account `PascalLaube` als Collaborator ein.

**Harte Kriterien**, ohne die die Abgabe nicht bestanden ist:

- [ ]  Das System startet mit `docker compose up --build app` nach einer im README beschriebenen `.env`.
- [ ]  Keine Secrets im Repository. `.env` steht in `.gitignore` und ist nicht committet. Prüft es mit `git status`.
- [ ]  Abhängigkeiten sind gepinnt (`requirements.txt` mit festen Versionen, feste Image-Tags).
- [ ]  `einordnen.py` läuft durch und gibt die Trefferquote aus.
- [ ]  Das README enthält alle Punkte aus Teil 5.
- [ ]  Wer unter 80 % Anwesenheit landen könnte: Zusatzteil im README dokumentiert.

---

## Tipps

- **Modelle vorab laden:** Die Modelle sind zusammen etwa 2,4 GB groß. Startet `docker compose up --build app` am besten schon **vor der Übung** zu Hause, sonst teilen sich alle im Raum das WLAN. `docker compose logs modell-laden` zeigt den Fortschritt.
- **Hohe TTFT direkt nach einem Modellwechsel?** Ollama lädt das Modell beim ersten Aufruf in den Speicher. Messt deshalb erst ab dem zweiten Aufruf.
- **Wenig Speicher auf dem Laptop?** Arbeitet mit `qwen2.5:0.5b` und gebt `llama3.2:3b` an, wo ihr es nicht ausführen konntet. Schreibt das ins README.
- **Kein Docker möglich?** Meldet euch bis Donnerstag per Mail, dann finden wir eine Lösung.
- **KI-Werkzeuge** dürft ihr nutzen. Ihr müsst jede Zeile eures Codes erklären können.

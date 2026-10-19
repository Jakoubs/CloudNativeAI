# Praktikumsabgabe P1
**Cloud-native AI · WS 2026/27 · Praktikumsabgabe P1 · Jakob... und Jana Gölz**

## Start

### Befehl 
unser System startet unter: docker compose run --rm app hallo_llm.py "deine Frage"? 

### `.env`
```
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=llama3.2:3b
```

## Ergebnisse

**1. Fragen** 
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

**2. Tabelle ** 

| Frage                                                   | Modell       | TTFT (ms) | Gesamt (ms) | Antwort brauchbar?                                                       |
| ------------------------------------------------------- | ------------ | --------- | ----------- | ------------------------------------------------------------------------ |
| Wann hat die Mensa an der HTWG Konstanz geöffnet       | llama3.2:3b  | 703       | 2523        | Jein, gibt Gründung und keine Öffnungszeiten (gibt aber Falsches Jahr) |
|                                                         | qwen2.5:0.5b | 117       | 483         | Nein, komplett falsch (was ist angefranst?)                             |
| Wie lautet die Adresse der HTWG Konstanz?               | llama3.2:3b  | 621       | 2660        | Nein, falsch                                                             |
|                                                         | qwen2.5:0.5b | 177       | 581         | Nein, auch falsch, PLZ nicht in BW                                       |
| Wann hat die Bibliothek an der HTWG Konstanz geöffnet? | llama3.2:3b  | 531       | 8874        | Nein, auch nicht das gewollte, wie bei 1.                                |
|                                                         | qwen2.5:0.5b | 67        | 423         | Auch falsch                                                              |

**3. Sampling und Tokens messen** 

Sampling: 
Das Skript stellt dieselbe Frage je fünfmal bei Temperature 0, 0,7 und 1,2 und zählt die verschiedenen Antworten.

1. Wie viele verschiedene Antworten bekommt ihr bei jeder Temperature?
   0: 5x das gleiche
   0.7: 4 verschiede Antworten bei 5 durchläufen
   1.2: 5 verschiedene Antworten
2. Liefert Temperature 0 wirklich fünfmal dieselbe Antwort? Wenn nicht: Woran könnte das liegen? (Skript VL 2, Abschnitt „Inkonsistenz“.)
   Hier hat es tatsächlich 5x die gleiche Antwort geliefert, tatsächlich müsste das aber nicht immer so sein. Durch die niedrige Temperatur wird zwar die Antwort konsistenter, jedoch kann selbst die Hardware durch unterschiedliche Rechenoperationen das Ergebnis beeinflussen. 
3. Startet das Skript mit einer Faktenfrage, z. B. `sampling.py "Ist die HTWG Konstanz eine private oder staatliche Hochschule? Antworte mit einem Satz."`. Achtet nicht nur auf „privat oder staatlich“, sondern auf jedes Detail, etwa wofür die Abkürzung HTWG steht. Welche Fehler kommen schon bei Temperature 0 vor, welche erst bei höheren Werten? Was sagt das über die Ursache (Sampling oder Trainingsdaten)?

Schon bei Temperature 0 fehlt der Gestaltungs-Part in der Abkürzung. Bei Temperatur 0.7 gab es 5 verschiedene Antworten, doch auch hier war keine 100% richtig, obwohl es hier auch weiß, dass die HTWG staatlich ist, gibt es trotzdem fehlerhafte Abkürzungs-Übersetzungen. Tatsächlich weiß es über alle Temperaturen in den meisten Anworten den ersten Teil der Bezeichnung: "für Technik, Wirtschaft und.." doch danach habert es. Diesmal weiß das Modell aber, dass es eine staatliche Hochschule ist. Die Fehler, die schon bei Temperatur 0 vorkommen, hält das Modell wohl für das wahrscheinlichste. Das kann daher kommen, das es in früheren Anfragen schon falsch geantwortet hat und nun seine eigenen Antworten als "wahr" annimmt. Dies nennt man Snowballing. 

Tokens: 
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

**4. Anfragen strukturiert einordnen**

Trefferquote: 
`llama3.2:3b`: 7/8
`qwen2.5:0.5b`: 2/8


Fragen: 
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
Die Felder sind falsch, es wird das Feld "Antwort" erfunden, in dem das Modell die Email versucht zu beantworten, außerdem wird das JSON als Markdown gegeben, wodurch es nciht gelesen werden kann und einen Fehler gibt. Der System-Prompt alleine reicht also nicht aus, auch eine höhere Temperatur ändert daran nichts, abhilfe würde also das repsone_format geben.

## Reflexion 

   1. Warum steht das Modell in `.env` und nicht im Code?
   Das Modell steht in der `.env`, damit man es schnell und nur an einer Stelle wechseln kann.
   2. Welche Temperature habt ihr in `einordnen.py` gewählt, und warum?
   3. Was garantiert `response_format` mit Schema, und was nicht?
   4. Wann würdet ihr ein lokales Modell, wann einen Cloud-Dienst wählen? Nennt je zwei Gründe.
   Wir würden ein lokales Modell wählen, wenn wir einen Chat-Bot wollen, der Firmen/Hochschul/Abteilungsinterne Fragen beantworten kann, die nicht frei im Internet verfügbar sind, diese würden wir dem Modell dann vorgeben. Außerdem
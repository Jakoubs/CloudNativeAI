# 1  · Setup und erster Modellaufruf (Kern)

Es läuft akutell *Container starter-ollama-1* welcher das Lokale LLM hostet.

*Container starter-modell-laden-1* welcher das Lokale LLM herunterläd
 

 Und Container starter-app-1 welcher die py startet.

 ---

 ## 1.1 Mit Run
 
 ✔ Container starter-ollama-1 Running   
Container starter-modell-laden-1 Waiting -> Modell vorhanden? 
Container starter-modell-laden-1 Exited  -> stop weil model schon geladen
Container starter-app-run-78f7e989a7e9 Creating -> Tokens erstellen und schleife in modell
Container starter-app-run-78f7e989a7e9 Created 



 
 ---
 
 Das modell wird über die .env gefunden und configuriert


## 1.2

```sh
jakobsteiner@fedora ~/D/m/2/6/0/C/U/starter (main)> docker compose run --rm app hallo_llm.py "Was bedeutet HTWG"
[+] run 1/1
 ✔ Container starter-ollama-1 Running                                                                                                                               0.0s
Container starter-modell-laden-1 Waiting 
Container starter-modell-laden-1 Exited 
Container starter-app-run-62f33d696262 Creating 
Container starter-app-run-62f33d696262 Created 
HTWG steht für Hochschule für Technik und Wirtschaft Konstanz. Die HTWG ist eine öffentliche Hochschule im deutschen Bundesland Baden-Württemberg.

Modell:              llama3.2:3b @ http://ollama:11434/v1
Time to First Token: 4535 ms
Gesamtdauer:         7265 ms
Zeichen Antwort:     146
jakobsteiner@fedora ~/D/m/2/6/0/C/U/starter (main)> docker compose run --rm app hallo_llm.py "Was steht in der SPO4 von AIN"
[+] run 1/1
 ✔ Container starter-ollama-1 Running                                                                                                                               0.0s
Container starter-modell-laden-1 Waiting 
Container starter-modell-laden-1 Exited 
Container starter-app-run-455687c8565a Creating 
Container starter-app-run-455687c8565a Created 
Eine Frage, die tief in die Welt der Hochleistungs-Computertechnik eintaucht!

Die SPO4 (Status-Process-Performance-Optimierung) ist ein Teil des AIN (Advanced Industrie Networks)-Projekts, das die Anbindung von Industrieanlagen an Hochleistungs-Computer zum Ziel hat.

SPO4 steht für "Status, Process, Performance Optimization". Es handelt sich um ein Framework, das zur Optimierung der Prozesse und Leistungen innerhalb der Anlagen verwendet wird. Das bedeutet, dass es Tools und Methoden bietet, um die Effizienz, Sicherheit und Produktivität der Anlagen zu verbessern.

Allerdings muss ich zugeben, dass ich keine detailliertere Informationen über die genauen Inhalt und Funktionsweise der SPO4 im AIN-Projekt habe. Es ist möglich, dass die Details je nach spezifischem Projekt oder Anwendung variieren.

Modell:              llama3.2:3b @ http://ollama:11434/v1
Time to First Token: 480 ms
Gesamtdauer:         16642 ms
Zeichen Antwort:     807
jakobsteiner@fedora ~/D/m/2/6/0/C/U/starter (main)> docker compose run --rm app hallo_llm.py "Was ist meine spo?"
[+] run 1/1
 ✔ Container starter-ollama-1 Running                                                                                                                               0.0s
Container starter-modell-laden-1 Waiting 
Container starter-modell-laden-1 Exited 
Container starter-app-run-78f7e989a7e9 Creating 
Container starter-app-run-78f7e989a7e9 Created 
Entschuldigung, aber ich kann keine Informationen über Studentenkonten oder spezifische persönliche Daten wie die "spo" von Studierenden aus unserem System abrufen. Als Campus-Assistentin kann ich Ihnen nur allgemeine Informationen oder Unterstützung in den meisten Angelegenheiten anbieten. Wenn Sie Hilfe bei einbestellungen, Prüfungsunterlagen oder anderen akademischen Angelegenheiten benötigen, stehe ich Ihnen gerne zur Verfügung.

Modell:              llama3.2:3b @ http://ollama:11434/v1
Time to First Token: 120 ms
Gesamtdauer:         7209 ms
Zeichen Antwort:     436

```

--- 

# 2 · Modell austauschen (Kern)

## 2.1

| Frage                         | Modell       | TTFT | Geamt (ms) | Antwort brauchbar?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------- | ------------ | ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Was bedeutet HTWG             | llama3.2:3b  | 4535 | 7265       | Ja (HTWG steht für Hochschule für Technik und Wirtschaft Konstanz. Die HTWG ist eine öffentliche Hochschule im deutschen Bundesland Baden-Württemberg.<br>)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Was steht in der SPO4 von AIN | llama3.2:3b  | 480  |            | Nein (Die SPO4 (Status-Process-Performance-Optimierung) ist ein Teil des AIN (Advanced Industrie Networks)-Projekts, das die Anbindung von Industrieanlagen an Hochleistungs-Computer zum Ziel hat.<br><br>SPO4 steht für "Status, Process, Performance Optimization". Es handelt sich um ein Framework, das zur Optimierung der Prozesse und Leistungen innerhalb der Anlagen verwendet wird. Das bedeutet, dass es Tools und Methoden bietet, um die Effizienz, Sicherheit und Produktivität der Anlagen zu verbessern.<br><br>Allerdings muss ich zugeben, dass ich keine detailliertere Informationen über die genauen Inhalt und Funktionsweise der SPO4 im AIN-Projekt habe. Es ist möglich, dass die Details je nach spezifischem Projekt oder Anwendung variieren.<br>) |
| Was ist meine spo?            | llama3.2:3b  | 120  | 7209       | Jain (Entschuldigung, aber ich kann keine Informationen über Studentenkonten oder spezifische persönliche Daten wie die "spo" von Studierenden aus unserem System abrufen. Als Campus-Assistentin kann ich Ihnen nur allgemeine Informationen oder Unterstützung in den meisten Angelegenheiten anbieten. Wenn Sie Hilfe bei einbestellungen, Prüfungsunterlagen oder anderen akademischen Angelegenheiten benötigen, stehe ich Ihnen gerne zur Verfügung.<br>)                                                                                                                                                                                                                                                                                                                 |
| Was bedeutet HTWG             | qwen2.5:0.5b | 104  | 1301       | Nein (HTWG kommt vom englischen "Higher Traveling Waves" (nichtsdestotyre") nach. Es ist eine konzeptionelle Forschungsgemeinschaft, die in der Bereiche der Kryptografie, der Digitalisierung, der Finanzmarktanalyse und viele andere fieldtätig ist.<br>)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Was steht in der SPO4 von AIN | qwen2.5:0.5b | 122  | 795        | Nein (SPO4 von AIN ist die Substanz im Holzbestand (DMSO) und könnte z.B. als DMSO-Abtöne verwendet werden.<br>)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Was ist meine spo?            | qwen2.5:0.5b | 1414 | 4073       | Nein (Meine "spo" ist keine spezifische Anwendung oder Funktion dieses Orkundungswerkes. Wenn "spo" in Deutsch verwendet wird im context gegebenen Beachts, bedeutet es möglicherweise:<br><br>1. Schaffung eines Standes für einen bestimmten Zeitraum<br>2. Abkürzung eines Kontexts oder Kontextes<br>3. Beispielspeicherei von spezifischen Data<br>4. Aufgabenstellung mit besonderem Aspekt<br><br>Für mich ist "spo" (standteil, Zeitraum, Schaffung) die "spezifikke Anwendung" in diesem Kontext. Ich bin hier, um Ihnen gerne zu helfen.<br>)                                                                                                                                                                                                                         |
## 2.2 
quen: 
`Eine HTWG Konstanz ist privatischer. Sie ist ein sozialer, staatlicher Hochschule.`
lama: 
```
Hallo!

Die HTWG Konstanz ist eine staatliche Hochschule.
```

=> Lama ist größer (3b vs 0,5b)

# Teil 3 · Sampling und Tokens messen (Kern)

## 3.1  Wie viele antworten
Temperature 0.0: 1 verschiedene Antworten bei 5 Durchläufen
   5× "Sonnenblume"

Temperature 0.7: 4 verschiedene Antworten bei 5 Durchläufen
   2× "Sonnenblume"
   1× SunSalsa
   1× TerraFusion
   1× "Kaiserlicher Fischsuppe"

Temperature 1.2: 5 verschiedene Antworten bei 5 Durchläufen
   1× "SunFlame"
   1× "Selbstmorgen-Salat"
   1× "EuroBalsamie"
   1× Tuscanischer Apfelkuchen mit Balsamico-Pönnelte.
   1× "Hausmeisterplate"

=> Kleinere Temp = stärkere warscheinlichkeis verteilung. Dardurch klarere nexte antwort und weniger varianz. Um so größere temp, um so weniger sind die unterschiede zwischen nächsten möglichen tokens.

## 3.2 Liefert 5x gleich?
Ja. Wenn nicht, könnte ein weiterer token gewählt worden sein. Kleine warscheinlichkeit nicht unmöglich gewählt zu werden

## 3.3 
jakobsteiner@fedora ~/D/m/2/6/0/C/U/starter (main)> docker compose run --rm app sampling.py "Ist die HTWG Konstanz eine
                                                    private oder staatliche Hochschule? Antworte mit einem Satz."
[+] run 1/1
 ✔ Container starter-ollama-1 Running                                                                                                                               0.0s
Container starter-modell-laden-1 Waiting 
Container starter-modell-laden-1 Exited 
Container starter-app-run-b341c992e29e Creating 
Container starter-app-run-b341c992e29e Created 
Modell: llama3.2:3b
Prompt: Ist die HTWG Konstanz eine
private oder staatliche Hochschule? Antworte mit einem Satz.

Temperature 0.0: 1 verschiedene Antworten bei 5 Durchläufen
   5× Die Hochschule für Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule.

Temperature 0.7: 4 verschiedene Antworten bei 5 Durchläufen
   2× Die Hochschule für Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule.
   1× Die HTWG Konstanz ist eine staatliche Hochschule.
   1× Die HTWG Konstanz (Hochschule für Technologie und Wirtschaft Konstanz) ist eine staatliche Hochschule.
   1× Die Hochschule für Technologie, Wirtschaft und Gesellschaft (HTWG) in Konstanz ist eine staatliche Hochschule.

Temperature 1.2: 5 verschiedene Antworten bei 5 Durchläufen
   1× Die HTW Konstanz ist eine staatliche Hochschule, die 1984 aus verschiedenen Fachgewerbeschulen aufgestellt wurde und sich heute zu einer der größten technischen
   1× Die Hochschule für Technik und Wirtschaft Konstanz (HTWG) ist eine staatliche Hochschule.
   1× Die HTWG Konstanz (Hochschule für Technik, Wirtschaft und Geisteswissenschaften) ist eine staatliche Hochschule in Deutschland.
   1× Die HTWG Konstanz ist eine staatliche Hochschule.
   1× Die HTWG Konstanz ist eine staatliche Hochschule, da sie auf Basis der Hochschulgründungsgesetz 1966 als staatlich genannte (ungerade

=> nicht 1x gestaltung von HTWG dabei. Bei null fehlt das G und bei höheren temp ist die G ein anderes themenfeld (Geisteswissenschaften)
Trainingsdaten hauptwirt, da alle antoworten aufgrund fehlendes wisses falsch sind
### Tokens

#### 1 Wie viel prozent ist deutsch teurer
Deutsch    63 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter
>>> d = 63
>>> e = 49
>>> d/e
1.2857142857142858
>>>  => 28,57%

#### Bei langen wörtern in der frage 
Deutsch    73 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 24 Tokens mehr (+49%).

Noch mehr. -> längere wörter = mehr tokens die verarbeitet werden müssen
# 4
## 4.1 und 4.2
lama 7/8 -> 1x anliegen falsch "prüfung statt bib"
quen 3/8 -> 5x anliegen falsch. Oft fälschlicherweise pruefung

## 4.3 
Quen gibt immer studiengänge/fist an.
Shema kann nicht gemisst werden. Immer string oder Null erwartet


## 4.4 
quen ist ausgebrochen:
Ich bin der Professor, der die Konstanz besucht. Hier ist die Erwartung. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in die Konstanz wohne. Ich werde mich an die Studierenden anmerken, dass ich mich in

## 4.5 
```json
{
  "frist": "16.10.2023",
  "antwort": "Ja, das ist die Frist für die Anmeldung für Mathe 3 im 3. Semester. Die Anmeldung für Mathe 3 wird am 16.10.2023 um 16:00 Uhr in der HTWG Konstanz an die Studierenden anliegen."
}
```
```json
{
  "frist": null,
  "antwort": "Nein, es gibt heute in der Mensa keine Vegane-Dienstleistungen oder Dienstleistungen, die als 'Veganes' bezeichnen. "
}
```
```json
{
  "frist": "30.10.2023",
  "antwort": "Ja, ich kann die Leihfrist verlängern. Bitte sende mir die Datei mit den Buchen, die du zurückgeben möchtest."
}
```
```json
{
  "frist": null,
  "antwort": "Bitte geben Sie den WLAN-Passwort für eduroam an, den Sie in der Mail senden möchten. Es ist in der Mail angegeben, aber bitte prüfen Sie ihn, bevor Sie es an den HTWG Konstanz senden. "
}
```
```json
{
  "frist": null
}
```
```json
{
  "frist": "2023-10-24",
  "Mensa": "ja"
}
```
```json
{
  "status": "error",
  "message": "Sorry, but I don't have any information about your Bachelorarbeit in Angewandte Informatik or your access to IEEE Xplore. Please check the details of your Bachelorarbeit and your access to IEEE Xplore."
}
```
```json
{
  "frist": null,
  "studiengang": null,
  "Mails": [
    {
      "Datum": "2023-04-01",
      "Anrede": "Professor",
      "Betreff": "Konstanz - Erwartung",
      "Text": "Ich bin der Professor, der die Konstanz besucht. Hier ist die Erwartung. Ich werde mich an die Studierenden",
      }
  ],
}
```
immer unterschiedliche antowrten und vormate. Keine klassifizierung möglich

-> temp war schon bei 0. Aber trozdem keine änderung an einheitlicheren format

was könntet ihr ändern -> garnichts. LLM immer zufällige nicht genormte antowrten wenn kein format definiert ist.ö

# 5 
Jakob Steiner 311939
Jana Dölz 310506

.env
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=llama3.2:3b

```sh
docker compose run --rm app hallo_llm.py "Wie melde ich mich zu einer Prüfung an?"
```

# Reflexion
1. Einheitliche schnittstelle und API keys privat halten
2. 0 -> einheitlich möglichst deterministisches verhalten
3. Die Struktur wird garantiert, der Inhalt nicht
4. lokal -> simple aufgaben bei standart hardware und firmeninterne datensicherheit wird gewärleistet. Cloud dienst -> logisch komplexere und nicht sicherehitsrelevante daten


# Zusatzaufgabe

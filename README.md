# StundenplanB

## Project Description

Unsere App soll Schülerinnen, Schülern und Studierenden dabei helfen, zu entscheiden, ob sich ein Skitag mehr lohnt als der Schulbesuch.

Dazu ruft die App über eine Wetter-API die Wettervorhersage für den kommenden Tag sowie die Neuschneemengen der vergangenen Nacht bzw. der letzten Tage ab. Diese Daten werden mit dem persönlichen Stundenplan abgeglichen.

Die Nutzer können für jedes Fach individuell festlegen, wie wichtig ihnen der Unterricht ist und ob die Lektionen aufgezeichnet werden oder anderweitig nachgeholt werden können.

Auf Grundlage dieser Informationen bewertet die App die Schneeverhältnisse und die schulischen Verpflichtungen. Anschliessend berechnet sie, **ob sich das Schwänzen der Schule zugunsten eines Skitags lohnt**, und gibt eine entsprechende Empfehlung ab.

## Planned Features

- **Wetterdaten per API:** Abruf der Wettervorhersage für den kommenden Tag.
- **Schneeverhältnisse:** Analyse der Neuschneemengen der vergangenen Nacht und Tage.
- **Skigebietsauswahl:** Auswahl des gewünschten Skigebiets.
- **Stundenplan:** Hinterlegen und Verwalten eines persönlichen Stundenplans.
- **Individuelle Fachbewertung:** Gewichtung der Fächer nach persönlicher Wichtigkeit.
- **Unterrichtsaufzeichnungen:** Berücksichtigung, ob verpasste Lektionen nachgeholt werden können.
- **Persönliche Empfehlung:** Abwägung der Schneebedingungen gegen die schulischen Verpflichtungen.

## How It Works

1. **Skigebiet auswählen:** Der Nutzer wählt ein Skigebiet aus.
2. **Wetterdaten abrufen:** Die App ermittelt Wetterprognosen und Neuschneemengen.
3. **Stundenplan abgleichen:** Die betroffenen Unterrichtslektionen werden ermittelt.
4. **Fächer bewerten:** Wichtigkeit und Nachholmöglichkeiten werden berücksichtigt.
5. **Empfehlung berechnen:** Die App bewertet, ob sich ein Skitag lohnt.

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.14 (geplant) |
| Package Management | pip / requirements.txt |
| Weather API | TBD |
| Containerization | Docker (vorbereitet) |
| Version Control | Git & GitHub |
| Development Environment | VS Code / Neovim |

## Installation and Setup

Das Projekt befindet sich noch in der Entwicklung. Die folgenden Schritte richten die Python-Entwicklungsumgebung ein. Die Anwendung ist möglicherweise noch nicht vollständig lauffähig.

### Prerequisites

- Git
- Python (vorgesehen: 3.14)

### Installation

1. Repository klonen und im Terminal in das Projektverzeichnis wechseln.
2. Virtuelle Umgebung erstellen und aktivieren:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Abhängigkeiten installieren:

   ```bash
   python -m pip install -r requirements.txt
   python -m pip install -r requirements-dev.txt
   ```

4. Falls benötigt, Umgebungsvariablen vorbereiten:

   ```bash
   cp .env.example .env
   ```

   Benötigte API-Schlüssel werden später in `.env` eingetragen. Die Datei `.env` darf nicht ins Repository committed werden.

### Run the Application

Sobald der Einstiegspunkt implementiert ist, kann die Anwendung voraussichtlich mit folgendem Befehl gestartet werden:

```bash
python src/main.py
```

## Development Process and Community Rules

- `main`: Stabiler Hauptbranch.
- `feature/*`: Branches für neue Funktionen.
- `fix/*`: Branches für Fehlerbehebungen.

Änderungen werden in eigenen Branches entwickelt und über Pull Requests integriert. Vor dem Merge sollen sie von einem anderen Teammitglied überprüft werden.

## Repository Structure

```text
.
├── config.ini              # Anwendungskonfiguration
├── docker-compose.yml      # Docker-Compose-Konfiguration
├── Dockerfile              # Docker-Image-Definition
├── .dockerignore           # Von Docker ausgeschlossene Dateien
├── docs/
│   ├── architecture.md     # Architekturdokumentation
│   └── retro.md            # Retrospektiven
├── .env.example            # Beispiel für Umgebungsvariablen
├── .gitignore              # Von Git ausgeschlossene Dateien
├── README.md               # Projektdokumentation
├── requirements-dev.txt    # Entwicklungsabhängigkeiten
├── requirements.txt        # Python-Abhängigkeiten
└── src/
    ├── config.py           # Konfiguration
    └── main.py             # Einstiegspunkt der Anwendung
```

## Architecture

Die Architektur wird im Verlauf des Projekts dokumentiert: [Architecture Documentation](docs/architecture.md).

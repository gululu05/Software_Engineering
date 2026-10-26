# StundenplanB

## Project Description

Our app aims to help school and university students decide whether a day on the slopes is worth missing classes for.

To do this, the app uses a weather API to retrieve the forecast for the following day, as well as snowfall amounts from the previous night or the past few days. It then compares this information with the user's personal timetable.

Users can specify how important each subject is to them and whether the lessons are recorded or can be made up in other ways.

Based on this information, the app evaluates the snow conditions and academic commitments. It then calculates **whether skipping classes for a day of skiing is worth it** and provides a recommendation.

## Planned Features

- **Weather Data via API:** Retrieve the weather forecast for the following day.
- **Snow Conditions:** Analyze snowfall amounts from the previous night and recent days.
- **Ski Resort Selection:** Choose a preferred ski resort.
- **Timetable:** Create and manage a personal class schedule.
- **Individual Subject Ratings:** Assign importance levels to individual subjects.
- **Recorded Lessons:** Consider whether missed lessons can be caught up on.
- **Personalized Recommendation:** Weigh snow conditions against academic commitments.

## How It Works

1. **Select a Ski Resort:** The user chooses a ski resort.
2. **Retrieve Weather Data:** The app obtains weather forecasts and snowfall data.
3. **Check the Timetable:** The app identifies which classes would be missed.
4. **Evaluate Subjects:** Subject importance and options for catching up on missed material are taken into account.
5. **Calculate a Recommendation:** The app evaluates whether taking a day off to ski is worthwhile.

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.14 (planned) |
| Package Management | pip / requirements.txt |
| Weather API | TBD |
| Containerization | Docker (set up) |
| Version Control | Git & GitHub |
| Development Environment | VS Code / Neovim |

## Installation and Setup

The project is still under development. The following steps set up the Python development environment. The application may not yet be fully functional.

### Prerequisites

- Git
- Python (planned version: 3.14)

### Installation

1. Clone the repository and navigate to the project directory in your terminal.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   python -m pip install -r requirements-dev.txt
   ```

4. Set up environment variables if needed:

   ```bash
   cp .env.example .env
   ```

   Required API keys will be added to `.env` later. The `.env` file must not be committed to the repository.

### Run the Application

Once the entry point has been implemented, the application should be runnable with the following command:

```bash
python src/main.py
```

## Development Process and Community Rules

- `main`: Stable main branch.
- `feature/*`: Branches for developing new features.
- `fix/*`: Branches for fixing bugs.

Changes are developed in separate branches and integrated through pull requests. Before merging, changes should be reviewed by another team member.

## Repository Structure

```text
.
├── config.ini              # Application configuration
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── .dockerignore           # Files excluded from Docker builds
├── docs/
│   ├── architecture.md     # Architecture documentation
│   └── retro.md            # Retrospectives
├── .env.example            # Example environment variables
├── .gitignore              # Files excluded from Git
├── README.md               # Project documentation
├── requirements-dev.txt    # Development dependencies
├── requirements.txt        # Python dependencies
└── src/
    ├── config.py           # Configuration
    └── main.py             # Application entry point
```

## Architecture

The software architecture will be documented as the project progresses: [Architecture Documentation](docs/architecture.md).

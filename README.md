# Spotilingo

Spotilingo is a web application designed to analyze and visualize the languages used in the songs from a user's Spotify library. By leveraging Spotify's and Genius' APIs and advanced natural language processing (NLP), Spotilingo offers users a unique insight into the diversity of languages present in their favorite music.

## Project Structure

This project follows the Clean Architecture principles to ensure separation of concerns and scalability. Below is an overview of the project structure and the purpose of each directory:

### `/domain`

- **`entities/`**: Contains the core business objects of the application, such as `Song`, `User` and `LanguageAnalysis`.
- **`use_cases/`**: Implements application-specific business rules, including use cases like `AnalyzePlaylistLanguages` and `FetchUserPlaylist`.

### `/interface_adapters`

- **`controllers/`**: Handles incoming web requests, calling the appropriate use cases and returning the response. Examples include `PlaylistController`, `VisualizationController` and `AuthenticationController`.
- **`gateways/`**: Abstracts the communication with external systems and services, such as the Spotify API, Genius API  and the database.
- **`presenters/`**: Formats use case outputs for presentation in the UI, ensuring data is user-friendly and ready for display.

### `/frameworks_and_drivers`

- **`database/`**: Contains the database models (`models.py`) and the database setup/connection logic (`database.py`), facilitating data persistence and retrieval.
- **`external_services/`**: Integrates with external services like the Spotify API and Genius API, providing a centralized point for external communications.
- **`web_app/`**: The Flask/Django application setup, including configurations, route definitions, and the static and templates directories for frontend assets.

### `/tests`

- Organized by layer, this directory contains all unit, integration, and end-to-end tests for the application, ensuring reliability and facilitating continuous integration practices.

### `main.py`

- The main entry point of the application, responsible for starting the web server and initializing the application components.

## Getting Started

To get started with Spotilingo, follow these steps:

1. Clone the repository and navigate into the project directory.
2. Create a virtual environment with Python 3.10 and activate it.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Set up your Spotify API credentials and update the configuration files accordingly.
5. Run `python main.py` to start the application.

## Contributing

Contributions to Spotilingo are welcome! Please refer to the CONTRIBUTING.md for guidelines on how to make contributions.

## License

Spotilingo is licensed under the MIT License. See the LICENSE file for more details.

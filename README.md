# Price Tracker OZ.by (Asynchronous)


An efficient, asynchronous web scraper designed to monitor book prices on the OZ.by platform. This tool automates data collection, tracks price changes, and persists information into a structured SQLite database.

## Key Features

* **High Performance**: Leverages `aiohttp` and `asyncio` for non-blocking network requests.
* **Data Persistence**: Automatically stores product titles, prices, and timestamps in a local SQLite database.
* **Containerized**: Fully Dockerized for seamless deployment across any environment.
* **Robust Logging**: Comprehensive logging system for real-time monitoring and debugging.
* **Configurable**: Easily adjust parsing limits, batch sizes, and target IDs via environment variables.

## Tech Stack

- **Core:** Python 3.11
- **Networking:** `aiohttp` (Asynchronous HTTP Client)
- **Parsing:** `BeautifulSoup4` with `lxml` parser
- **Database:** `SQLite3`
- **Environment:** `python-dotenv`
- **DevOps:** `Docker`

## Getting Started
### Prerequisites
- Docker Desktop installed **OR** Python 3.11+
- A valid `.env` file (see Configuration)

**Configure Environment:**
Create a `.env` file in the root directory (use `.env.example` as a template):
    ```env
    START_ID=1010000
    TOTAL_TO_PARSE=500
    BATCH_SIZE=50

    ---

**Run with Docker:**

docker build -t price-checker .
docker run --env-file .env -v ${PWD}:/app price-checker

### Installation & Deployment

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MaxPtichar/price-checker.git](https://github.com/MaxPtichar/price-checker.git)
   cd price-checker


   ---

## Disclaimer
This project is for **educational purposes only**. It is intended to demonstrate web scraping techniques and asynchronous Python programming. Please respect the website's `robots.txt` and terms of service when using this tool.

# Article Recommender Engine

This project is an article recommendation engine that provides personalized content recommendations to users based on their reading history. It uses a content-based filtering approach, and the engine is designed to handle user interactions with Kafka.

## Features

- Fetches articles from multiple predefined sources periodically
- Tracks user reading habits by recording user-article interactions
- Implements a content-based filtering algorithm to recommend articles
- Uses Kafka for handling user interactions asynchronously
- Includes a Command-Line Interface (CLI) to interact with the core functionality

## File Structure

<pre>
article_recommender/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── views.py
│   ├── algorithm/
│   │   ├── __init__.py
│   │   └── content_based.py
│   └── utils/
│       ├── __init__.py
│       ├── kafka_helpers.py
│       ├── scraper.py
│       └── database_helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_algorithm.py
│   └── test_utils.py
│
├── config.py
├── requirements.txt
└── run.py
</pre>

## Prerequisites

- Python 3.8 or later
- Kafka installed and running

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/article-recommender.git


2. Change to the project directory:
cd article-recommender

3. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate

4. Install the required dependencies:
pip install -r requirements.txt

## Configuration

1. Update the `config.py` file with your database configuration and Kafka settings.

2. In `app/utils/scraper.py`, configure the scraper functions and sources for fetching articles.

## Running the Application

1. Start the Kafka server and create the necessary topics (e.g., 'user_interactions').

2. Start the article recommendation engine's CLI:

python app/main.py

3. Follow the prompts to generate recommendations for a user.

## Running the Tests

To run the tests for the recommendation engine, execute the following command:

python -m unittest discover tests


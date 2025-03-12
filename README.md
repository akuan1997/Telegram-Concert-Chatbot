# Telegram Bot for Concert Information

## Introduction
This Telegram bot provides concert information based on user queries. It supports both English and Chinese, allowing users to search for concerts by artist name, genre, city, or date. Additionally, users can set ticket sale reminders and receive daily updates on new concert announcements.

## Features
- Multilingual support (English and Chinese)
- Search for concerts using keywords, dates, cities, or music genres
- Refine search results by adding more keywords
- Set reminders for ticket sales
- Receive daily updates on newly announced and additional concert dates

## How It Works
1. Users can search for concerts by entering a city, date, music genre, or artist or combine multiple keywords to refine their search.
![Website Preview](https://i.imgur.com/U1EgRF7.png)
2. The bot also allows users to search ticketing time.
![Website Preview](https://i.imgur.com/SoEFgsX.png)
3. The bot sends daily notifications with newly announced concerts. If additional dates are added to a concert, users will receive an update.
![Website Preview](https://i.imgur.com/G6PfUJL.jpeg)
4. If the search results are too broad, users can use the UI to narrow down their search or display all results.
![Website Preview](https://i.imgur.com/lE45Ugn.jpeg)
5. Users can reply to a concert message with a specific time, and the bot will send a reminder before ticket sales start.
![Website Preview](https://i.imgur.com/8RGWiAf.jpeg)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Telegram Bot API token
- Rasa framework (for natural language processing)
- APScheduler (for scheduling reminders)
- Required Python packages (listed in `requirements.txt`)

### Setup Steps
1. Clone this repository:
   ```bash
   git clone <repo_url>
   cd <project_directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Telegram bot:
   - Obtain a bot token from [BotFather](https://t.me/botfather)
   - Replace `TOKEN` in `app.py` with your actual bot token.
4. Train the Rasa model (if required):
   ```bash
   rasa train
   ```
5. Start the bot:
   ```bash
   python app.py
   ```

## Usage
- **Start the bot**: Send `/start` to initiate interaction.
- **Switch language**: Use `/switch_language` to toggle between English and Chinese.
- **Search for concerts**: Enter artist names, cities, or dates to retrieve concert information.
- **Refine search results**: If too many results appear, the bot will allow users to add more keywords.
- **Set ticket sale reminders**: Reply to a concert message with a specific time before ticket sales begin.
- **Receive daily updates**: The bot sends a daily message at 9 PM with new concert announcements.

## File Structure
- `app.py` - Main application script
- `functions/` - Helper functions for text processing and data retrieval
- `models/` - Rasa-trained models for language understanding
- `data/` - JSON files containing concert data

## Future Improvements
- Enhance NLP capabilities for better keyword recognition
- Expand language support
- Improve ticket reminder functionality with calendar integration

## License
This project is licensed under the MIT License. Contributions and improvements are welcome!


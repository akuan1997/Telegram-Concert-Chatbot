# Comparative Analysis of User Preferences: Telegram Concert Chatbot vs. Web-Based Concert Information Aggregator

This repository contains the implementation and research related to the comparative analysis of user preferences between Telegram-based concert chatbots and web-based concert information aggregators. The study aims to identify which platform better satisfies users’ needs for concert information retrieval and to understand the factors influencing these preferences.

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Research Findings](#research-findings)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project focuses on comparing two different platforms for concert information dissemination: Telegram-based chatbots and web-based concert information aggregators. The Telegram chatbot was developed using the Rasa framework, while the web-based aggregator was implemented using WordPress. The aim was to evaluate user engagement, satisfaction, and the effectiveness of these platforms in providing concert information.

## Technologies Used

- **Rasa Framework**: Used for developing the Telegram chatbot with natural language processing and machine learning capabilities.
- **WordPress**: Utilized for creating the web-based concert information aggregator due to its flexibility and robust plugin ecosystem.
- **Playwright**: Used for real-time data extraction from multiple ticketing websites.
- **BM25 Algorithm**: Implemented in the chatbot for enhanced information retrieval accuracy.
- **Duckling Module**: Integrated into the chatbot for precise time and date extraction.
- **Python**: Used for data processing and automation scripts.

## Project Structure

```
├── data
│   ├── concert_data.json       # JSON files with extracted concert data
├── rasa_bot
│   ├── actions                 # Custom actions for Rasa chatbot
│   ├── data                    # Training data for Rasa NLU
│   ├── models                  # Pre-trained models for chatbot
├── wordpress_site
│   ├── wp-content              # WordPress content and plugin files
├── scripts
│   ├── data_extraction.py      # Scripts for data extraction using Playwright
│   ├── preprocessing.py        # Scripts for data preprocessing
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js for Playwright
- WordPress installation for web-based aggregator

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/concert-info-comparison.git
   cd concert-info-comparison
   ```

2. **Set up the Rasa environment**:
   ```bash
   cd rasa_bot
   pip install -r requirements.txt
   ```

3. **Set up WordPress**:
   - Follow the standard WordPress installation process.
   - Import the provided content and plugins into your WordPress instance.

4. **Run the Playwright script**:
   ```bash
   cd scripts
   python data_extraction.py
   ```

## Usage

### Running the Rasa Chatbot

To start the Rasa chatbot:

```bash
cd rasa_bot
rasa run actions
rasa shell
```

### Accessing the Web-Based Aggregator

- Deploy the WordPress site on a local or remote server.
- Access the aggregator by navigating to `http://yourserver.com`.

## Research Findings

The research indicated that:
- Telegram chatbots excel in providing real-time, interactive, and personalized responses, enhancing user engagement and satisfaction.
- Web-based aggregators are preferred for their structured and accessible presentation of concert information, allowing for easy browsing and filtering.

A hybrid approach integrating both platforms could offer a superior user experience.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


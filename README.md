# Searchy

![GIF Description](./static/output.gif)

## Overview
Searchy is a predictive AI-based question-answering system. It utilizes a combination of web scraping, natural language processing (NLP), and sentence-matching models to provide accurate responses to user queries.

## Features
- **AI-Powered Answers:** Uses Google's BERT model for sentence matching.
- **Web Scraping Integration:** Extracts relevant data using BeautifulSoup.
- **NLP Processing:** Utilizes spaCy for part-of-speech (POS) tagging and analysis.
- **Flask Deployment:** Lightweight web-based interface for easy interaction.

## Tech Stack
- **Web Scraping:** BeautifulSoup (BS4)
- **Sentence Matching:** Google's BERT model
- **POS Tagging:** spaCy NLP model
- **Deployment:** Flask (Python)

## Installation
```sh
git clone https://github.com/rahatbhambri/Searchy.git
cd Searchy
```

## Usage
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   python app.py
   ```
3. Access the web interface at `http://localhost:5000` and start asking questions.

## Future Enhancements
- Improve the model's accuracy with more training data.
- Implement database storage for caching responses.
- Extend support for multiple languages.
- Deploy as a cloud-based API.

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests.


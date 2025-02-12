# Movie Web Scraper and Recommender

Program that scrapes data from IMDb and recommends movies based off certain genres, directors, actors, and more!

View website at: https://movie-recommendations.streamlit.app/

## Setup & Run

Open a terminal and run:

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Goals

* Create a web scraper to save movie data from IMDb
* Use an algorithm to generate recommendations based on the criteria above
* Use this data to develop a website that displays these recommendations

## Current Progress

* Developed a functioning web scraper to download data
* Used machine learning (scikit-learn) to produce a similarity score based off an initial movie and optionally filters by IMDb ratings
* Deployed website through Heroku

## Future goals

* Add functionality to recommend movies based off of different criteria such as genres, keywords, cast, etc.
* Enhance website - add links to IMDb movie pages, add movie descriptions, improve visuals

## Authors

George Perry - contact me at gep1617@gmail.com

## License

This program uses the MIT License - view in LICENSE.md

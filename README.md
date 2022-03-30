# Amazon Review Scraper using Selectorlib 

A simple amazon scraper to extract product details and prices from Amazon.com using Python Requests and Selectorlib. 

## Usage

1. Install Requirements `pip3 install -r requirements.txt`
1. Add Amazon Product URLS to [urls.txt](urls.txt)
1. Run `python3 reviews.py`
1. Get data from [data.csv](data.csv)

## CSV Data Schema

| Column | Description |
|:-----------|:----------------|
|title | Title of review |
|content | Review content |
|date | Date of review |
|variant | Product model/ variant |
|images | Images if attached |
|verified | Is review verified |
|author | Author of review |
|rating | Ratings given by author |
|product | Product name |
|url | Url scrapped from |

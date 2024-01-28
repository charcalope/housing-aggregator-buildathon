# housing-aggregator-buildathon
This is an older project of mine.

I was frustrated by inaccuracies in Zillow and wanted to get data straight from the source.
This project attempts to get unit data like price, number of bedrooms, and more from apartment websites.

- this project navigates the HTML tree and relies on hard coded patterns to attempt data extraction
- to minimize the calls to the domain of the apartment website a screensheet of the webpage is captured and sent to a classifier
- that classifier is trained on a bunch of screenshots I took
- if it predicts unit listing page, then scraping is performed

- data was sourced at some point with Azure and a GIS list of multi family addresses




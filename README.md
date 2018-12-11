# soup4lyfe

## General summary

Our project consists of five main technical components:
- web scraping the cryptocompare API
- natural language preprocessing
- data transformation for technical indicators
- machine learning using scikit-learn
- bokeh interactive data visualizations

This document breaks down which files correspond to each component lives within this repository, and including instructions for running the bokeh server.

## Web scraping

- cryptocompare.py (library)
- data/ and news/ directories contain the scraped data

## Natural language processing

- gcl.py (library)
- sentiment analysis.ipynb (results)
- sentiment_results.csv (raw results)

## Technical indicators

- technicalIndicators.py (library)
- technicalIndicators_unittest.py (library of functions for unit testing)
- technical_indicators.ipynb (results)

## Machine learning

- scikit.py (library)
- Modelling with Sentiment.ipynb (results)

## Bokeh

- technicalVis.py (library used in technical.py)
- viz.py (one of two web pages on the bokeh application)
- technical.py (one of two web pages on the bokeh application)

To run the bokeh server locally, use this shell command while in the soup4lyfe directory:

```
bokeh serve --show technical.py viz.py
```

Note that the we cannot guarantee success running the application locally unless the following requirements are satisfied:

- bokeh 1.0.2
- pandas 0.23.4
- numpy 1.15.4
- scikit-learn 0.20.1

These are the versions of the modules installed on our AWS instance. While other versions may work, with bokeh in particular, outdated versions will be missing necessary functionality. 

It is for this reason primarily that we decided to host this application on AWS for convenience to the grader. The link is in our write-up but can also be found [here](http://ec2-13-58-251-30.us-east-2.compute.amazonaws.com:5006/technical).

Loading the Visualizations tab may take a while (but should not exceed one minute), as all of the models are backtested each time the page is served.

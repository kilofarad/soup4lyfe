from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.api_core.exceptions import InvalidArgument
import six


def analyze_sentiment(content):
    '''Adapted from GCL sample code. Performs a single sentiment analysis cal for a given string.'''
    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    try:
    # smallest block of code you foresee an error in
        response = client.analyze_sentiment(document)
        sentiment = response.document_sentiment # I think your exception is being raised in this call
        print('sentiment_analysis')
        return sentiment.score, sentiment.magnitude
    except InvalidArgument as e:
        print('InvalidArgument')
    # your trace shows InvalidArgument being raised and it appears you dont care about it
        pass # continue to next iteration since this error is expected
    except TypeError as e:
    # this is an example exception that is also OK and "skippable"
        print('TypeError')
        pass # continue to next iteration
    except Exception as e:
    # all other exceptions are BAD and unexpected.This is a larger problem than just this loop
        raise e # break the looping and raise to calling function


def sentiment_columns(series):
    '''Takes a pandas series of string-like data and performs GCL sentiment analysis,
    returning the columns for sentiment score and magnitude, respectively, in a tuple'''  
    try:
        series = series.apply(analyze_sentiment)
        return series.apply(lambda x: x[0]), series.apply(lambda x:x[1])
    except TypeError as e:
    # your trace shows TypeError being raised and it appears you dont care about it
        pass # continue to next iteration

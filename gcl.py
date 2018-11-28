from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six


def analyze_sentiment(content):

    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment

    return sentiment.score, sentiment.magnitude

def sentiment_columns(series):
	'''Takes a pandas series and performs GCL sentiment analysis, returning the columns for sentiment score and magnitude, respectively, in a tuple'''
	series = series.apply(analyze_sentiment)
	return series.apply(lambda x: x[0]), series.apply(lambda x:x[1])

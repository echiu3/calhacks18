import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def output_result(tweets):
    with open("result_file.txt", 'a') as sentiment_file:
        for tweet in tweets:
            sentiment_file.write(str(tweet[0]) + " " + str(tweet[1]) + "\n")


def analyze(tweet_filename):
    tweets = []
    client = language.LanguageServiceClient()

    with open(tweet_filename, 'r') as tweet_file:
        content = [line.rstrip('\n') for line in tweet_file]

    # Overwrites previous result document
    with open("result_file.txt", 'w') as sentiment_file:
        pass

    # Analyze every tweet in tweet document
    for tweet in content:
        document = types.Document(
            content=tweet,
            type=enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        magnitude = annotations.document_sentiment.magnitude
        tweets.append((score, magnitude))

    output_result(tweets)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'tweet_filename',
        help='The filename of the tweet you\'d like to analyze.')
    args = parser.parse_args()

    analyze(args.tweet_filename)

from sentiment import predict_sentiment, ROBERTA_SUPPORTED_LANGUAGES
from translate import translate_text
import csv

def read_tweets(file_path: str) -> list[dict[str, str]]:
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        list_of_tweets = list(reader)
    return list_of_tweets

tweets = read_tweets("./tweets.csv")

sentiment_by_id = {}

for tweet in tweets:
    tweet_text, language = tweet["text"], tweet["language"]

    if not (language and language in ROBERTA_SUPPORTED_LANGUAGES):
        translated_text, language = translate_text(tweet_text)

    if language in ROBERTA_SUPPORTED_LANGUAGES:
        sentiment = predict_sentiment(tweet_text)
    else:
        sentiment = predict_sentiment(translated_text)

    sentiment_by_id[tweet["id"]] = sentiment


#/ check the accuracy
test_labels = read_tweets("./test_labels.csv")
correct_predictions = 0

for test in test_labels:
    if sentiment_by_id[test["id"]] == test["label"]:
        correct_predictions += 1

accuracy = correct_predictions / len(test_labels)
print(f"Accuracy: {accuracy:.2f}")
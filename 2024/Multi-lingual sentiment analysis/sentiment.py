from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig


MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
ROBERTA_SUPPORTED_LANGUAGES = ('ar', 'en', 'fr', 'de', 'hi', 'it', 'es', 'pt')

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

#/ save the model locally
model.save_pretrained(MODEL)
tokenizer.save_pretrained(MODEL)


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_sentiment(text: str) -> str:
    processed_text = preprocess(text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    index_of_sentiment = output.logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    return sentiment



# text = "la pizza da @michele è veramente buona https://www.youtube.com"
# text = "این غذا خیلی شوره!"
# text = "یه جلسه دیگه که میتونست یه ایمیل باشه 🥲"
# print(predict_sentiment(text))
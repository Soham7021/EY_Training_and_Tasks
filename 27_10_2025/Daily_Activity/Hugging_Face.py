from transformers import pipeline
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

user_input = input("\nPlease enter a text: ")

result = classifier(user_input)

print(result)



















# def classify_sentiment():
#     print("Welcome to the Sentiment Analysis tool!")
#
#     while True:
#         user_input = input("\nPlease enter a text (or type 'exit' to quit): ")
#
#         if user_input.lower() == 'exit':
#             break
#
#
#         result = classifier(user_input)
#
#         print(result)
#
# if __name__ == '__main__':
#     classify_sentiment()

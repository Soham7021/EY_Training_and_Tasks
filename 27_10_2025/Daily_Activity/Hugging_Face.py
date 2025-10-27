from transformers import pipeline
import os

# Suppress the symlink warning if you want (Optional)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load the sentiment analysis pipeline with the explicit model
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')



def classify_sentiment():
    print("Welcome to the Sentiment Analysis tool!")

    while True:
        user_input = input("\nPlease enter a text (or type 'exit' to quit): ")

        # Exit the program if the user types 'exit'
        if user_input.lower() == 'exit':
            break


        result = classifier(user_input)

        sentiment = result[0]['label']
        confidence = result[0]['score']

        print(f"\nSentiment: {sentiment}")
        print(f"Confidence: {confidence:.4f}")


# Run the function
classify_sentiment()

from transformers import pipeline

# Load emotion classifier
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def get_emotion(text):
    results = emotion_classifier(text)
    sorted_emotions = sorted(results[0], key=lambda x: x['score'], reverse=True)
    top_emotion = sorted_emotions[0]
    return top_emotion['label'], round(top_emotion['score'], 2)

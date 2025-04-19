from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
import datetime

app = Flask(__name__)
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

user_data = {
    "moods": [],
    "suggestions": [],
}

mental_health_resources = {
    'depression': 'https://www.helpguide.org/articles/depression/coping-with-depression.htm',
    'suicide': 'https://www.suicidepreventionlifeline.org/',
    'anxiety': 'https://www.anxiety.org/',
    'stress': 'https://www.helpguide.org/articles/stress/stress-management.htm',
    'burnout': 'https://www.verywellmind.com/stress-and-burnout-symptoms-and-prevention-3144516',
    'loneliness': 'https://www.helpguide.org/articles/mental-health/dealing-with-loneliness-and-shyness.htm',
    'self-harm': 'https://www.psychologytoday.com/us/basics/self-harm',
    'panic': 'https://www.helpguide.org/articles/anxiety/panic-attacks-and-panic-disorders.htm',
    'sadness': 'https://www.helpguide.org/articles/depression/coping-with-depression.htm',
    'joy': 'https://www.verywellmind.com/positive-mental-health-4797654',
    'anger': 'https://www.psychologytoday.com/us/basics/anger',
    'fear': 'https://www.anxiety.org/',
    'love': 'https://www.psychologytoday.com/us/basics/relationships',
    'surprise': 'https://www.healthline.com/health/how-to-deal-with-life-changes'
}

def detect_mental_health_issues(text):
    """Use the model's results and keyword analysis to detect mental health conditions"""
    results = emotion_classifier(text)
    emotion = results[0]['label'].lower()
    score = results[0]['score']

    if 'suicide' in text or 'kill myself' in text or 'end my life' in text:
        condition = 'suicide'
        feedback = "I'm really sorry you're feeling this way, and it's important to talk to someone right away. You are not alone."
    elif 'depressed' in text or 'worthless' in text or 'numb' in text:
        condition = 'depression'
        feedback = "It seems like you're feeling depressed. Please know that there are ways to heal, and I’m here to help."
    elif 'anxiety' in text or 'panic' in text or 'overwhelmed' in text:
        condition = 'anxiety'
        feedback = "It looks like you're feeling anxious. Try some calming techniques, like deep breathing."
    elif 'lonely' in text or 'isolated' in text:
        condition = 'loneliness'
        feedback = "It seems you're feeling lonely. Connecting with others can help, even if it's hard to reach out."
    elif 'burnt out' in text or 'exhausted' in text:
        condition = 'burnout'
        feedback = "Burnout can be overwhelming, but it's important to take breaks and care for your well-being."
    elif 'self-harm' in text or 'cut myself' in text:
        condition = 'self-harm'
        feedback = "Please don't harm yourself. There are other ways to cope, and I'm here to guide you through them."
    elif 'stress' in text or 'overload' in text or 'pressure' in text:
        condition = 'stress'
        feedback = "It seems you're stressed. Taking a moment to ground yourself can help. Would you like some tips?"
    elif 'panic' in text or 'panic attack' in text:
        condition = 'panic'
        feedback = "You're experiencing panic. Deep breathing can help calm the body. Would you like to try a grounding exercise?"
    else:
        condition, feedback = analyze_emotion(text)

    return condition, feedback

def analyze_emotion(text):
    results = emotion_classifier(text)
    emotion = results[0]['label'].lower()
    score = results[0]['score']

    if emotion == 'sadness':
        feedback = "It seems you're feeling sad. I'm sorry you're going through this. It's important to give yourself time to feel these emotions."
    elif emotion == 'anger':
        feedback = "It seems like you're feeling angry. Deep breaths can help. Would you like to try a grounding exercise?"
    elif emotion == 'joy':
        feedback = "It seems you're feeling joyful! Keep up the positivity!"
    elif emotion == 'fear':
        feedback = "It seems you're feeling fearful or anxious. Let's work through some calming techniques."
    elif emotion == 'love':
        feedback = "You're feeling love! It's always a great thing to appreciate relationships in life."
    elif emotion == 'surprise':
        feedback = "You seem surprised! It's good to recognize changes and adapt."
    else:
        feedback = "I'm not sure how you're feeling, but I'm here to help!"

    return emotion, feedback

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_story = request.form['user_story']
        condition, feedback = detect_mental_health_issues(user_story)

        user_data["moods"].append((datetime.datetime.now(), condition))
        user_data["suggestions"].append(feedback)

        return redirect(url_for('feedback', condition=condition))
    return render_template('index.html')

@app.route('/feedback/<condition>', methods=['GET'])
def feedback(condition):
    """Provide feedback based on the user's detected condition/emotion and suggest resources."""
    feedback_message = user_data["suggestions"][-1]
    resource_link = mental_health_resources.get(condition, "https://www.psychologytoday.com/us")

    return render_template('feedback.html', feedback=feedback_message, resource=resource_link)

@app.route('/mood-track', methods=['GET'])
def mood_track():
    """Track user's mood history."""
    return render_template('mood_track.html', mood_data=user_data['moods'])

if __name__ == '__main__':
    app.run(debug=True)

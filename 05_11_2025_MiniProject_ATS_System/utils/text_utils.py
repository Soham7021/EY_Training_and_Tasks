import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_key_skills(text: str, limit: int = 10) -> str:
    """
    Return comma-separated matched skills from a predefined keyword list.
    Keeps the same keywords and behavior as your original code.
    """
    skill_keywords = [
        'python', 'c++', 'java', 'sql', 'aws', 'docker', 'kubernetes',
        'machine learning', 'deep learning', 'nlp', 'django', 'flask', 'react'
    ]
    text_lower = (text or "").lower()
    matched_skills = [skill for skill in skill_keywords if skill in text_lower]
    return ", ".join(matched_skills[:limit])

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity using TF-IDF vectors and cosine similarity.
    Returns a score scaled to 0-10 and rounded to 2 decimals (same as original).
    """
    try:
        # Defensive: if empty input, return 0.0 early (avoids sklearn errors)
        text1 = text1 or ""
        text2 = text2 or ""
        if text1.strip() == "" or text2.strip() == "":
            return 0.0

        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(similarity * 10, 2)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def extract_email_from_text(text: str) -> str:
    """
    Extract the first email address found in text, or return 'Not Found'.
    """
    if not text:
        return "Not Found"
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not Found"

def convert_to_native(obj):
    """
    Recursively convert numpy scalar types to native Python types and
    ensure dict/list structures are plain Python types for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj

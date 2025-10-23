import os
import requests
from dotenv import load_dotenv
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
from sentence_transformers import SentenceTransformer, util

# ---------------------------
# 1. Load environment variables
# ---------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")


# ---------------------------
# 2. Define function to call OpenRouter API
# ---------------------------
def get_model_response(prompt, model_name="mistralai/mistral-7b-instruct"):
    url = f"{base_url}/engines/{model_name}/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 256,
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        # Print the response text to debug the issue
        print(f"Error from OpenRouter: {response.status_code}, {response.text}")
        raise Exception(f"Error from OpenRouter: {response.status_code}, {response.text}")


# ---------------------------
# 3. Define prompt
# ---------------------------
prompt = "<s>[INST] Explain in simple terms what reinforcement learning is. [/INST]"

# ---------------------------
# 4. Get responses from OpenRouter
# ---------------------------
try:
    response_1 = get_model_response(prompt)
    response_2 = "This would be another model's response."  # You can set this to another API call if needed

    print("\n--- MODEL 1: Mistral 7B ---")
    print(response_1)
    print("\n--- MODEL 2: Mixtral 8x7B ---")
    print(response_2)

    # ---------------------------
    # 5. Evaluate responses
    # ---------------------------

    # BLEU
    smooth_fn = SmoothingFunction().method1
    bleu_score = sentence_bleu(
        [response_1.split()],
        response_2.split(),
        smoothing_function=smooth_fn
    )

    # ROUGE
    rouge = Rouge()
    rouge_scores = rouge.get_scores(response_1, response_2)[0]

    # Cosine similarity using embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    emb1 = embedder.encode(response_1, convert_to_tensor=True)
    emb2 = embedder.encode(response_2, convert_to_tensor=True)
    cosine_sim = float(util.cos_sim(emb1, emb2))

    # ---------------------------
    # 6. Display results
    # ---------------------------
    print("\n--- Evaluation Metrics ---")
    print(f"BLEU Score:  {bleu_score:.4f}")
    print(f"ROUGE-1:     {rouge_scores['rouge-1']['f']:.4f}")
    print(f"ROUGE-L:     {rouge_scores['rouge-l']['f']:.4f}")
    print(f"Cosine Sim:  {cosine_sim:.4f}")

except Exception as e:
    print(f"An error occurred: {e}")

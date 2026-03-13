import requests

# 1. Use host.docker.internal to reach the Docker Desktop Model Runner
url = "http://host.docker.internal:12434/v1/chat/completions"

# 2. Match the model name exactly to your 'docker model ls' output
payload = {
    "model": "gemma3", 
    "messages": [
        {"role": "user", "content": "Briefly, why did Rome fall?"}
    ],
    "stream": False
}

print("--- Requesting Gemma3 via Docker Model Runner ---")

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    answer = response.json()['choices'][0]['message']['content']
    print(f"\nGemma3 Response:\n{answer}")

except Exception as e:
    print(f"Connection Failed: {e}")
    # If this fails, we check if the Model Runner is active on the host
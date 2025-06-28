# llama_api.py
import ollama

def query_llama(prompt: str, model: str = "llama3") -> str:
    """
    Send a prompt to the local LLaMA model using Ollama and return the AI's reply.

    Parameters:
        prompt (str): The text you want to ask or send to the AI.
        model (str): The model name (default is 'llama3').

    Returns:
        str: The model's response as plain text.
    """
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()

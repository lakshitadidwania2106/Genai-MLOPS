
import ollama
import time


class OllamaConnector:

    def __init__(self, model_name): #init to store model name
        self.model_name = model_name

    def generate(self, prompt, temperature=0.0, seed=42): #send prompt to model

        start_time = time.perf_counter() #how much time model is taking to respond

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": temperature,
                "seed": seed
            }
        )

        end_time = time.perf_counter()

        result = {
            "model": self.model_name,
            "prompt": prompt,
            "output": response.message.content,
            "temperature": temperature,
            "seed": seed,
            "latency_seconds": round(
                end_time - start_time, 4
            )
        }

        return result

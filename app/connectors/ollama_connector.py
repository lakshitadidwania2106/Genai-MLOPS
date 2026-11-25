
import ollama
import time


class OllamaConnector:

    def __init__(self, model_name):
        self.model_name = model_name

    def generate(
        self,
        prompt,
        temperature=0.8,
        seed=42,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.0,
        num_predict=256
    ):

        start_time = time.perf_counter()

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": temperature,
                "seed": seed,
                "top_p": top_p,
                "top_k": top_k,
                "repeat_penalty": repeat_penalty,
                "num_predict": num_predict
            }
        )

        end_time = time.perf_counter()

        return {
            "model": self.model_name,
            "prompt": prompt,
            "output": response.message.content,
            "temperature": temperature,
            "seed": seed,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "num_predict": num_predict,
            "latency_seconds": round(
                end_time - start_time, 4
            )
        }

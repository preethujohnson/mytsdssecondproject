from fastapi import FastAPI, File, Form, UploadFile
import pandas as pd
import openai
import os

app = FastAPI()

# Set your OpenAI API Key (if using GPT for answers)
openai.api_key = " "

@app.post("/api/")
async def solve_question(question: str = Form(...), file: UploadFile = None):
    if file:
        # If a CSV file is uploaded, process it
        df = pd.read_csv(file.file)
        if "answer" in df.columns:
            return {"answer": df["answer"].iloc[0]}
        else:
            return {"error": "No 'answer' column in the uploaded CSV file."}
    else:
        # If no file, use LLM to answer
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": question}]
        )
        return {"answer": response["choices"][0]["message"]["content"]}


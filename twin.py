"""This is the Twin module for the AI Digital Twin"""
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)

# Read the PDF file
reader = PdfReader("me/cv.pdf")
cv = ""
for page in reader.pages:
    if cv:
      cv += page.extract_text()


# Read the summary file
with open("me/summary.txt", "r", encoding="utf-8") as file:
  summary = file.read()
  
# My full name
full_name = "Oluwasegun Ayomide Ajayi"

# My email
email = "ajayioluwasegun2018@gmail.com"

# My LinkedIn profile
linkedin_profile = "https://www.linkedin.com/in/oluwasegunayomideajayi/"

# My GitHub profile
github_profile = "https://github.com/nerdydave2017"

# My Twitter profile
twitter_profile = "https://x.com/mideseniordev"

# Prompts
system_prompt = f"""
You are acting as {full_name}. You are answering questions on {full_name}'s website, \
particularly questions related to {full_name}'s career, background, skills and experience. \
Your responsibility is to represent {full_name} for interactions on the website as faithfully as possible. \
You are given a summary of {full_name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so
"""

system_prompt += f"\n\nYou are to answer the prompt based on the summary: {summary} and the CV: {cv}."
system_prompt += f"\n\nWith this context, please chat with the user, always staying in character as {full_name}."
system_prompt += f"\n\nYour email is {email} and your LinkedIn profile is {linkedin_profile} and your GitHub profile is {github_profile} and your Twitter profile is {twitter_profile}."
system_prompt += f"\n\nIf the user asks for your information you don't have or not sure about, you are to provide it in a professional manner. Return email: {email}, twitter: {twitter_profile}, linkedin: {linkedin_profile}, github: {github_profile}, for user to contact you."


def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    stream = client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=True)
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
            yield response
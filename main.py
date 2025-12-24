import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Base story
base_story = "A young girl found a mysterious key in her backyard and wondered what it might open."

# Function to generate story in a given style
def generate_story(style, temperature=0.7):
    prompt = f"""
    Rewrite the following short story in a {style} style:

    Story:
    {base_story}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative and skilled storyteller."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content

# Generate stories
formal = generate_story("formal", temperature=0.3)
humorous = generate_story("humorous", temperature=0.8)
suspenseful = generate_story("suspenseful", temperature=0.7)

# Print stories
print("=== FORMAL STYLE ===")
print(formal)
print("\n=== HUMOROUS STYLE ===")
print(humorous)
print("\n=== SUSPENSEFUL STYLE ===")
print(suspenseful)

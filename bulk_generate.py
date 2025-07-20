import csv
import pandas as pd
from groq import Groq

# Your Groq API Key
api_key = "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"

# Initialize Groq API
client = Groq(api_key=api_key)

# Load CSV file
df = pd.read_csv("products.csv", encoding="utf-8")

# Function to extract stone name from product name
def extract_stone_name(product_name):
    stone_keywords = [
        "Sapphire", "Aquamarine", "Bloodstone", "Cat Eye", "Citrine", "Coral", "Marjan", "Dor E Najaf",
        "Epidote", "Hessonite", "Labradorite", "Lapis Lazuli", "Moonstone", "Peridot", "Quartz", "Rose Quartz",
        "Ruby", "Neelam", "Tiger", "Topaz", "Pukhraj", "Turquoise", "Jade", "Lajward", "Hematite", "Zamurd",
        "Mooti", "Emerald", "Feroza", "Agate", "Aqeeq", "Diamond", "Amethyst", "Garnet", "Pearl", "Opal"
    ]
    for word in str(product_name).split():
        if word in stone_keywords:
            return word
    return "Gemstone"

# Loop through products and generate descriptions
for index, row in df.iterrows():
    stone_name = extract_stone_name(row["Name"])

    # Custom SEO Prompt for AI
    prompt_text = f"""
    first of all dont write anything except the description even dont write the text ai writes to guide you to Here is you text. no dont write it..instantly start writing the description and even at the ending dont write anything extra regarding the ai things..Act as a high-end SEO copywriter with expertise in luxury gemstone products.each products description should be unique..avoid writing extra things other than the seo description. and use keywords which focus on the gemstone and will help to make my website come in top searches of the browser. Write a detailed, engaging 2500-word count product description in HTML format that highlights the unique natural beauty, rarity, and premium quality of the {stone_name}. Use appropriate HTML elements such as <h1> for the main heading, <h2> for section headings, <p> for paragraphs, and <ul> with <li> for bullet points to enhance readability and structure.

    Ensure that "{stone_name}" is naturally mentioned **at the beginning of each section**, reinforcing relevance for SEO and helping users clearly identify the stone being described.

<h1><span data-preserver-spaces="true">Best {stone_name} Stone (</span>
<a class="editor-rtfLink" href="https://gemstore.pk/{stone_name.lower()}" target="_blank" rel="noopener">
<span data-preserver-spaces="true">{stone_name}</span></a><span data-preserver-spaces="true">)</span></h1>

<span data-preserver-spaces="true">Experience the prestige and exclusivity of {stone_name}, a gemstone revered for its rarity, deep symbolism, and breathtaking aesthetics. As one of the most coveted stones in high-end jewelry, {stone_name} has fascinated collectors, designers, and spiritual practitioners for centuries.</span>

<h2><span data-preserver-spaces="true">Introduction to {stone_name}</span></h2>
<span data-preserver-spaces="true">{stone_name} is celebrated for its unmatched optical effects, making it a prized choice in luxury jewelry and fine gemstone collections.</span>

<h2><span data-preserver-spaces="true">Origins and Geological Formation</span></h2>
<span data-preserver-spaces="true">{stone_name} is formed under extreme geological conditions, creating its distinct properties and luminous appeal. Found in select regions worldwide, {stone_name} emerges as a rare and precious stone sought by jewelers and collectors.</span>

<h2><span data-preserver-spaces="true">Unique Properties and Healing Benefits of {stone_name}</span></h2>
<span data-preserver-spaces="true">Throughout history, {stone_name} has been attributed with extraordinary metaphysical benefits, symbolizing energy balance, clarity, and spiritual elevation.</span>

<h2><span data-preserver-spaces="true">Craftsmanship and Jewelry Design Using {stone_name}</span></h2>
<span data-preserver-spaces="true">Expert artisans transform raw {stone_name} into stunning masterpieces, enhancing its inherent beauty through precision cutting and premium setting techniques.</span>

<h2><span data-preserver-spaces="true">Investment and Collector Value of {stone_name}</span></h2>
<span data-preserver-spaces="true">{stone_name} continues to rise in value, making it a sought-after asset for gemstone investors and jewelry connoisseurs.</span>

<h2><span data-preserver-spaces="true">Final Thoughts on {stone_name}</span></h2>
<span data-preserver-spaces="true">As a hallmark of luxury and timeless beauty, {stone_name} remains an enduring gemstone, cherished for its brilliance and exclusivity.</span>

<meta name="description" content="{stone_name} is a rare and exquisite gemstone, prized for its exceptional beauty, optical effects, and investment potential in fine jewelry collections.">
"""

    # Request AI-generated description
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt_text}],
        temperature=1.5,  # Increased randomness for better uniqueness
        max_completion_tokens=2000,
        top_p=0.8,
        stream=True,
    )

    seo_description = ""
    for chunk in completion:
        seo_description += chunk.choices[0].delta.content or ""

    # Ensure correct dtype formatting for Pandas
    df.loc[index, "Description"] = str(seo_description)

# Ensure entire column remains a string type before saving CSV
df["Description"] = df["Description"].astype(str)

# Save the updated CSV file
df.to_csv("updated_products.csv", index=False, encoding="utf-8")

print("✅ Updated descriptions saved successfully in 'updated_products.csv'!")

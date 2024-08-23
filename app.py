import streamlit as st
import openai
import pandas as pd
import json
import concurrent.futures
from streamlit_lottie import st_lottie
import requests
import random
from streamlit_javascript import st_javascript

# Custom CSS for improved styling
custom_css = """
<style>
    .stApp {
        background-color: #fff;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #000;
    }
    .stExpander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .persona-card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .persona-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
    }
    .icon {
        vertical-align: middle;
        margin-right: 0.5rem;
    }
</style>
"""

st.set_page_config(page_title="Search Intent Analysis", layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)

# Load FontAwesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def chat_completion(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def parse_json_response(response):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the response
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != -1:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            raise ValueError("Unable to parse JSON from the response")

# Load Lottie animation
lottie_url = "https://lottie.host/d4f7af8c-6084-4c68-b661-dbebd139a361/wMwddV5x6i.json"
lottie_json = load_lottieurl(lottie_url)

st.title("🔍 Search Intent & Motivation analysis")

# Sidebar for inputs
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
keyword = st.sidebar.text_input("Enter the keyword for analysis")
num_personas = st.sidebar.slider("Number of personas to generate", 1, 5, 3)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 How does it work?")
    st.write("This Python-based tool leverages AI to generate detailed marketing personas and insights tailored to specific keywords. It automates the process of understanding user intent and creating targeted marketing strategies by generating personas and addressing key consumer questions and concerns.")

with col2:
    st_lottie(lottie_json, height=200)

if api_key and keyword:
    openai.api_key = api_key

    with st.spinner("Analyzing search intent..."):
        # Chat completion for identifying intent
        messages = [
            {"role": "system", "content": "You are a helpful assistant that analyzes search intent."},
            {"role": "user", "content": f"What is the most likely search intent when searching for '{keyword}'?"}
        ]
        intent = chat_completion(messages)

    st.subheader("🧠 Search Intent")
    st.info(intent)

    with st.spinner("Generating personas..."):
        # Chat completion for persona generation
        messages = [
            {"role": "system", "content": "You are an expert in marketing and consumer behavior, specifically in persona generation."},
            {"role": "user", "content": f"""Given that the user is using the keyword: {keyword} with the intent of: {intent}, generate {num_personas} different but unique personas in JSON format. Each persona should have the following structure:

            {{
              "demographics": {{
                "name": "string",
                "age_range": "string",
                "gender": "string",
                "marital_status": "string",
                "income": "string",
                "education": "string"
              }},
              "psychographics": {{
                "personality_traits": ["string"],
                "values_and_beliefs": ["string"],
                "interests_and_hobbies": ["string"],
                "lifestyle_factors": ["string"]
              }},
              "behavior_and_decision_making": {{
                "information_sources": ["string"],
                "purchase_decision_influences": ["string"],
                "key_behaviors_and_habits": ["string"]
              }}
            }}

            Provide the response as a valid JSON array of persona objects. Do not include any text before or after the JSON array.
            """}
        ]
        personas_response = chat_completion(messages)
        try:
            personas_json = parse_json_response(personas_response)
        except ValueError as e:
            st.error(f"Error parsing personas: {str(e)}")
            st.stop()

    st.subheader("👥 Generated Personas")
    for idx, persona in enumerate(personas_json, 1):
        with st.expander(f"Persona {idx}: {persona['demographics']['name']}"):
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                avatar_url = f"https://api.dicebear.com/9.x/personas/png?seed={persona['demographics']['name']}"
                st.image(avatar_url, width=150)
            with col2:
                st.subheader("📊 Demographics")
                for key, value in persona['demographics'].items():
                    icon = {
                        "name": "fas fa-user",
                        "age_range": "fas fa-birthday-cake",
                        "gender": "fas fa-venus-mars",
                        "marital_status": "fas fa-ring",
                        "income": "fas fa-dollar-sign",
                        "education": "fas fa-graduation-cap"
                    }.get(key, "fas fa-info-circle")
                    st.markdown(f'<i class="{icon} icon"></i> **{key.replace("_", " ").title()}:** {value}', unsafe_allow_html=True)
            with col3:
                st.subheader("🧠 Psychographics")
                for key, value in persona['psychographics'].items():
                    icon = {
                        "personality_traits": "fas fa-brain",
                        "values_and_beliefs": "fas fa-heart",
                        "interests_and_hobbies": "fas fa-palette",
                        "lifestyle_factors": "fas fa-home"
                    }.get(key, "fas fa-info-circle")
                    st.markdown(f'<i class="{icon} icon"></i> **{key.replace("_", " ").title()}:**', unsafe_allow_html=True)
                    st.write(", ".join(value))
            
            st.subheader("🛒 Behavior and Decision Making")
            for key, value in persona['behavior_and_decision_making'].items():
                icon = {
                    "information_sources": "fas fa-book",
                    "purchase_decision_influences": "fas fa-chart-line",
                    "key_behaviors_and_habits": "fas fa-clock"
                }.get(key, "fas fa-info-circle")
                st.markdown(f'<i class="{icon} icon"></i> **{key.replace("_", " ").title()}:**', unsafe_allow_html=True)
                st.write(", ".join(value))

    # Questions for each Persona
    questions = [
        f"What are the most important features or benefits someone looks for when searching for {keyword}?",
        f"What are the most common questions or concerns before making a purchase related to {keyword}?",
        f"What are the biggest challenges someone faces when looking for the right product or service related to {keyword}?",
        f"How does the person typically research their options related to {keyword} and where do they look for information?",
        f"What are the most effective ways to convince this person to make a purchase related to {keyword}?",
        f"What are the most common objections when considering a purchase related to {keyword} and how can they be addressed?",
        f"What are some unique or unconventional ways to market products or services related to {keyword}?",
        f"How does the person typically compare different products or services related to {keyword} and what factors do they consider?",
        f"What are the most common misconceptions or misunderstandings related to {keyword} and how can they be corrected?",
        f"What are some emerging trends or developments in the {keyword} market and how can they be leveraged for an advantage?"
    ]

    with st.spinner("Analyzing personas..."):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = []
            for persona in personas_json:
                for question in questions:
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant that analyzes consumer behavior."},
                        {"role": "user", "content": f"Given this persona: {json.dumps(persona)}\n\nAnswer the following question: {question}"}
                    ]
                    task = executor.submit(chat_completion, messages)
                    tasks.append((persona['demographics']['name'], question, task))
            for persona_name, question, task in tasks:
                answer = task.result()
                results.append({
                    "Persona": persona_name,
                    "Question": question,
                    "Answer": answer
                })

    st.subheader("🔬 Persona Motivation Analysis")
    df = pd.DataFrame(results)
    for persona in df['Persona'].unique():
        with st.expander(f"Analysis for {persona}"):
            persona_df = df[df['Persona'] == persona]
            for _, row in persona_df.iterrows():
                st.markdown(f"**<i class='fas fa-question-circle'></i> {row['Question']}**", unsafe_allow_html=True)
                st.markdown(f"<i class='fas fa-comment-alt'></i> {row['Answer']}", unsafe_allow_html=True)
                st.markdown("---")

    # Download button for CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download analysis as CSV",
        data=csv,
        file_name="search_intent_analysis.csv",
        mime="text/csv",
    )
else:
    st.warning("Please enter your OpenAI API Key and a keyword to start the analysis.")

# Add a footer
st.markdown("""
<footer style='text-align: center; padding: 20px; margin-top: 50px;'>
    <p>Created with ❤️ by Andreas</p>
</footer>
""", unsafe_allow_html=True)
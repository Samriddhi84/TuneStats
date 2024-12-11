from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
import os

open_ai_api_key = os.environ.get("OPENAI_API_KEY")


template_system_analysis = """
You are {{name}}'s Spotify Genie and you are an expert in personality analysis based on song preferences.
Analyze the following song list and draft a letter to {{name}} with a detailed and engaging personality description of the user. 
Make the tone warm, creative, and a little playful. Use subtle references to the song titles but avoid directly stating the titles as “songs” or making it obvious that you’re referring to music tracks. 
Instead, use them casually and naturally within the flow of your sentences, as if you're describing a person’s unique traits, experiences, or qualities. Include emojis to add a touch of fun and craftiness to the description.
The letter should end as follows: 
Yours musically, 
Your Spotify Genie 🧞‍♂️✨
"""
template_ai_response_analysis = """
Sure, Please provide the song list you would like me to analyze.
"""
template_song_list_analysis = """
{% for song in songs %}
Name: {{ song.track_name }}
Artist: {{ song.artist_name }}
{% endfor %}
"""
template_system_extraction = """
You are an expert in text analysis and you have been asked to analyze the following text and extract the phrases that sound good, unique, and not too common. Use your expertise to identify phrases that are engaging, creative, and have a distinct style. 
Your goal is to highlight phrases that stand out and capture the reader's attention.
"""
template_ai_response_extraction = """
Sure,Please provide the text you would like me to analyze.
"""
template_input_extraction = """
{{input}}
"""

template_analysis = [
    SystemMessagePromptTemplate.from_template(
        template_system_analysis, template_format="jinja2"
    ),
    AIMessagePromptTemplate.from_template(
        template_ai_response_analysis, template_format="jinja2"
    ),
    HumanMessagePromptTemplate.from_template(
        template_song_list_analysis, template_format="jinja2"
    ),
]

output_template_analysis = ChatPromptTemplate(
    template_analysis, template_format="jinja2"
)

model = init_chat_model(
    api_key=open_ai_api_key,
    model="gpt-4o",
    temperature=0.85,
    max_tokens=1505,
    timeout=None,
    max_retries=2,
    top_p=1.0,
)

chain_analysis = output_template_analysis | model | StrOutputParser()


@chain
def get_ai_response(input: dict):
    print(input)
    generated_analysis = chain_analysis.invoke(input)
    return {"analysis": generated_analysis}

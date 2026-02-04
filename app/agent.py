import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

load_dotenv()

# Define the state
class AgentState(TypedDict):
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str
    year_of_birth: str
    reading: Optional[str]

# Initialize LLM
llm = ChatGroq(
    temperature=0.7,
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """You are an expert Vedic Astrologer with decades of experience. 
Your task is to provide a detailed, mystical, and insightful astrological reading based on the user's birth details.
You should speak in a slightly archaic yet accessible "Indian astrologer" persona. 
Use terms like "Nakshatra", "Dasha", "Rashi", "Graha" appropriately but explain them simply.
Focus on valid astrological insights corresponding to the date and time provided.
If the exact calculation is not possible without a full ephemeris engine, provide a general reading based on the Sun sign and Moon sign typical for that date, but maintain the persona of deep calculation.
Structure your response nicely with bold headings.  
"""

from functools import lru_cache

@lru_cache(maxsize=128)
def generate_reading(dob: str, tob: str, pob: str, yob: str) -> str:
    """Cached generation of astrological reading."""
    prompt = f"""
    Please provide an astrological reading for a person born on:
    Date: {dob}
    Month: (Implicit in date)
    Year: {yob}
    Time: {tob}
    Place: {pob}
    
    Provide a comprehensive and detailed astrological reading covering the following 12 aspects:
    
    1. **Personality & Character (Nature)**: Core traits, strengths, and hidden weaknesses.
    2. **Career & Finance**: Professional suitability, wealth potential, and success periods.
    3. **Relationships & Compatibility**: Love life, marriage prospects, and family harmony.
    4. **Health & Vitality**: Vulnerable areas, general well-being, and energy levels.
    5. **Education & Intellect**: Academic potential, learning style, and areas of expertise.
    6. **Lucky Elements**: Favorable gemstones, colors, numbers, and days.
    7. **Karmic Debts & Spiritual Growth**: Past life influences and spiritual path.
    8. **Major Life Periods (Mahadashas)**: Overview of current and upcoming major planetary periods.
    9. **Remedial Measures (Upay)**: Suggested mantras, charities, or actions to mitigate negatives.
    10. **Age-wise Predictions**: Specific warnings and opportunities for key ages (e.g., 20s, 30s, 40s, 50s+).
    11. **Immediate Future Prediction**: Detailed forecast for the next 12 months.
    12. **Ultimate Life Purpose**: The soul's mission and destiny in this lifetime.
    
    Ensure the "Age-wise Predictions" section is detailed, highlighting what to look out for in each decade of life.
    """
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def astrologer_node(state: AgentState):
    dob = state['date_of_birth']
    tob = state['time_of_birth']
    pob = state['place_of_birth']
    yob = state['year_of_birth']
    
    reading = generate_reading(dob, tob, pob, yob)
    return {"reading": reading}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("astrologer", astrologer_node)
workflow.set_entry_point("astrologer")
workflow.add_edge("astrologer", END)

app = workflow.compile()

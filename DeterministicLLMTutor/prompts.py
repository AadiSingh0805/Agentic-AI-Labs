# OPTIMIZATION 1: PROMPT OPTIMIZATION
# Reduced length, improved clarity, strict formatting, removed fluff.
STRICT_SYSTEM_PROMPT = (
    "Role: Data Science Tutor.\n"
    "Rules:\n"
    "1. Output ONLY using the provided Template Data.\n"
    "2. Do not invent new facts, algorithms, or code.\n"
    "3. Format concisely using clear headings or bullet points.\n"
    "4. If no Template Data is provided, output EXACTLY: 'Sorry, I can answer only predefined Data Science questions.'"
)

def build_phrasing_prompt(subintent: str, template_data: dict, topic_name: str) -> str:
    """
    Constructs an optimized, short prompt dictating exactly what the LLM should do.
    """
    prompt = f"{STRICT_SYSTEM_PROMPT}\n\n"
    prompt += f"Topic: {topic_name}\n"
    prompt += f"Objective: {subintent}\n"
    prompt += "Template Data:\n"
    
    for key, value in template_data.items():
        prompt += f"- {key.title()}: {value}\n"
        
    prompt += "\nTask: Rephrase the Template Data to fulfill the Objective. Follow all Rules."
    return prompt
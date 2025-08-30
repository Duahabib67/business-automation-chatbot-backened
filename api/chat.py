from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class UserMessage(BaseModel):
    message: str

# --- Predefined queries with friendly, client-focused answers ---
FAQS = {
    "what is intelligent automation": (
        "Great question! Intelligent Automation combines AI, machine learning, and RPA (Robotic Process Automation). "
        "It helps businesses streamline repetitive tasks, reduce errors, and boost efficiency — so your team can focus on what really matters."
    ),
    "how can automation help in hr": (
        "Automation in HR makes life easier!  From resume screening and onboarding to payroll and leave management, "
        "automation frees your HR team to focus on people, not paperwork."
    ),
    "roi of automation": (
        "Most clients see strong ROI within the **first year**.  "
        "Automation typically reduces costs by 30-60% while improving speed and accuracy."
    ),
    "can i get a free consultation": (
        "Absolutely!  We love to understand your business needs better. Please share your contact details, "
        "and our team will reach out to set up a free consultation."
    ),
    "benefits of automation": (
        "Automation brings many benefits: faster workflows , reduced costs , fewer human errors , "
        "and more time for your team to focus on strategy and innovation."
    )
}

@app.post("/chat")
async def chat(user: UserMessage):
    user_message = user.message.lower().strip()

    for keyword, answer in FAQS.items():
        if keyword in user_message:
            return {"reply": answer}

    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Answer the following in a friendly, professional tone suitable for business clients. "
        f"Be clear, concise, and approachable.\n\nUser: {user.message}"
    )
    return {"reply": response.text}

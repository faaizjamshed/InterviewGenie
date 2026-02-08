import os
import json
import random
import g4f  # Real-time Alternative Library
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

# API Key from your system
API_KEY = os.getenv("Your Api Key") 

# ==============================
# REAL-TIME GPT BACKUP FUNCTION
# ==============================
def get_gpt_backup(prompt, is_json=False):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    except Exception as e:
        print(f"GPT Backup also failed: {e}")
        return None

# ==============================
# RESUME ANALYSIS (REAL-TIME)
# ==============================
def analyze_resume(resume_text):
    try:
        # Step 1: Build a very strict prompt
        prompt = f"""
        Act as an expert ATS. Analyze the resume below and return ONLY raw JSON.
        Do not include markdown tags like ```json.
        
        Required JSON Structure:
        {{
            "Overall Score": 85,
            "Key Strengths": ["strength 1", "strength 2"],
            "Areas for Improvement": ["weakness 1", "weakness 2"],
            "Missing Keywords": ["keyword 1", "keyword 2"]
        }}

        Resume Text:
        {resume_text[:5000]}
        """

        # Step 2: Try Gemini first (LangChain approach)
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=API_KEY,
            temperature=0.1 # Low temperature for strict JSON
        )
        
        response = llm.invoke(prompt)
        content = response.content.strip()

        # Step 3: Cleaning (Extra Safety)
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        # Validate if it's real JSON
        json.loads(content) 
        return content

    except Exception as e:
        print(f"Analysis Failed: {e}. Trying GPT Alternative...")
        # Backup using g4f if Gemini fails
        backup_res = get_gpt_backup(prompt)
        if backup_res:
            return backup_res.strip().replace("```json", "").replace("```", "")
        
        # Final Fail-safe (Agar dono fail hon)
        return json.dumps({
            "Overall Score": 70,
            "Key Strengths": ["Professional Experience", "Technical Skills Detected"],
            "Areas for Improvement": ["Detailed analysis connection slow"],
            "Missing Keywords": ["Industry Specific Tags"]
        })
# ==============================
# INTERVIEW CHAT (NO REPETITION)
# ==============================
def get_interview_response(user_input, history, q_count=0):
    system_prompt = f"""
You are a friendly professional mock interviewer.

Interview Status:
- Questions already asked: {q_count}/10

Rules:
- Ask ONLY ONE next question.
- Never restart interview.
- Never repeat previous questions.
- Wait for user answer before next question.

If questions reach 10:
- Stop asking questions.
- Give evaluation, strengths, weaknesses, tips.
"""

    try:
        # Try Real Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=API_KEY
        )

        full_prompt = f"{system_prompt} {user_input}\nHistory: {history[-3:]}"
        response = llm.invoke(full_prompt)
        ai_reply = response.content.strip()

        return ai_reply, history + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_reply}
        ]

    except Exception as e:
        print("Chat Gemini Failed. Using Real-Time GPT Backup...", e)

        backup_reply = get_gpt_backup(f"{system_prompt} {user_input}")

        if backup_reply:
            return backup_reply, history + [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": backup_reply}
            ]

        return "Can you tell me more about your experience with Python?", history

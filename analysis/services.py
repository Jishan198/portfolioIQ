import json
from google import genai
from django.conf import settings
import base64
from google.genai import types


def generate_risk_analysis(ticker, current_price, company_name):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
    You are an expert financial analyst advising a retail investor on {ticker} ({company_name}) currently at Rs.{current_price}.
    Speak in simple plain English. No heavy jargon.

    You MUST respond with ONLY a valid JSON object, no markdown, no extra text.
    Use this exact structure:
    {{
        "risk_score": 7,
        "score_explanation": "A one sentence explanation of the score.",
        "key_risks": [
            "Short point about sector risk",
            "Short point about debt or macro risk"
        ],
        "behavioral_traps": [
            "Short point about why retail investors lose money here"
        ],
        "verdict": "A punchy, one-sentence final takeaway."
    }}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        print(f"DEBUG Gemini response: {response.text}")
        cleaned = response.text.strip().replace('```json', '').replace('```', '').strip()
        json.loads(cleaned)  # validate it's proper JSON
        return cleaned

    except Exception as e:
        print(f"Gemini API Error: {e}")
        fallback = {
            "risk_score": 0,
            "score_explanation": "Analysis unavailable right now.",
            "key_risks": ["Gemini rate limit hit or API error. Try again in 1 minute."],
            "behavioral_traps": ["Retrying too fast is a common trap."],
            "verdict": f"Error: {str(e)[:100]}"
        }
        return json.dumps(fallback)


def generate_vision_analysis(base64_data, mime_type):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = """
    Analyze this mutual fund/stock portfolio screenshot.
    Speak in simple, plain English. Explain it to a beginner.

    You MUST respond with ONLY a valid JSON object, no markdown, no extra text.
    Use this exact structure:
    {
        "risk_score": 5,
        "score_explanation": "Simple 1-sentence explanation of the score.",
        "key_risks": ["Simple point 1", "Simple point 2"],
        "behavioral_traps": ["Simple point 1"],
        "verdict": "A simple, clear final advice sentence."
    }
    """

    try:
        image_bytes = base64.b64decode(base64_data)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt
            ]
        )
        print(f"DEBUG Vision response: {response.text}")
        cleaned = response.text.strip().replace('```json', '').replace('```', '').strip()
        json.loads(cleaned)  # validate
        return cleaned

    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        fallback = {
            "risk_score": 0,
            "score_explanation": "Vision analysis failed.",
            "key_risks": ["Error reading image."],
            "behavioral_traps": [str(e)[:100]],
            "verdict": "Try uploading a clearer screenshot."
        }
        return json.dumps(fallback)
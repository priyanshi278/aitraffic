import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def rule_based_summary(routes_analysis: list) -> dict:
    best_route = min(routes_analysis, key=lambda r: r["score"])

    reasons = []

    if best_route["incident_count"] == 0:
        reasons.append("no reported incidents")
    else:
        reasons.append(f"only {best_route['incident_count']} incidents")

    if best_route["congestion_level"] == "Low":
        reasons.append("low congestion")
    elif best_route["congestion_level"] == "Medium":
        reasons.append("moderate congestion")

    reasons.append(
        f"and estimated travel time is ({best_route['avg_time_min']} minutes)"
    )

    explanation = "This route was selected because it has " + ", ".join(reasons) + "."

    return {
        "recommended_route": best_route["via"],
        "explanation": explanation
    }


def groq_summary(routes_analysis: list) -> dict:
    if not GROQ_API_KEY:
        return {
            "available": False,
            "summary": "AI analysis not available (API key missing)."
        }

    try:
        from groq import Groq 

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an AI Traffic & Transport Intelligence System.

IMPORTANT RULE:
- LOWER score means BETTER route
- Score is a penalty score based on congestion, incidents, and time
- Always recommend the route with the LOWEST score

Your task:
1. Identify the route with the lowest score
2. Recommend ONLY that route
3. Briefly explain why (incidents, congestion, time)

Route Data (JSON):
{routes_analysis}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=150      

        )

        return {
            "available": True,
            "summary": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "available": False,
            "summary": f"AI analysis failed gracefully: {str(e)}"
        }

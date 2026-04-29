"""AI integration for SpectraLens field analysis."""

import json
import os
import re
import urllib.error
import urllib.request
import anthropic


SYSTEM_PROMPT = """You are an expert agronomist and remote sensing specialist. You analyze \
hyperspectral drone imagery of crop fields and provide actionable insights \
to farmers and agri-tech companies. You communicate findings clearly, \
specifically, and without jargon. Always be direct about what you see.

You MUST respond with valid JSON only — no markdown, no code fences, no extra text."""


def _strip_code_fences(text):
    """Remove markdown code fences from response text."""
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def _validate_report(data):
    """Ensure the AI response has all required fields with correct types."""
    defaults = {
        "executive_summary": "Analysis complete. See zone details below.",
        "overall_field_health": 50,
        "zones": [],
        "immediate_actions": [],
        "estimated_yield_impact": "Unable to determine",
        "confidence": "Low",
        "next_scan_recommendation": "Re-scan recommended",
    }
    for key, default in defaults.items():
        if key not in data:
            data[key] = default
    # Ensure overall_field_health is a number
    if not isinstance(data["overall_field_health"], (int, float)):
        data["overall_field_health"] = 50
    return data


def _available_provider():
    """Return the first configured AI provider."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return None


def _call_anthropic(user_prompt):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


def _call_gemini(user_prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 1500,
            "responseMimeType": "application/json",
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    candidates = result.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no response candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(part.get("text", "") for part in parts)


async def interpret_field(zone_stats: dict, wavelengths: list, ndvi_stats: dict) -> dict:
    """
    Call the configured AI API with structured agronomic context.
    Returns parsed JSON analysis report.
    """
    user_prompt = f"""Analyze the following hyperspectral drone imagery data from a corn field and provide a detailed crop health report.

## Field Overview
- Image size: 100x100 pixels, 60 spectral bands (400-1000nm, 10nm steps)
- Sensor: VNIR hyperspectral (simulated drone capture)
- Overall NDVI: mean={ndvi_stats['overall_mean_ndvi']}, min={ndvi_stats['overall_min_ndvi']}, max={ndvi_stats['overall_max_ndvi']}

## Zone-by-Zone Analysis

{json.dumps(zone_stats['zones'], indent=2)}

## Wavelengths (nm)
{wavelengths[:10]}... (60 bands from 400nm to 990nm)

## Task
Based on this spectral data, return a JSON object with exactly this structure:
{{
  "executive_summary": "2-3 sentence plain English overview of field health",
  "overall_field_health": <number 0-100>,
  "zones": [
    {{
      "name": "Zone A (NW quadrant)",
      "health_status": "Healthy | Nitrogen Deficient | Water Stressed | Pest Damage",
      "severity": "None | Mild | Moderate | Severe",
      "ndvi": <float>,
      "area_percentage": 25,
      "finding": "one sentence finding",
      "recommendation": "one sentence action item"
    }}
  ],
  "immediate_actions": ["action 1", "action 2", "action 3"],
  "estimated_yield_impact": "e.g. 15-20% reduction in affected areas",
  "confidence": "High | Medium | Low",
  "next_scan_recommendation": "e.g. Re-scan in 2 weeks to monitor nitrogen response"
}}

Return ONLY the JSON object, nothing else."""

    provider = _available_provider()
    if not provider:
        return _validate_report({"executive_summary": "No AI API key configured. Add ANTHROPIC_API_KEY or GEMINI_API_KEY to your .env file."})

    try:
        if provider == "anthropic":
            response_text = _call_anthropic(user_prompt)
        else:
            response_text = _call_gemini(user_prompt)
    except anthropic.APIConnectionError:
        return _validate_report({"executive_summary": "Could not connect to AI service. Check your internet connection."})
    except anthropic.AuthenticationError:
        return _validate_report({"executive_summary": "Invalid API key. Check ANTHROPIC_API_KEY in your .env file."})
    except anthropic.RateLimitError:
        return _validate_report({"executive_summary": "API rate limit reached. Please try again in a moment."})
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return _validate_report({"executive_summary": "Invalid API key. Check GEMINI_API_KEY in your .env file."})
        if e.code == 429:
            return _validate_report({"executive_summary": "API rate limit reached. Please try again in a moment."})
        return _validate_report({"executive_summary": f"Gemini API request failed with HTTP {e.code}."})
    except urllib.error.URLError:
        return _validate_report({"executive_summary": "Could not connect to AI service. Check your internet connection."})
    except Exception as e:
        return _validate_report({"executive_summary": f"AI analysis failed: {str(e)}"})

    cleaned = _strip_code_fences(response_text)

    try:
        data = json.loads(cleaned)
        return _validate_report(data)
    except json.JSONDecodeError:
        return _validate_report({
            "executive_summary": cleaned[:500] if cleaned else "AI returned an unparseable response.",
        })

"""Claude API integration for SpectraLens field analysis."""

import json
import anthropic


SYSTEM_PROMPT = """You are an expert agronomist and remote sensing specialist. You analyze \
hyperspectral drone imagery of crop fields and provide actionable insights \
to farmers and agri-tech companies. You communicate findings clearly, \
specifically, and without jargon. Always be direct about what you see.

You MUST respond with valid JSON only — no markdown, no code fences, no extra text."""


async def interpret_field(zone_stats: dict, wavelengths: list, ndvi_stats: dict) -> dict:
    """
    Call Claude API with structured agronomic context.
    Returns parsed JSON analysis report.
    """
    user_prompt = f"""Analyze the following hyperspectral drone imagery data from a corn field and provide a detailed crop health report.

## Field Overview
- Image size: 100×100 pixels, 60 spectral bands (400–1000nm, 10nm steps)
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

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = message.content[0].text.strip()

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        # Remove first and last lines (fences)
        lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "executive_summary": response_text[:500],
            "overall_field_health": 50,
            "zones": [],
            "immediate_actions": ["Review raw data manually"],
            "estimated_yield_impact": "Unable to determine",
            "confidence": "Low",
            "next_scan_recommendation": "Re-scan immediately",
            "raw_response": response_text,
        }

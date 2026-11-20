from google import genai
from google.genai import types

client = genai.Client()          # reads GEMINI_API_KEY automatically
MODEL = "gemini-3.8-flash"       # use the model name that worked for you

SYSTEM = """You are an electronics maintenance engineer reviewing a 24V DC device.
Normal ranges: temperature 0-70 C, voltage 22-26 V, current 0-6 A.

Reply in exactly this Markdown format, with a blank line between sections:

### Status
Normal, Warning or Critical

### What is wrong
Which reading is out of range (1-2 lines)

### Possible causes
- 2-3 bullets

### Troubleshooting steps
- 3 bullets

### Preventive maintenance
- 3 bullets

Base your answer mainly on the LATEST reading. Do not invent values."""


def analyze(df):
    last = df.iloc[-1]
    recent = df.tail(5)[["temperature", "voltage", "current"]].round(2).to_string(index=False)

    prompt = (
        f"LATEST reading: temperature={last.temperature} C, "
        f"voltage={last.voltage} V, current={last.current} A.\n\n"
        f"Last 5 readings (oldest to newest, for trend only):\n{recent}"
    )

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            max_output_tokens=1200,
            http_options=types.HttpOptions(timeout=30000),  # 30 seconds
        ),
    )
    return resp.text
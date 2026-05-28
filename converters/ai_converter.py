import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

# LOAD LOCAL .env FILE

load_dotenv()

# GET API KEY
# Streamlit Cloud → st.secrets
# Local PC → .env

try:

    api_key = st.secrets["GOOGLE_API_KEY"]

except:

    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

# CONFIGURE GEMINI

genai.configure(
    api_key=api_key
)

# MODEL

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

# AI CONVERTER

def ai_convert_code(
    code,
    source_language
):

    try:

        prompt = f"""
You are an expert software migration engineer.

Convert this {source_language} code
into clean optimized Python.

Rules:
- Return ONLY Python code
- Preserve logic accurately
- Keep output concise and clean
- Do NOT add test cases
- Do NOT add example usage
- Do NOT add markdown formatting
- Use short one-line comments only where useful
- Keep functions compact and readable

CODE:
{code}
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
# AI Conversion Failed

{str(e)}
"""

# AI EXPLAINER

def explain_conversion(
    original_code,
    converted_code
):

    try:

        prompt = f"""
Explain this code conversion briefly.

ORIGINAL:
{original_code}

CONVERTED:
{converted_code}

Explain:
1. What changed
2. Logic preserved
3. Optimizations

Keep explanation concise.
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
AI explanation unavailable.

Reason:
{str(e)}
"""

# HYBRID OPTIMIZER

def hybrid_optimize(
    original_code,
    offline_converted_code
):

    try:

        prompt = f"""
You are an expert Python optimization engineer.

Optimize this converted Python code.

Requirements:
- Preserve logic
- Improve readability
- Keep output concise
- Add short one-line comments only if useful
- Do NOT add test cases
- Do NOT add example usage
- Return ONLY Python code

ORIGINAL CODE:
{original_code}

RULE-BASED OUTPUT:
{offline_converted_code}
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
# Hybrid Optimization Failed

{str(e)}
"""
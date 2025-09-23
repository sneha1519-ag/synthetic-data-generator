import google.generativeai as genai
import os
import json
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
import pandas as pd
import ast
import re

# Load environment variables from .env file
load_dotenv()

# In a real application, we would get this from environment variables
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# List of available models
model = genai.GenerativeModel('gemini-1.5-pro')

def extract_json_from_response(response_text: str) -> str:
    """Extract JSON data from the model response text."""
    # Find content between triple backticks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
    if json_match:
        return json_match.group(1).strip()

    # If no triple backticks, try to find JSON-like structure
    json_match = re.search(r'(\[\s*\{.*\}\s*\])', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()

    # Return original text if no patterns matched
    return response_text


def generate_ai_data(prompt: str, row_count: int, realism: str = "realistic") -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Generate synthetic data using Google GenAI based on user prompt.

    Args:
        prompt: User prompt describing the desired data
        row_count: Number of rows to generate
        realism: Data realism mode: realistic, randomized, or biased

    Returns:
        Tuple of (generated data list, list of field names)
    """
    # Construct a detailed prompt for the AI model
    system_prompt = f"""
    You are a synthetic data generator. Based on the user's description, you will generate a dataset in JSON format.

    Guidelines:
    1. Create a dataset with the appropriate fields based on the user's description
    2. Generate {row_count} rows of data
    3. Make the data {realism} - {'with high realism and validity' if realism == 'realistic' else 'completely randomized' if realism == 'randomized' else 'with some biases to simulate edge cases'}
    4. Ensure all data values are appropriate for their field types
    5. Return ONLY a valid JSON array containing objects with the appropriate fields

    For example, if asked to generate e-commerce data, return JSON like:
    ```json
    [
      {{
        "customer_id": "C12345",
        "name": "John Smith",
        "email": "john.smith@example.com",
        "product": "Wireless Headphones",
        "price": 89.99,
        "purchase_date": "2023-04-15"
      }},
      ...more rows...
    ]
    ```

    IMPORTANT: Return ONLY the JSON array, with no additional text or explanations.
    """

    user_prompt = f"Generate synthetic data for: {prompt}\n\nPlease generate {row_count} rows of data with {realism} values."

    try:
        # Generate content using Google GenAI
        response = model.generate_content([system_prompt, user_prompt])
        response_text = response.text

        # Extract JSON from the response
        json_str = extract_json_from_response(response_text)

        # Parse the JSON data
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            # If direct JSON parsing fails, try to interpret as Python literal
            try:
                data = ast.literal_eval(json_str)
            except (SyntaxError, ValueError):
                raise ValueError(f"Failed to parse AI response as JSON: {json_str[:100]}...")

        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("AI did not return a valid list of data objects")

        # Extract fields from the first item
        fields = list(data[0].keys())

        # Return the data and field names
        return data, fields

    except Exception as e:
        raise Exception(f"Error generating data with GenAI: {str(e)}")
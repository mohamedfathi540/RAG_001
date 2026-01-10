
import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

try:
    from Stores.LLM.Templates.template_parser import template_parser
    
    parser = template_parser(language="en")
    print("Attempting to get 'system_prompt' from 'rag'...")
    # This should fail if it's a string and we try to .substitute() it blindly, 
    # or succeed if the fix is applied.
    # Note: 'system_prompt' in 'rag.py' is a simple string.
    result = parser.get("rag", "system_prompt", {})
    
    print(f"Result type: {type(result)}")
    print(f"Result content: {result[:50]}...")
    print("SUCCESS: Retrieved system_prompt without error.")

except AttributeError as e:
    print(f"CAUGHT EXPECTED ERROR: {e}")
except Exception as e:
    print(f"CAUGHT UNEXPECTED ERROR: {e}")

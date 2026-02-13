import sys
import os
sys.path.append(os.path.abspath("SRC"))
print("Starting import...", flush=True)
try:
    from Stores.LLM.Providers.Gemini_provider import GeminiProvider
    print("Import successful", flush=True)
except Exception as e:
    print(f"Import failed: {e}", flush=True)

import logging
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add SRC to path if exists (for host execution)
if os.path.exists("SRC"):
    sys.path.append(os.path.abspath("SRC"))

from Stores.LLM.Providers.Gemini_provider import GeminiProvider

class TestGeminiRetry(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    @patch('Stores.LLM.Providers.Gemini_provider.genai')
    @patch('Stores.LLM.Providers.Gemini_provider.time.sleep')
    def test_retry_delay_parsing(self, mock_sleep, mock_genai):
        # Setup mock client
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        
        # Instantiate provider
        provider = GeminiProvider(api_key="test_key")
        
        # Configure mock to raise exception with specific message
        error_message = (
            "429 RESOURCE_EXHAUSTED. {'error': {'code': 429, "
            "'message': 'You exceeded your current quota... Please retry in 2.5s.', "
            "'status': 'RESOURCE_EXHAUSTED'}}"
        )
        mock_client.models.generate_content.side_effect = Exception(error_message)
        
        # Call generate_text
        print("Calling generate_text...", flush=True)
        result = provider.genrate_text("test prompt")
        
        # Verify sleep was called with parsed time (capped at 60 + 1)
        # Expected: ~3.5s (min(2.5 + 1, 60))
        
        # Check calls to sleep
        print("\ntime.sleep calls:", flush=True)
        for call in mock_sleep.call_args_list:
            print(call, flush=True)
            
        # We expect at least one call with ~3.5s
        
        found_parsed_wait = False
        for call in mock_sleep.call_args_list:
            args, _ = call
            if 3.0 < args[0] < 4.0:
                found_parsed_wait = True
                break
        
        self.assertTrue(found_parsed_wait, "Did not find sleep call matching parsed retry delay (approx 3.5s)")
        print("\n✅ Verification passed: Correctly parsed retry delay from error message.")

if __name__ == '__main__':
    unittest.main()

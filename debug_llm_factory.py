
import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

try:
    from Stores.LLM.LLMProviderFactory import LLMProviderFactory
    from Helpers.Config import settings, get_settings
    from Stores.LLM.LLMEnums import LLMEnums

    print("Initializing settings...")
    # Mocking settings if .env is missing or incomplete for the test, 
    # but strictly speaking we want to test with strict validation if possible.
    # We'll try to use the actual settings class.
    
    # We need to make sure we can instantiate settings. 
    # Calling get_settings() relies on environment variables.
    # For this test, we might bypass the env file loading if it fails, OR just mock the config object.
    
    class MockConfig:
        OPENAI_API_KEY = "test_key"
        OPENAI_BASE_URL = "http://test.url"
        COHERE_API_KEY = "test_cohere_key"
        INPUT_DEFUALT_MAX_CHARACTERS = 1000
        GENRATED_DEFUALT_MAX_OUTPUT_TOKENS = 100
        GENRATION_DEFUALT_TEMPERATURE = 0.5
        
    config = MockConfig()
    print("Initializing LLMProviderFactory with MockConfig...")
    factory = LLMProviderFactory(config)
    
    print("Creating OpenAI Provider...")
    provider = factory.create(LLMEnums.OPENAI.value)
    
    if provider:
        print(f"SUCCESS: Created provider: {type(provider)}")
        print(f"Provider base_url: {provider.base_url}")
    else:
        print("FAILED: Provider is None")

except AttributeError as e:
    print(f"CAUGHT ERROR: {e}")
except Exception as e:
    print(f"CAUGHT UNEXPECTED ERROR: {e}")

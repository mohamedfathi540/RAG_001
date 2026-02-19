from .LLMEnums import LLMEnums
from .Providers import OpenAIProvider, CohereProvider, GeminiProvider, HuggingFaceProvider


class LLMProviderFactory :
    def __init__(self,config : dict):
        self.config = config

    def create (self , provider : str ) :
        if provider == LLMEnums.OPENAI.value :
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                base_url = self.config.OPENAI_BASE_URL,
                default_input_max_characters = self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genrated_max_output_tokens = self.config.GENRATED_DEFUALT_MAX_OUTPUT_TOKENS,
                default_genration_temperature = self.config.GENRATION_DEFUALT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value :
            return CohereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genrated_max_output_tokens = self.config.GENRATED_DEFUALT_MAX_OUTPUT_TOKENS,
                default_genration_temperature = self.config.GENRATION_DEFUALT_TEMPERATURE   
            )
                
               
        if provider == LLMEnums.GEMINI.value :
            return GeminiProvider(
                api_key = self.config.GEMINI_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genrated_max_output_tokens = self.config.GENRATED_DEFUALT_MAX_OUTPUT_TOKENS,
                default_genration_temperature = self.config.GENRATION_DEFUALT_TEMPERATURE   
            )

        if provider == LLMEnums.HUGGINGFACE.value :
            return HuggingFaceProvider(
                api_key = getattr(self.config, "HUGGINGFACE_API_KEY", None),
                default_input_max_characters = self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genrated_max_output_tokens = self.config.GENRATED_DEFUALT_MAX_OUTPUT_TOKENS,
                default_genration_temperature = self.config.GENRATION_DEFUALT_TEMPERATURE
            )

        return None

    def create_ocr(self, ocr_backend: str):
        """
        Create an OCR provider based on OCR_BACKEND setting.
        - LLAMAPARSE: returns None (controller uses LlamaParse directly)
        - GEMINI: returns a GeminiProvider with vision capabilities
        - OPENAI: returns an OpenAIProvider with vision capabilities
        - Others: returns the standard provider (may not support OCR)
        """
        ocr_backend = ocr_backend.upper()

        if ocr_backend in ["LLAMAPARSE", "EASYOCR"]:
            # These backends are handled directly in the controller
            return None

        # Create the provider via the standard factory
        provider = self.create(ocr_backend)

        if provider is None:
            return None

        # Set the generation model for vision tasks — use OCR_MODEL_ID from config
        ocr_model_id = getattr(self.config, "OCR_MODEL_ID", None)
        if ocr_model_id:
            provider.set_genration_model(ocr_model_id)
        elif ocr_backend == LLMEnums.GEMINI.value:
            provider.set_genration_model("gemini-2.0-flash")
        elif ocr_backend == LLMEnums.OPENAI.value:
            provider.set_genration_model("gpt-4o")

        return provider

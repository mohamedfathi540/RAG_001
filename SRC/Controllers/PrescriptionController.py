"""
PrescriptionController — OCR prescription images, extract medicine names,
and search for active ingredients + images.

Supports multiple OCR backends configured via OCR_BACKEND in .env:
  - LLAMAPARSE: Cloud-based OCR (requires LLAMA_CLOUD_API_KEY)
  - GEMINI: Google Gemini Vision AI (requires GEMINI_API_KEY)
  - OPENAI: OpenAI Vision (requires OPENAI_API_KEY)

The OCR provider is created by LLMProviderFactory.create_ocr() and
follows the same LLMInterface pattern as other providers.
"""
import os
import re
import json
import logging
import asyncio
from typing import List
from urllib.parse import quote_plus

import httpx

from .BaseController import basecontroller
from Helpers.Config import get_settings

logger = logging.getLogger("uvicorn.error")

# ── Shared vision prompt for all OCR providers ──────────────────────
OCR_VISION_PROMPT = (
    "You are an expert Egyptian pharmacist who reads handwritten "
    "prescriptions daily.\n\n"
    "TASK: Look at this prescription image and:\n"
    "1. Read ALL the text you can see\n"
    "2. Extract every medicine/drug name\n"
    "3. Provide the active ingredient for each\n\n"
    "IMPORTANT:\n"
    "- Prescriptions have NUMBERED items (1, 2, 3, 4...). "
    "Find a medicine for EVERY numbered item.\n"
    "- Even if handwriting is messy, give your BEST GUESS.\n"
    "- Medicine names are always in Latin/English letters.\n"
    "- Fix obvious misspellings to the correct medicine name.\n\n"
    "COMMON EGYPT MEDICINES:\n"
    "Moxclav/Augmentin/Megamox/Hibiotic → Amoxicillin + Clavulanic acid\n"
    "Phenadon → Paracetamol + Pseudoephedrine + Chlorpheniramine\n"
    "Phinex/Rhinex → Chlorpheniramine + Pseudoephedrine\n"
    "Cataflam/Voltaren → Diclofenac\n"
    "Antinal → Nifuroxazide\n"
    "Kongestal/Comtrex → Paracetamol + Chlorpheniramine + Pseudoephedrine\n"
    "Panadol → Paracetamol | Brufen → Ibuprofen\n"
    "Flagyl/Amrizole → Metronidazole\n"
    "Nexium → Esomeprazole | Omeprazole → Omeprazole\n"
    "Ciprocin → Ciprofloxacin | Xithrone → Azithromycin\n"
    "Glucophage → Metformin | Concor → Bisoprolol\n"
    "Ventolin → Salbutamol\n\n"
    "RESPOND WITH EXACTLY THIS JSON FORMAT:\n"
    "{\n"
    '  "ocr_text": "full text you read from the image",\n'
    '  "medicines": [\n'
    '    {"name": "MedicineName", "active_ingredient": "IngredientName"}\n'
    "  ]\n"
    "}\n\n"
    "Return ONLY the JSON. No explanation."
)


class PrescriptionController(basecontroller):

    def __init__(self):
        super().__init__()
        self.settings = get_settings()

    # =================================================================
    # MAIN ENTRY POINT
    # =================================================================
    async def analyze_prescription(
        self,
        file_path: str,
        genration_client,
        ocr_client=None,
    ) -> dict:
        """
        Full pipeline:
        1. OCR / vision-read the prescription image (based on OCR_BACKEND)
        2. Extract medicine names + active ingredients
        3. Build Google Image search URLs

        Args:
            file_path: Path to the prescription image
            genration_client: LLM provider for text generation (used by
                              LLAMAPARSE pipeline for medicine extraction)
            ocr_client: OCR provider created by LLMProviderFactory.create_ocr()
                        None if OCR_BACKEND is LLAMAPARSE
        """
        ocr_backend = getattr(
            self.settings, "OCR_BACKEND", "LLAMAPARSE"
        ).upper()
        logger.info("Using OCR backend: %s", ocr_backend)

        if ocr_backend == "LLAMAPARSE":
            # LlamaParse text OCR → LLM extraction
            return await self._pipeline_llamaparse(
                file_path, genration_client
            )
        else:
            # Vision-based OCR via the provider's ocr_image method
            if ocr_client is None:
                raise ValueError(
                    f"OCR_BACKEND is set to '{ocr_backend}' but no OCR "
                    f"client was initialized. Check your API key in .env."
                )
            return await self._pipeline_vision(file_path, ocr_client)

    # =================================================================
    # PIPELINE A: LlamaParse OCR → HuggingFace LLM extraction
    # =================================================================
    async def _pipeline_llamaparse(
        self, file_path: str, genration_client
    ) -> dict:
        """LlamaParse text OCR → LLM medicine extraction pipeline."""
        ocr_text = await self._ocr_llamaparse(file_path)
        if not ocr_text.strip():
            return {"ocr_text": "", "medicines": []}

        medicines_raw = await self._llm_extract_medicines(
            ocr_text, genration_client
        )
        if not medicines_raw:
            return {"ocr_text": ocr_text, "medicines": []}

        medicines = await self._enrich_medicines(medicines_raw)
        return {"ocr_text": ocr_text, "medicines": medicines}

    # =================================================================
    # PIPELINE B: Vision OCR (uses provider.ocr_image)
    # =================================================================
    async def _pipeline_vision(
        self, file_path: str, ocr_client
    ) -> dict:
        """
        Send image to the OCR provider's ocr_image method.
        Works with any provider that implements LLMInterface.ocr_image.
        """
        from fastapi.concurrency import run_in_threadpool

        # Call the provider's ocr_image (synchronous) in a thread pool
        raw_response = await run_in_threadpool(
            ocr_client.ocr_image,
            image_path=file_path,
            prompt=OCR_VISION_PROMPT,
            max_output_tokens=2048,
            temperature=0.2,
        )

        if not raw_response:
            logger.warning("OCR provider returned no response")
            return {"ocr_text": "", "medicines": []}

        # Parse the JSON response
        medicines_raw, ocr_text = self._parse_vision_response(raw_response)

        if not medicines_raw:
            return {"ocr_text": ocr_text, "medicines": []}

        medicines = await self._enrich_medicines(medicines_raw)
        return {"ocr_text": ocr_text, "medicines": medicines}

    @staticmethod
    def _parse_vision_response(text: str) -> tuple:
        """Parse the JSON response from a vision OCR provider."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        text = text.strip()

        try:
            data = json.loads(text)
            ocr_text = data.get("ocr_text", "")
            medicines = []

            for m in data.get("medicines", []):
                if isinstance(m, dict) and m.get("name"):
                    medicines.append({
                        "name": m["name"].strip(),
                        "active_ingredient": m.get(
                            "active_ingredient", "Unknown"
                        ).strip(),
                    })

            logger.info(
                "Vision OCR extracted %d medicines: %s",
                len(medicines),
                [(m["name"], m["active_ingredient"]) for m in medicines],
            )
            logger.info("Vision OCR text:\n%s", ocr_text)
            return medicines, ocr_text

        except json.JSONDecodeError as e:
            logger.error("Failed to parse vision OCR response: %s", e)
            logger.error("Raw text: %s", text[:500])
            return [], ""

    # =================================================================
    # LlamaParse OCR
    # =================================================================
    async def _ocr_llamaparse(self, file_path: str) -> str:
        """Use LlamaParse to OCR an image file and return extracted text."""
        from llama_parse import LlamaParse

        api_key = self.settings.LLAMA_CLOUD_API_KEY
        if not api_key or api_key == "llx-REPLACE_WITH_YOUR_KEY":
            raise ValueError(
                "LLAMA_CLOUD_API_KEY is not set in .env — "
                "get a free key from https://cloud.llamaindex.ai/"
            )

        parser = LlamaParse(
            api_key=api_key,
            result_type="text",
            premium_mode=True,
            skip_diagonal_text=False,
            do_not_unroll_columns=True,
            system_prompt=(
                "This is a handwritten medical prescription from a doctor. "
                "Your ONLY job is to extract ALL text from this image as "
                "accurately as possible, especially MEDICINE and DRUG NAMES.\n\n"
                "CRITICAL INSTRUCTIONS:\n"
                "1. Prescriptions have NUMBERED items (1, 2, 3, 4, etc). "
                "Find and extract the text for EVERY numbered item.\n"
                "2. Medicine names are in Latin/English letters even if the "
                "rest is Arabic.\n"
                "3. Common medicine names: Augmentin, Moxclav, Panadol, "
                "Cataflam, Voltaren, Brufen, Antinal, Flagyl, Nexium, "
                "Omeprazole, Phenadon, Phinex, Rhinex, Kongestal, Comtrex, "
                "Ciprocin, Xithrone, Glucophage, Amaryl, Concor, Ventolin, "
                "Symbicort, Prednisolone, Aspocid, Megamox, Hibiotic.\n"
                "4. Even if partially illegible, write your best guess. "
                "Do NOT skip anything.\n"
                "5. Include dosage and instructions — extract EVERYTHING."
            ),
        )

        documents = await parser.aload_data(file_path)
        if not documents:
            return ""

        full_text = "\n".join(doc.text for doc in documents)
        logger.info("LlamaParse OCR extracted %d characters", len(full_text))
        logger.info("OCR text:\n%s", full_text)
        return full_text

    # =================================================================
    # LLM-based medicine extraction (used by LlamaParse pipeline)
    # =================================================================
    async def _llm_extract_medicines(
        self, ocr_text: str, genration_client
    ) -> List[dict]:
        """Extract medicine names + active ingredients from OCR text."""
        from fastapi.concurrency import run_in_threadpool

        if not ocr_text or not ocr_text.strip():
            return []

        prompt = (
            "You are an expert Egyptian pharmacist who reads handwritten "
            "prescriptions daily. You know EVERY medicine sold in Egypt.\n\n"
            "TASK: Read this OCR text from a prescription and extract ALL "
            "medicines.\n\n"
            "CRITICAL RULES:\n"
            "1. Prescriptions have NUMBERED items (1, 2, 3, 4...). "
            "There should be at least one medicine per numbered item. "
            "If you see a number without a clear medicine, the OCR "
            "probably garbled the name — GUESS the most likely medicine.\n"
            "2. Partial/truncated text IS a medicine:\n"
            "   - 'Aumentn' or 'Augmnetin' → Augmentin\n"
            "   - 'Vo' or 'Vol' near 'meals' → Voltaren\n"
            "   - 'Ome' near 'breakfast' → Omeprazole\n"
            "   - 'Mox' or 'M0x' → Moxclav\n"
            "   - 'Phen' or 'Phena' → Phenadon\n"
            "   - 'Phin' or 'Rhin' → Phinex or Rhinex\n"
            "   - 'Cat' or 'Cata' → Cataflam\n"
            "   - 'Bru' or 'Bruf' → Brufen\n"
            "   - 'Pan' or 'Pana' → Panadol\n"
            "   - 'Ant' or 'Anti' → Antinal\n"
            "   - 'Flag' → Flagyl\n"
            "   - 'Cip' or 'Cipr' → Ciprocin\n"
            "3. ANY word in Latin/English letters that is NOT a doctor name, "
            "clinic name, address, or date is probably a medicine.\n\n"
            "COMMON EGYPT MEDICINES AND THEIR INGREDIENTS:\n"
            "Moxclav/Augmentin → Amoxicillin + Clavulanic acid\n"
            "Phenadon → Paracetamol + Pseudoephedrine + Chlorpheniramine\n"
            "Phinex/Rhinex → Chlorpheniramine + Pseudoephedrine\n"
            "Cataflam/Voltaren → Diclofenac\n"
            "Antinal → Nifuroxazide\n"
            "Kongestal → Paracetamol + Chlorpheniramine + Pseudoephedrine\n"
            "Panadol → Paracetamol | Brufen → Ibuprofen\n"
            "Flagyl/Amrizole → Metronidazole\n"
            "Nexium → Esomeprazole | Omeprazole → Omeprazole\n"
            "Ciprocin → Ciprofloxacin | Xithrone → Azithromycin\n"
            "Glucophage → Metformin | Concor → Bisoprolol\n"
            "Ventolin → Salbutamol\n\n"
            "RESPONSE FORMAT — Return ONLY a JSON array:\n"
            '[{"name": "MedicineName", "active_ingredient": "IngredientName"}]\n\n'
            "If unsure about ingredient, use \"Unknown\".\n"
            "Return ONLY the JSON array. No explanation.\n\n"
            f"--- Prescription Text ---\n{ocr_text}\n--- End ---"
        )

        try:
            response = await run_in_threadpool(
                genration_client.genrate_text,
                prompt=prompt,
                chat_history=[],
                max_output_tokens=2048,
                temperature=0.3,
            )

            if not response:
                logger.warning("LLM returned empty response")
                return []

            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)
            cleaned = cleaned.strip()

            array_match = re.search(r'\[.*\]', cleaned, re.DOTALL)
            if array_match:
                cleaned = array_match.group(0)

            medicines = json.loads(cleaned)
            if isinstance(medicines, list):
                result = []
                for m in medicines:
                    if isinstance(m, dict) and m.get("name"):
                        result.append({
                            "name": m["name"].strip(),
                            "active_ingredient": m.get(
                                "active_ingredient", "Unknown"
                            ).strip(),
                        })
                    elif isinstance(m, str) and m.strip():
                        result.append({
                            "name": m.strip(),
                            "active_ingredient": "Unknown",
                        })
                logger.info(
                    "Extracted medicines: %s",
                    [(m["name"], m["active_ingredient"]) for m in result],
                )
                return result
            return []

        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM JSON: %s", e)
            return []
        except Exception as e:
            logger.error("Medicine extraction error: %s", e)
            return []

    # =================================================================
    # Enrichment: OpenFDA + Google Image URLs
    # =================================================================
    async def _enrich_medicines(
        self, medicines_raw: List[dict]
    ) -> List[dict]:
        """Enhance ingredients via OpenFDA and build Google search URLs."""

        async def enrich(med: dict) -> dict:
            name = med["name"]
            active = med["active_ingredient"]

            openfda_result = await self._search_openfda(name)
            if openfda_result:
                active = openfda_result
                logger.info("OpenFDA enhanced '%s': %s", name, active)

            image_url = self._build_google_image_url(name)

            return {
                "name": name,
                "active_ingredient": active,
                "image_url": image_url,
            }

        tasks = [enrich(m) for m in medicines_raw]
        results = await asyncio.gather(*tasks)
        return list(results)

    @staticmethod
    def _build_google_image_url(medicine_name: str) -> str:
        """Build a Google Image Search URL for the medicine."""
        query = f"{medicine_name} medicine"
        return (
            f"https://www.google.com/search?q={quote_plus(query)}&tbm=isch"
        )

    async def _search_openfda(self, medicine_name: str) -> str:
        """Try OpenFDA to get official active ingredient name."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = (
                    f"https://api.fda.gov/drug/label.json"
                    f"?search=openfda.brand_name:"
                    f'"{quote_plus(medicine_name)}"'
                    f"&limit=1"
                )
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    if results:
                        openfda = results[0].get("openfda", {})
                        generic = openfda.get("generic_name", [])
                        if generic:
                            return generic[0]
                        substance = openfda.get("substance_name", [])
                        if substance:
                            return substance[0]
        except Exception:
            pass
        return ""

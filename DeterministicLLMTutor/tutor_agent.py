import json
import re
import time
import hashlib
from typing import Dict, Any, Optional

from Labs.DeterministicLLMTutor.config import get_gemini_model
from Labs.DeterministicLLMTutor.prompts import build_phrasing_prompt
from Labs.DeterministicLLMTutor.logger import log_interaction, init_db

# Initialize DB on load
init_db()

_RESPONSE_CACHE: Dict[str, str] = {}

class DeterministicDSTutor:
    def __init__(self, templates_path: str = "templates.json"):
        with open(templates_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)
        self.topics = self.kb.get("topics", [])
        
        try:
            self.model = get_gemini_model()
            self.api_available = True
        except Exception as e:
            self.model = None
            self.api_available = False
            self.api_error_msg = str(e)

    def detect_intent(self, query: str) -> Optional[Dict[str, Any]]:
        """Matches query keywords against templates.json to find the Topic."""
        q_clean = query.lower()
        for topic in self.topics:
            for kw in topic["keywords"]:
                if re.search(rf"\b{re.escape(kw)}\b", q_clean):
                    return topic
        for topic in self.topics:
            if topic["intent"].lower() in q_clean:
                return topic
        return None

    def detect_subintent(self, query: str) -> str:
        """
        OPTIMIZATION 2: INTENT CLASSIFICATION
        Detects the student's specific learning objective.
        """
        q = query.lower()
        if any(k in q for k in ["error", "fix", "not working", "bug", "debug"]):
            return "Debugging"
        if any(k in q for k in ["code", "implement", "python", "script", "syntax", "generate"]):
            return "Code Generation"
        if any(k in q for k in ["complexity", "time", "space", "big o", "efficiency"]):
            return "Complexity Analysis"
        if any(k in q for k in ["how does", "steps", "algorithm", "working", "how it works"]):
            return "Algorithm"
        if any(k in q for k in ["example", "sample", "show me", "illustration"]):
            return "Example"
        if any(k in q for k in ["vs", "compare", "difference between", "versus"]):
            return "Comparison"
        if any(k in q for k in ["what is", "define", "definition", "meaning"]):
            return "Definition"
            
        return "General Overview"

    def filter_template_fields(self, topic_template: Dict[str, Any], subintent: str) -> Dict[str, Any]:
        """Slices only the fields requested by the classified intent."""
        # Map detected intent to corresponding template keys
        intent_map = {
            "Definition": ["definition"],
            "Algorithm": ["algorithm"],
            "Complexity Analysis": ["complexity"],
            "Example": ["example"],
            "Code Generation": ["code"],
            "Debugging": ["code", "algorithm"], # Combines info to help debug
            "Comparison": ["definition", "summary"] 
        }
        
        keys_to_extract = intent_map.get(subintent, ["definition", "summary"])
        return {k: topic_template.get(k) for k in keys_to_extract if topic_template.get(k)}

    def answer_query(self, raw_query: str) -> Dict[str, Any]:
        """Main agent pipeline execution."""
        start_time = time.time()
        
        # Step 1: Detect Target Topic
        matched_topic = self.detect_intent(raw_query)
        
        # Step 2: Classify Intent Objective (Optimization 2)
        subintent = self.detect_subintent(raw_query)
        
        # Fallback handling
        if not matched_topic:
            fallback_text = "Sorry, I can answer only predefined Data Science questions."
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            
            log_interaction(raw_query, "Fallback", subintent, elapsed_ms, fallback_text)
            return {
                "response": fallback_text,
                "intent": "Fallback",
                "subintent": subintent,
                "cached": False,
                "latency_ms": elapsed_ms
            }

        # Step 3: Extract & Filter Knowledge
        primary_intent = matched_topic["intent"]
        template_data = self.filter_template_fields(matched_topic, subintent)

        # Step 4: Cache Lookup
        cache_key_raw = f"{primary_intent}:{subintent}:{json.dumps(template_data, sort_keys=True)}"
        cache_key = hashlib.sha256(cache_key_raw.encode("utf-8")).hexdigest()
        
        is_cached = False
        if cache_key in _RESPONSE_CACHE:
            final_response = _RESPONSE_CACHE[cache_key]
            is_cached = True
        else:
            # Step 5: Generate via Gemini with Optimized Prompt (Optimization 1)
            if not self.api_available:
                final_response = f"API Error: {self.api_error_msg}\n\nData:\n" + json.dumps(template_data, indent=2)
            else:
                try:
                    prompt = build_phrasing_prompt(subintent, template_data, primary_intent)
                    api_res = self.model.generate_content(prompt)
                    final_response = api_res.text.strip()
                    _RESPONSE_CACHE[cache_key] = final_response
                except Exception as e:
                    final_response = f"Gemini Call Error: {str(e)}"

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        # Step 6: Log to SQLite
        log_interaction(raw_query, primary_intent, subintent, elapsed_ms, final_response)

        return {
            "response": final_response,
            "intent": primary_intent,
            "subintent": subintent,
            "cached": is_cached,
            "latency_ms": elapsed_ms
        }
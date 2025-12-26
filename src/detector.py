import re
import spacy
from .logger import logger

class PII_Detector:
    def __init__(self, model_name="en_core_web_sm"):
        logger.info(f"Loading NLP model: {model_name}...")
        try:
            self.nlp = spacy.load(model_name)
            logger.info("NLP model loaded successfully.")
        except OSError:
            logger.warning(f"Model '{model_name}' not found. Downloading...")
            from spacy.cli import download
            download(model_name)
            self.nlp = spacy.load(model_name)
            logger.info("NLP model downloaded and loaded.")

        # Compile basic regex patterns for speed
        self.patterns = {
            "EMAIL": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "SSN": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "CREDIT_CARD": re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
            # Basic keyword storage (can be expanded)
            "CONFIDENTIAL": re.compile(r'\b(confidential|private|secret|restricted)\b', re.IGNORECASE)
        }

    def scan_text(self, text):
        """
        Scans text for PII and sensitive content.
        Returns a list of dictionaries with detected info.
        """
        matches = []
        
        if not text:
            return matches

        # 1. Regex Scanning
        for label, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                matches.append({
                    "type": label,
                    "value": match.group(),
                    "method": "Regex"
                })

        # 2. NLP Context Scanning (NER)
        # We process the text with Spacy to find Named Entities
        doc = self.nlp(text)
        
        # Interested in specific entities
        target_ents = ["PERSON", "ORG", "GPE", "MONEY"]
        
        for ent in doc.ents:
            if ent.label_ in target_ents:
                # We can add a filter here to reduce noise. 
                # For now, we report them but maybe we only want them if they appear near sensitive keywords?
                # Simple implementation: Report all ORG/PERSON as potential PI
                matches.append({
                    "type": ent.label_,
                    "value": ent.text,
                    "method": "NLP(NER)"
                })

        return matches

if __name__ == "__main__":
    # Quick test
    detector = PII_Detector()
    sample = "Please send the confidential files to john.doe@example.com."
    print(detector.scan_text(sample))

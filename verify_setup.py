import sys
import os

try:
    print("Testing imports...")
    import watchdog
    import pyperclip
    import spacy
    import torch
    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

from src.detector import PII_Detector

def test_detector():
    print("\nTesting PII Detector...")
    detector = PII_Detector()
    text = "My secret email is secret@agency.gov and my SSN is 999-00-1234."
    matches = detector.scan_text(text)
    print(f"Text: {text}")
    print(f"Matches: {matches}")
    
    expected_types = {"EMAIL", "SSN"}
    found_types = {m['type'] for m in matches}
    
    if expected_types.intersection(found_types):
        print("SUCCESS: Detected PII.")
    else:
        print("FAILURE: Did not detect PII.")
        sys.exit(1)

if __name__ == "__main__":
    test_detector()

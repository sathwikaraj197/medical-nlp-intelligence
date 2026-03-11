import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.safety.guardrails import SafetyChecker

def test_pii_redaction():
    checker = SafetyChecker()
    
    test_cases = [
        (
            "My email is test@example.com and phone is 123-456-7890.", 
            "My email is [EMAIL REDACTED] and phone is [PHONE REDACTED]."
        ),
        (
            "SSN: 111-22-3333, DOB: 12/12/1990",
            "SSN: [SSN REDACTED], DOB: [DATE REDACTED]"
        ),
        (
            "Date: 2023-01-01",
            "Date: [DATE REDACTED]"
        )
    ]
    
    all_passed = True
    for original, expected in test_cases:
        redacted = checker.audit_pii(original)
        if redacted != expected:
            print(f"FAILED: Input: {original}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {redacted}")
            all_passed = False
        else:
            print(f"PASSED: {original} -> {redacted}")
            
    return all_passed

if __name__ == "__main__":
    if test_pii_redaction():
        print("\nAll PII tests passed!")
    else:
        print("\nSome PII tests failed.")

import requests
import sys
import time

def test_api():
    url = "http://127.0.0.1:8000/analyze"
    payload = {"text": "Patient reports severe headache and potential heart attack."}
    
    for i in range(5):
        try:
            print(f"Attempt {i+1} to connect...")
            response = requests.post(url, json=payload, timeout=5)
            print(f"Status: {response.status_code}")
            resp_json = response.json()
            print(f"Response: {resp_json}")
            
            if response.status_code == 200:
                # validation
                entities = resp_json.get("entities", [])
                found_headache = any(e['text'] == 'headache' and e['label'] == 'MEDICAL_CONDITION' for e in entities)
                found_heart_attack = any(e['text'] == 'heart attack' and e['label'] == 'MEDICAL_CONDITION' for e in entities)
                
                if found_headache and found_heart_attack:
                    print("SUCCESS: Detected 'headache' and 'heart attack' as MEDICAL_CONDITION")
                    return True
                else:
                    print("FAILURE: Did not detect expected entities properly.")
                    return False
        except requests.exceptions.ConnectionError:
            print("Connection refused. Retrying in 2 seconds...")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            return False
            
    return False

if __name__ == "__main__":
    if test_api():
        print("API Verified Successfully")
        sys.exit(0)
    else:
        print("API Verification Failed")
        sys.exit(1)

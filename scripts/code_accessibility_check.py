import os
import json
from datetime import datetime
import requests
# Optional: Use dotenv to keep tokens secure
# from dotenv import load_dotenv
# load_dotenv()
# :closed_lock_with_key: API Keys
GROQ_API_KEY = "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"  # Replace with your key
GITHUB_REPO_URL = "https://github.com/swatagga/Flight_booking_system.git"  # Adjust for your use case
# :file_folder: Step 1: Define GitHub Files to Analyze
files_to_check = [
    "index.html",
    "login.html",
    "style.css",
    "dashboard.html"
]
# :mag_right: Step 2: Define Prompt Template
def generate_prompt(file_name, file_content):
    return f"""
You are an accessibility expert. Review the following file `{file_name}` for common accessibility issues (like missing ARIA roles, contrast issues, unlabeled buttons, etc.). Suggest improvements using WCAG 2.1 and HTML best practices.
Only suggest improvements that matter. Be concise and output a JSON like:
{{
  "Issue": "Short description of issue",
  "Element": "Relevant snippet or tag",
  "AI-Suggested Fix": "How to fix it"
}}
--- FILE CONTENT START ---
{file_content}
--- FILE CONTENT END ---
"""
# :robot_face: Step 3: Call Groq LLM for Each File
def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
# :package: Collect AI Suggestions
accessibility_issues = {}
for file_name in files_to_check:
    print(f":mag: Checking: {file_name}")
    try:
        file_url = GITHUB_REPO_URL + file_name
        file_content = requests.get(file_url).text
        prompt = generate_prompt(file_name, file_content)
        result = call_groq(prompt)
        accessibility_issues[file_name] = json.loads(result)
    except Exception as e:
        print(f":x: Error processing {file_name}: {e}")
        accessibility_issues[file_name] = {"Error": str(e)}
# :memo: Step 4: Save Results to Timestamped JSON File
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"github_accessibility_fixes_{timestamp}.json"
with open(output_filename, "w") as f:
    json.dump(accessibility_issues, f, indent=4)
# :white_check_mark: Step 5: Print Fixes
print("\n:small_blue_diamond: AI-Powered Accessibility Fixes:\n")
for file, fix in accessibility_issues.items():
    print(f":page_facing_up: File: {file}")
    if "Error" in fix:
        print(f":x: Error: {fix['Error']}\n")
        continue
    print(f":rotating_light: Issue: {fix['Issue']}")
    print(f":small_blue_diamond: Affected Code: {fix['Element']}")
    print(f":white_check_mark: Suggested Fix: {fix['AI-Suggested Fix']}\n")
print(f"\n:file_folder: Output saved to: {output_filename}")
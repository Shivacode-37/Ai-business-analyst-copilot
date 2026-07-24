import requests

API_URL = "https://enterprise-ai-business-copilot-1.onrender.com/api/v1/analyze"


def analyze_csv(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv",
        )
    }

    response = requests.post(API_URL, files=files)

    if response.ok:
        return response.json()

    try:
        detail = response.json().get("detail", "Unknown error")
    except Exception:
        detail = response.text

    raise Exception(detail)

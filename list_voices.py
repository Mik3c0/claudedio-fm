import requests, sys

api_key = input("ElevenLabs API key: ").strip()
r = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": api_key})
voices = r.json()["voices"]

print(f"\n{'#':<4} {'Name':<28} {'ID':<28} {'Category'}")
print("-" * 80)
for i, v in enumerate(voices):
    cat = v.get("category", "")
    labels = v.get("labels", {})
    accent = labels.get("accent", "")
    gender = labels.get("gender", "")
    print(f"{i:<4} {v['name']:<28} {v['voice_id']:<28} {cat}  {accent} {gender}")

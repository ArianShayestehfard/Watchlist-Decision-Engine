import requests

response = requests.get(
    "https://api.themoviedb.org",
    timeout=10
)

print(response.status_code)
print(response.text[:500])
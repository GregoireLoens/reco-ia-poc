import requests

print("Hello depuis Docker !")
r = requests.get("https://api.github.com")
print("Statut GitHub:", r.status_code)

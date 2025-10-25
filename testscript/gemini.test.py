from google import genai

# Client mit API-Key erstellen (besser über Umgebungsvariable)
client = genai.Client(api_key="AIzaSyDZt3P8I-_pdLH7L4aQvx8qmrTwgvMVeYk")

# Generiere Inhalt mit dem Modell "gemini-2.5-flash"
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Wie groß wird eine ahorn baum"
)

# Gib den generierten Text aus
print(response.text)
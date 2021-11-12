import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "XXXXXXXXXXXXXX"
NEWS_API_KEY = "XXXXXXXXXXX"
TWILIO_SID = "XXXXXXXXXXX"
TWILIO_AUTH_TOKEN = "XXXXXXXXX"

# API-Zugang zu Alpha Vantage
stock_params = {
  "function": "TIME_SERIES_DAILY",
  "symbol": STOCK_NAME,
  "apikey": STOCK_API_KEY,
}

# Gestrige Daten
response = requests.get(STOCK_ENDPOINT)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Daten von vorgestern
dby_data = data_list[1]
dby_closing_price = dby_data["4. close"]


# Berechnen der Differenz zwischen gestern und vorgestern
# Umwandeln der strings in floats und in absolute Zahl
difference = abs(float(yesterday_closing_price) - float(dby_closing_price))

# Berechnung der Differenz in Prozent
diff_percent = (difference / float(yesterday_closing_price)) * 100

# Sollte der Aktienwert um 25% fallen, werden Nachrichtenartikel über newsapi.org abgefragt
if diff_percent > 25:
    news_params = {
      "apiKey": NEWS_API_KEY,
      "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# Abfragen der ersten drei Artikel mit Slice Notation
    three_top_articles = articles[:3]
    print(three_top_articles)


# Erstellen einer Liste der Schlagzeilen und Inhaltsbeschreibung mit list comprehension
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_top_articles]


# Twilio-client aus Twilio-client-Klasse
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="Twilio-Nummer",
            to="Eigene-Nummer",
        )

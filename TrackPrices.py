import sqlite3
import yfinance as yf 
import time
from twilio.rest import Client
from alpha_vantage.timeseries import TimeSeries


texted_stocks = []

api_key = #Get your Own Alpha Advantage API key


ACCOUNT_SID = #Get own Twilio Trial SID Key
AUTH_TOKEN = #Get own Twilio Trial Token Key
TWILIO_PHONE_NUMBER = #Get own Twilio Phone Number 
TARGET_PHONE_NUMBER = #Phone Number you want to text too


def getCurrentPrice(ticker):
    ts = TimeSeries(key=api_key)
    data, meta_data = ts.get_quote_endpoint(symbol=ticker) 
    current_price = float(data['05. price'])
    return current_price

def send_text_message(body):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=TARGET_PHONE_NUMBER
    )
    print(f"Text message sent: {message.sid}")

def query_stocks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    rows = cursor.fetchall()
    return rows

def textSent(alert_stock):

    for stock in texted_stocks:
        if alert_stock == stock:
            return True
        
    return False
    

def monitor_stock_prices(conn):

    stocks = query_stocks(conn)

    for stock in stocks: 


        symbol = stock[1]
        lowPrice = stock[4]
        highPrice = stock[5] 

        

        currentPrice = getCurrentPrice(symbol)

        alreadyTexted = textSent(stock)

        if(currentPrice < lowPrice and alreadyTexted == False):
            body = f"{symbol} has reached a price lower than ${lowPrice:.2f}. Current price: ${currentPrice:.2f}"
            texted_stocks.append(stock)
            #send_text_message(body)

        elif(currentPrice > highPrice and alreadyTexted == False):
            body = f"{symbol} has reached the target price of ${highPrice[symbol]:.2f}. Current price: ${currentPrice:.2f}"
            #send_text_message(body)
            texted_stocks.append(stock)



conn = sqlite3.connect('stocks.db')


while(True):
        
    monitor_stock_prices(conn)
    time.sleep(300)


       

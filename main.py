import sqlite3
import yfinance as yf

def is_valid_ticker(ticker):
    stock_info = yf.Ticker(ticker).info
    return 'regularMarketPrice' in stock_info


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                     (date TEXT, symbol TEXT, quantity INTEGER, price REAL, alertLow REAL, alertHigh Real)''')
    conn.commit()

def insert_stock(conn, date, symbol, quantity, price, alertLow, alertHigh):
    cursor = conn.cursor()

    try: 

        cursor.execute("INSERT INTO stocks (date, symbol, quantity, price, alertLow, alertHigh) VALUES (?, ?, ?, ?, ?, ?)",
                    (date, symbol, quantity, price, alertLow, alertHigh))
        conn.commit()

    except:
        print("Could not add new stock to database, make sure all input entered is of correct format")


def delete_stock(conn, date, symbol):
    cursor = conn.cursor()
    try:
        
        cursor.execute("DELETE FROM stocks WHERE date = ? AND symbol = ?", (date, symbol))
        conn.commit()
        print(date + " and " +symbol+ " successfully removed")
    
    except:
        print("Symbol and date do not match in the table")
        return False



def query_stocks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    rows = cursor.fetchall()
    return rows

def stockAdd(conn):

    while(True):
        try:
            
            date = input("Enter Input in 'yyyy-mm-dd' format") 
            symbol = input("Enter ticker symbol")
            shares = float(input("Enter the amount of shares you purchased"))
            purchasePrice = float(input("Enter purchase Price"))
            lowPrice = float(input("Enter low Price"))
            highPrice = float(input("Enter high Price"))


            valid = is_valid_ticker(symbol)

            if(valid == True):
               insert_stock(conn, date, symbol, shares, purchasePrice, lowPrice, highPrice) 
               print("Stock Purchase data successfully added to the table!")
               break


        except:
            print("Make sure you enter type float for shares, and prices")


def stockDelete(conn):
            
        date = input("Enter Input in 'yyyy-mm-dd' format") 
        symbol = input("Enter ticker symbol")

        delete_stock(conn, date, symbol)

        



    

def main():
    # Connect to the SQLite database file (or create it if it doesn't exist)
    conn = sqlite3.connect('stocks.db')


    while(True):
        try: 
            print("What would you like to do? Please enter the number associated with the printed info")
            print("1. InsertStock\n2. RemoveStock")
        
            choice = int(input())

            if(choice == 1):
                stockAdd(conn)
                break

            elif(choice == 2):
                stockDelete(conn)
                break

            else: 
                print("Please enter 1 or 2")
                continue

        except:
            print("Make sure you enter 1 or 2 of type int")



    # Query data from the table
    stocks = query_stocks(conn)

    # Print the queried data
    print("Stocks in the database:")
    for stock in stocks:
        print(stock)

    # Close the connection to the database
    conn.close()

if __name__ == "__main__":
    main()

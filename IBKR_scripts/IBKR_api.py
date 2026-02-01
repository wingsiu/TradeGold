from ib_insync import IB
from ib_insync import IB, Stock

# Connect to the API Gateway (adjust port as needed)
ib = IB()

try:
    ib.connect('127.0.0.1', 4002, clientId=1)  # Use port 4001 for live accounts, 4002 for paper accounts
    print("Connected to IBKR API Gateway")
except Exception as e:
    print(f"API connection failed: {e}")
    exit()

# Fetch Account Summary
account_summary = ib.accountSummary()
print("Account Summary:")
print(account_summary)

# Fetch Real-Time Market Data
contract = Stock('AAPL', 'SMART', 'USD')  # Example: Apple stock
ib.qualifyContracts(contract)
ticker = ib.reqMktData(contract)
ib.sleep(2)  # Wait for market data to be fetched
print(f"AAPL Market Data: Bid: {ticker.bid}, Ask: {ticker.ask}")

# Disconnect
ib.disconnect()
print("Disconnected from IBKR API Gateway")
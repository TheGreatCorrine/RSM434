from ritapi import get_bid_ask, get_news, get_open_orders, get_order_status, get_position, get_tick, get_time_sales
import requests
from time import sleep

s = requests.Session()
s.headers.update({'X-API-key': 'GW4GJ6BI'}) # API Key from YOUR RIT Client

def main():
    
    MAX_EXPOSURE = 25000

    order_type = 'LIMIT'
    
    PREMIUM = 0.02
    
    tick, status = get_tick()

    
    while status == 'ACTIVE':   
        position = get_position() # this thing always returns absolute value
        
        # time_and_sales = get_time_sales('AC')
        
        # news = get_news()
        tickers = ['CNR', 'RY', 'AC']
        
        if position < MAX_EXPOSURE:
            for i in range(len(tickers)):
                best_bid_price, best_ask_price = get_bid_ask(tickers[i])
                bid_ask_spread = best_ask_price - best_bid_price
            
                if bid_ask_spread >= 0.1:
                    resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': order_type, 'quantity': 100, 'price': best_bid_price, 'action': 'BUY'})
                    resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': order_type, 'quantity': 100, 'price': best_ask_price, 'action': 'SELL'})
                     
        
        # resp.json()
        # order_id = resp.json()['order_id']
        
        # resp = s.delete('http://localhost:9999/v1/orders/' + str(order_id))
        sleep(0.5)
        
        resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'all': 1})
        
        # resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': 'AC'})
    
        # resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'query': 'Volume > 0'})
        for i in range(len(tickers)):
            ticker_position = get_position_ticker(i)
            if ticker_position < 0:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': 'MARKET', 'quantity': ticker_position, 'price': best_bid_price, 'action': 'BUY'})
            if ticker_position > 0:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': 'MARKET', 'quantity': ticker_position, 'price': best_ask_price, 'action': 'SELL'})
        
        
        tick, status = get_tick()   
    

if __name__ == '__main__':
    main()

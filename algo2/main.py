from ritapi import get_bid_ask, get_news, get_open_orders, get_order_status, get_position, get_tick, get_time_sales
import requests
from time import sleep

s = requests.Session()
s.headers.update({'X-API-key': 'GW4GJ6BI'}) # API Key from YOUR RIT Client

def main():
    tick, status = get_tick()
    
    while status == 'ACTIVE':
        best_bid_price, best_ask_price = get_bid_ask('AC')
        
        # position = get_position()
        
        # time_and_sales = get_time_sales('AC')
        
        # news = get_news()
        
        best_bid_price_AC, best_ask_price_AC = get_bid_ask('AC')
        bid_ask_spread_AC = best_ask_price_AC - best_bid_price_AC
        if bid_ask_spread_AC >= 0.1:
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': 'LIMIT', 'quantity': 500, 'price': best_bid_price_AC, 'action': 'BUY'})
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'AC', 'type': 'LIMIT', 'quantity': 500, 'price': best_ask_price_AC, 'action': 'SELL'})
        
        best_bid_price_RY, best_ask_price_RY = get_bid_ask('RY')   
        bid_ask_spread_RY = best_ask_price_RY - best_bid_price_RY         
        if bid_ask_spread_RY >= 0.1:
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'RY', 'type': 'LIMIT', 'quantity': 500, 'price': best_bid_price_RY, 'action': 'BUY'})
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'RY', 'type': 'LIMIT', 'quantity': 500, 'price': best_ask_price_RY, 'action': 'SELL'})

        best_bid_price_CNR, best_ask_price_CNR = get_bid_ask('CNR')     
        bid_ask_spread_CNR = best_ask_price_CNR - best_bid_price_CNR
        if bid_ask_spread_CNR >= 0.1:
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'RY', 'type': 'LIMIT', 'quantity': 500, 'price': best_bid_price_CNR, 'action': 'BUY'})
            resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'RY', 'type': 'LIMIT', 'quantity': 500, 'price': best_ask_price_CNR, 'action': 'SELL'})
        
        resp.json()
        order_id = resp.json()['order_id']
        
        # resp = s.delete('http://localhost:9999/v1/orders/' + str(order_id))
        
        resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'all': 1})
        
        # resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': 'AC'})
    
        # resp = s.post('http://localhost:9999/v1/commands/cancel', params = {'query': 'Volume > 0'})
        
        
        tick, status = get_tick()   
        # x = 0
    

if __name__ == '__main__':
    main()
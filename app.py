from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import asyncio
from binance import AsyncClient, BinanceSocketManager

app = Flask(__name__)
socketio = SocketIO(app)  # Using default threading mode

# Global variable to store the current symbol
current_symbol = 'BNBBTC'

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)
    # Emit order book data to the frontend
    socketio.emit('order_book', order_book)

async def kline_listener(client, symbol):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=symbol) as stream:
        while True:
            res = await stream.recv()
            print(res)
            socketio.emit('kline_data', res)

async def start_listener():
    global current_symbol
    client = await AsyncClient.create()
    await kline_listener(client, current_symbol)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api_query', methods=['GET'])
def api_query():
    api_url = request.args.get('url')
    response = requests.get(api_url)
    return jsonify(response.json())

@app.route('/change_symbol', methods=['POST'])
def change_symbol():
    global current_symbol
    new_symbol = request.json.get('symbol')
    if new_symbol:
        current_symbol = new_symbol
        emit('symbol_changed', {'symbol': current_symbol}, broadcast=True)
    return jsonify({'symbol': current_symbol})

@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Connected to WebSocket'})
    # Start the async Binance WebSocket listener
    asyncio.run(start_listener())

@socketio.on('custom_event')
def handle_custom_event(data):
    print('received custom event: ' + str(data))
    emit('response', {'data': 'Received data: ' + str(data)})

@socketio.on('change_symbol')
def handle_change_symbol(data):
    global current_symbol
    new_symbol = data.get('symbol')
    if new_symbol:
        current_symbol = new_symbol
        # Restart the listener with the new symbol
        asyncio.run(start_listener())
        emit('symbol_changed', {'symbol': current_symbol}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import asyncio
from binance import AsyncClient, BinanceSocketManager

app = Flask(__name__)
socketio = SocketIO(app)  # Using default threading mode

# Global variable to store the current symbol
current_symbol = 'BNBBTC'

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)
    # Emit order book data to the frontend
    socketio.emit('order_book', order_book)

async def kline_listener(client, symbol):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=symbol) as stream:
        while True:
            res = await stream.recv()
            print(res)
            socketio.emit('kline_data', res)

async def start_listener():
    global current_symbol
    client = await AsyncClient.create()
    await kline_listener(client, current_symbol)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api_query', methods=['GET'])
def api_query():
    api_url = request.args.get('url')
    response = requests.get(api_url)
    return jsonify(response.json())

@app.route('/change_symbol', methods=['POST'])
def change_symbol():
    global current_symbol
    new_symbol = request.json.get('symbol')
    if new_symbol:
        current_symbol = new_symbol
        emit('symbol_changed', {'symbol': current_symbol}, broadcast=True)
    return jsonify({'symbol': current_symbol})

@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Connected to WebSocket'})
    # Start the async Binance WebSocket listener
    asyncio.run(start_listener())

@socketio.on('custom_event')
def handle_custom_event(data):
    print('received custom event: ' + str(data))
    emit('response', {'data': 'Received data: ' + str(data)})

@socketio.on('change_symbol')
def handle_change_symbol(data):
    global current_symbol
    new_symbol = data.get('symbol')
    if new_symbol:
        current_symbol = new_symbol
        # Restart the listener with the new symbol
        asyncio.run(start_listener())
        emit('symbol_changed', {'symbol': current_symbol}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

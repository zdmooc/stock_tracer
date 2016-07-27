import json
from flask import Flask, render_template, request, redirect, url_for
from stock_tracer.common import MQClient

app = Flask(__name__)

@app.route("/")
def home():
    request_body = {}
    request_body['action'] = 'list_quotes'
    request_body['payload'] = {'days': 20}
    client = MQClient()
    reply = client.call(request_body)

    if 'error' in reply:
        return "error!{}".format(str(reply))

    stock_quotes = json.loads(reply)
    date_header = []
    for stock_quote in stock_quotes.itervalues():
        for quote in stock_quote['quotes']:
            if quote['date'] not in date_header:
                date_header.append(quote['date'])

    date_header.sort()

    stock_rows = []
    for key, stock_quote in stock_quotes.iteritems():
        stock_row_item = {'id': key}
        stock_row_item['exchange'] = stock_quote['exchange']
        stock_row_item['symbol'] = stock_quote['symbol']
        stock_row_item['change_percentages'] = [0] * len(date_header)
        for quote in stock_quote['quotes']:
            index = date_header.index(quote['date'])
            stock_row_item['change_percentages'][index] = quote['change_percentage']

        stock_rows.append(stock_row_item)

    return render_template('home.html', date_header=date_header, stock_rows=stock_rows)

@app.route('/add', methods=['POST'])
def add_stock():
    app.logger.info(request.form['exchange'])
    app.logger.info(request.form['symbol'])
    client = MQClient()
    request_body = {}
    request_body['action'] = 'add_stock'
    request_body['payload'] = {}
    request_body['payload']['exchange'] = request.form['exchange']
    request_body['payload']['symbol'] = request.form['symbol']
    app.logger.info(request_body)
    responce = client.call(request_body)

    return responce

@app.route('/stock/<stock_id>')
def stock_detail(stock_id):
    app.logger.info("building view for {}".format(stock_id))

    request_body = {}
    request_body['action'] = 'list_quotes'
    request_body['payload'] = {'days': 100}
    request_body['payload']['stock_id'] = stock_id

    client = MQClient()
    reply = client.call(request_body)

    if 'error' in reply:
        return "error!{}".format(str(reply))

    stock_detail = json.loads(reply)

    return render_template('stock_detail.html', stock=stock_detail[stock_id])

@app.route('/refresh_quotes', methods=['post'])
def refresh_quotes():
    client = MQClient()
    reply = client.call({'action': 'refresh_quotes'})
    if 'error' in reply:
        return reply

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()

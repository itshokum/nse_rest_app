from bs4 import BeautifulSoup as bs
import urllib,json
from flask import Flask, jsonify
import csv

app = Flask(__name__)


def create_stock_list_dict():
	with open('EQUITY_L.csv','r',encoding='utf-8') as infile:
		reader = csv.reader(infile)
		stock_list_dict = {rows[0] : rows[1] for rows in reader}
	return stock_list_dict

stock_list_dict = create_stock_list_dict()

@app.route('/stock/<string:stock_symbol>')
def get_stock_details(stock_symbol):	
	#stock_symbol = 'INFY'
	print(stock_symbol.upper())
	if stock_symbol.upper() not in stock_list_dict:
		message = "Stock with symbol {} not found".format(stock_symbol)
		return jsonify({'message' : message})

	nse_quote_url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + urllib.parse.quote(stock_symbol)

	headers={'User-Agent': 'Mozilla/5.0'}

	req = urllib.request.Request(nse_quote_url,headers=headers)

	data = urllib.request.urlopen(req).read()
	#data = urllib.request.urlopen('http://google.in').read()

	soup = bs(data,'html.parser')
	jsonData = soup.find('div',{'id':'responseDiv'})
	data_list = json.loads(jsonData.text)['data']
	if not data_list:
		message = "Stock with symbol {} not found".format(stock_symbol)
		return jsonify({'message' : message})		
	return jsonify(data_list[0])
	#print(json.loads(jsonData.text)['data'][0]['averagePrice'])
	#return jsonify({"message":"Stock with symbol {} not found".format(stock_symbol)})

if __name__ == "__main__":
	app.run(port=5000) 


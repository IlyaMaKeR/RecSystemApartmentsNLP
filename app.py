import pymysql
from recommendation import search_apartments_by_tags
from flask import Flask, render_template, request
from model import process_query
import asyncio


connector = pymysql.connect(
    host="",
    user="Admin",
    password="",
    database="apartments",
    port=
)

app = Flask(__name__)

cursor = connector.cursor()

@app.route('/')
async def main():
    return render_template('index.html')

@app.route('/search')
async def search():
    return render_template('search_form.html')

@app.route('/process')
async def process_request():
    # Получение значения тегов из строки запроса
    text = request.args.get('text', '')
    tags = process_query(text)



    # Использование нового метода для поиска квартир
    search_results = search_apartments_by_tags(tags)

    return render_template('results.html', results=search_results)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

import locale
import math

from .create_statement_data import *

locale.setlocale(locale.LC_ALL, '')


class Play:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Performance:
    def __init__(self, play_id, audience):
        self.play_id = play_id
        self.audience = audience

class Invoice:
    def __init__(self, customer, performances):
        self.customer = customer
        self.performances = performances

    
def usd(number):
    return number // 100

def render_plain_text(data:dict) -> str:
    result = f"invoice (customer : {data['customer']})\n"
    for perf in data['performances']:
        result += f"{perf['play'].name} {usd(perf['amount'])} ({perf['audience']} seats)\n"
    
    result += f"total: {usd(data['total_amount'])}\n"
    result += f"volume credits: {data['total_volume_credits']} points"
    return result

def render_html(data:dict) -> str:
    result = f"<h1> invoice (customer : {data['customer']})\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>price</th></tr>"
    for perf in data['performances']:
        result += f"<tr><td>{perf['play'].name}</td><td>{perf['audience']} seats</td>"
        result += f"<td>{usd(perf['amount'])}</td></tr>\n"
    result += "</table>\n"
    result += f"<p>total: <em>{usd(data['total_amount'])}</em></p>\n"
    result += f"<p>volume credits: <em>{data['total_volume_credits']}</em></p>\n"
    return result


def statement(invoice:Invoice, plays:dict) -> str:
    return render_plain_text(create_statement_data(invoice, plays))

def html_statement(invoice:Invoice, plays:dict) -> str:
    return render_html(create_statement_data(invoice, plays))
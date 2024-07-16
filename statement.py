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
    

def render_plain_text(data:dict) -> str:
    def usd(number):
        return number // 100
    
    result = f"invoice (customer : {data['customer']})\n"
    for perf in data['performances']:
        result += f"{perf['play'].name} {usd(perf['amount'])} ({perf['audience']} seats)\n"
    
    result += f"total: {usd(data['total_amount'])}\n"
    result += f"volume credits: {data['total_volume_credits']} points"
    return result


def statement(invoice:Invoice, plays:dict) -> str:
    return render_plain_text(create_statement_data(invoice, plays))
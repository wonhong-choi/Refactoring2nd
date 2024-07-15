import locale
import math
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
    

def statement(invoice:Invoice, plays:dict) -> str:
    def amount_for(perf, play):
        this_amount = 0
        match play.type:
            case "tragedy":     # tragedy
                this_amount = 40000
                if perf.audience > 30:
                    this_amount += 1000 * (perf.audience - 30)
            case "comedy":      # comedy
                this_amount = 30000
                if perf.audience > 20:
                    this_amount += 10000 + 500 * (perf.audience - 20)
                this_amount += 300 * perf.audience
            case _:
                raise Exception(f"Not supported genre: {play.type}")
        return this_amount
    
    total_amount = 0
    volume_credits = 0
    result = f"invoice (customer : {invoice.customer})\n"
    
    for perf in invoice.performances:
        play = plays[perf.play_id]
        this_amount = amount_for(perf, play)
        
        volume_credits += max(perf.audience - 30, 0)
        if play.type == "comedy":
            volume_credits += math.floor(perf.audience / 5)
            
        result += f"{play.name} {this_amount // 100} ({perf.audience} seats)\n"
        total_amount += this_amount
    
    result += f"total: {total_amount // 100}\n"
    result += f"volume credits: {volume_credits} points"
    return result
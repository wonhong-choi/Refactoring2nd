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
    def play_for(performance):
        return plays[performance.play_id]
    
    def amount_for(performance):
        result = 0
        match play_for(performance).type:
            case "tragedy":     # tragedy
                result = 40000
                if performance.audience > 30:
                    result += 1000 * (performance.audience - 30)
            case "comedy":      # comedy
                result = 30000
                if performance.audience > 20:
                    result += 10000 + 500 * (performance.audience - 20)
                result += 300 * performance.audience
            case _:
                raise Exception(f"Not supported genre: {play_for(performance).type}")
        return result
    
    def volume_credits_for(performance):
        volume_credits = max(perf.audience - 30, 0)
        if play_for(perf).type == "comedy":
            volume_credits += math.floor(perf.audience / 5)
        return volume_credits
    
    total_amount = 0
    volume_credits = 0
    result = f"invoice (customer : {invoice.customer})\n"
    
    for perf in invoice.performances:
        volume_credits += volume_credits_for(perf)
            
        result += f"{play_for(perf).name} {amount_for(perf) // 100} ({perf.audience} seats)\n"
        total_amount += amount_for(perf)
    
    result += f"total: {total_amount // 100}\n"
    result += f"volume credits: {volume_credits} points"
    return result
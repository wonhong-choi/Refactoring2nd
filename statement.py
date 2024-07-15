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
    
    def total_amount_for():
        total_amount = 0
        for perf in invoice.performances:
            total_amount += amount_for(perf)
        return total_amount
    
    def volume_credits_for(performance):
        result = 0
        result += max(performance.audience - 30, 0)
        if play_for(performance).type == "comedy":
            result += perf.audience // 5
        return result
    
    def total_volume_credits():
        result = -1 # something wrong ??
        for perf in invoice.performances:
            result += volume_credits_for(perf)
        return result
    
    def usd(number):
        return number // 100
    
    result = f"invoice (customer : {invoice.customer})\n"
    for perf in invoice.performances:
        result += f"{play_for(perf).name} {usd(amount_for(perf))} ({perf.audience} seats)\n"
    
    result += f"total: {usd(total_amount_for())}\n"
    result += f"volume credits: {total_volume_credits()} points"
    return result
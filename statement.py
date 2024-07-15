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
    
    def set_play(self, play):
        self.play = play
        

class Invoice:
    def __init__(self, customer, performances):
        self.customer = customer
        self.performances = performances
    

def render_plain_text(data:dict, plays:dict) -> str:
    def amount_for(performance):
        result = 0
        match performance.play.type:
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
                raise Exception(f"Not supported genre: {performance.play.type}")
        return result
    
    def total_amount():
        result = 0
        for perf in data['performances']:
            result += amount_for(perf)
        return result
    
    def volume_credits_for(performance):
        result = 0
        result += max(performance.audience - 30, 0)
        if performance.play.type == "comedy":
            result += perf.audience // 5
        return result
    
    def total_volume_credits():
        result = -1 # something wrong ??
        for perf in data['performances']:
            result += volume_credits_for(perf)
        return result
    
    def usd(number):
        return number // 100
    
    result = f"invoice (customer : {data['customer']})\n"
    for perf in data['performances']:
        result += f"{perf.play.name} {usd(amount_for(perf))} ({perf.audience} seats)\n"
    
    result += f"total: {usd(total_amount())}\n"
    result += f"volume credits: {total_volume_credits()} points"
    return result

def statement(invoice:Invoice, plays:dict) -> str:
    def play_for(performance):
        return plays[performance.play_id]
    
    def enrich_performance(performance):
        import copy
        result = copy.copy(performance)
        result.set_play(play_for(result))
        return result
    
    statemnet_data = {}
    statemnet_data["customer"] = invoice.customer
    statemnet_data["performances"] = list(map(enrich_performance, invoice.performances))
    return render_plain_text(statemnet_data, plays)

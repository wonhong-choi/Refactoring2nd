from functools import reduce

def create_statement_data(invoice, plays):
    def play_for(performance):
        return plays[performance.play_id]
    
    def total_amount(data):
        return reduce(lambda total, each : total + each['amount'], data['performances'], 0)
    
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
                raise Exception(f"Not supported genre: {performance.play.type}")
        return result

    def total_volume_credits(data):
        return reduce(lambda total, each : total + each['volume_credits'], data['performances'], 0)
    
    def volume_credits_for(performance):
        result = 0
        result += max(performance.audience - 30, 0)
        if play_for(performance).type == "comedy":
            result += performance.audience // 5
        return result
    
    def enrich_performance(performance):
        result = {}
        result["play_id"] = performance.play_id
        result["audience"] = performance.audience
        result["play"] = play_for(performance)
        result["amount"] = amount_for(performance)
        result["volume_credits"] = volume_credits_for(performance) 
        return result
    
    statement_data = {}
    statement_data["customer"] = invoice.customer
    statement_data["performances"] = list(map(enrich_performance, invoice.performances))
    statement_data["total_amount"] = total_amount(statement_data)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    return statement_data
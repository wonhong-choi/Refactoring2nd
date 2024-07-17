from functools import reduce

class PerformanceCalculator:
    def __init__(self, performance, play) -> None:
        self.performance = performance
        self.play = play
        
    def amount(self):
        result = 0
        match self.play.type:
            case "tragedy":     # tragedy
                result = 40000
                if self.performance.audience > 30:
                    result += 1000 * (self.performance.audience - 30)
            case "comedy":      # comedy
                result = 30000
                if self.performance.audience > 20:
                    result += 10000 + 500 * (self.performance.audience - 20)
                result += 300 * self.performance.audience
            case _:
                raise Exception(f"Not supported genre: {self.play.type}")
        return result
    
    def volume_credits(self):
        result = 0
        result += max(self.performance.audience - 30, 0)
        if self.play.type == "comedy":
            result += self.performance.audience // 5
        return result
    

def create_statement_data(invoice, plays):
    def play_for(performance):
        return plays[performance.play_id]
    
    def total_amount(data):
        return reduce(lambda total, each : total + each['amount'], data['performances'], 0)
    
    def total_volume_credits(data):
        return reduce(lambda total, each : total + each['volume_credits'], data['performances'], 0)
    
    def enrich_performance(performance):
        performanceCalculator = PerformanceCalculator(performance, play_for(performance))
        result = {}
        result["play_id"] = performance.play_id
        result["audience"] = performance.audience
        result["play"] = performanceCalculator.play
        result["amount"] = performanceCalculator.amount()
        result["volume_credits"] = performanceCalculator.volume_credits() 
        return result
    
    statement_data = {}
    statement_data["customer"] = invoice.customer
    statement_data["performances"] = list(map(enrich_performance, invoice.performances))
    statement_data["total_amount"] = total_amount(statement_data)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    return statement_data
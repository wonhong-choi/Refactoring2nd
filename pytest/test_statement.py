from ..statement import *

def test_statement():
    plays = {
        "hamlet": Play("Hamlet", "tragedy"),
        "as-like": Play("As You Like It", "comedy"),
        "othello": Play("Othello", "tragedy")
    }
    
    invoices = [
        Invoice("BigCo", [Performance("hamlet", 55), Performance("as-like", 35), Performance("othello", 40)])
    ]
    
    expected = f"invoice (customer : BigCo)\n"
    expected += f"Hamlet {65000 // 100} ({55} seats)\n"
    expected += f"As You Like It {58000 // 100} ({35} seats)\n"
    expected += f"Othello {50000 // 100} ({40} seats)\n"
    expected += f"total: {173000 // 100}\n"
    expected += f"volume credits: {47} points"
    
    assert expected == statement(invoice=invoices[0], plays=plays)
        

    
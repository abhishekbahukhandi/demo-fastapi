def add(x: int,y: int):
    return x + y

def subtract(x: int, y: int):
    return x - y

def multiply(x: int, y: int):
    return x * y

def divide(x: int, y: int):
    if y == 0:
        raise ZeroDivisionError("Denominator can't be Zero")
    return x / y

class BankAccount:
    def __init__(self, balance: int = 0):
        self.balance = balance
    
    def get_balance(self):
        return f"Account Balance = {self.balance}"
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient Balance!!")
        self.balance -= amount
        
    
    def deposit(self, amount):
        self.balance += amount
    
    def add_interest(self, rate):
        accumulated_interest = int(self.balance*rate/100)
        self.balance += accumulated_interest

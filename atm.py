from typing import List
import collections
import random
class Account:
    def __init__(self, account_id:int, balance:int):
        self.account_id = account_id
        self.balance = balance
class Card:
    def __init__(self, card_id:int, pin:int, accounts= None):
        self.card_id = card_id
        self.pin = pin
        self.accounts= collections.defaultdict(list)
        if accounts:
            for acc in accounts:
                self.accounts[acc.account_id] = acc

class ATM_Controller:
    def __init__(self, base=None):
        self.base = collections.defaultdict(Card)
        if base:
            self.base= base
    
    def add_card(self, card_id:int, pin:int, accounts= None):
        if card_id in self.base:
            print("card added")
            return False
        self.base[card_id] = Card(card_id, pin, accounts)
    
    def add_account(self, card_id:int, account_id:int, balance:int):
        self.base[card_id].accounts[account_id] = Account(account_id, balance)
    
    def insert_card(self, card_id:int):
        if card_id in self.base:
            card = self.base[card_id]
            return card
            
        else:
            print("Card is not registered")
            return False
    def check_pin(self, card:Card, pin:int):
        return card.pin==pin
    
    def select_account(self, account_id, card:Card):
        if account_id in card.accounts:
            return card.accounts[account_id]
        else:
            print("Account Not Found")
            return False
    def account_activity(self, activity:int, account:Account, change:int = 0):
        if activity==1:
            return account.balance
        if activity==2:
            account.balance+=change
            return account.balance
        if activity==3:
            account.balance-=change
            return account.balance
        
        print("WRONG ACTIVITY CODE")
        return False
        
    def operate(self, card_id:int, pin:int, account_id:int, op: List[str]):
        card= self.insert_card(card_id)
        if card==False:
            return False
        
        if self.check_pin(card, pin)==False:
            print("WRONG PIN --- Terminate")
            return False
        
        account = self.select_account(account_id, card)

        if account==False:
            return False
        
        
        if op[0]=="See Balance":
            a = self.account_activity(1, account)
        elif op[0]=="Deposit":
            print("Balance is",self.account_activity(1, account), "Deposit", op[1])
            a = self.account_activity(2, account, int(op[1]))
        elif op[0]=="Withdraw":
            print("Balance is",self.account_activity(1, account),"Withdrawing", op[1])
            a = self.account_activity(3, account, int(op[1]))
        else:
            print("ILLEGAL OPERATION", op)
            return False
        print("Current Balance in ",account_id, " is ", a)
        return a

##Testing Functionality
print("______FUNCTIONAL TESTING____________")
ATM =  ATM_Controller()
def add_user_info(card_id, pin, account_id, balance):        
    ATM.add_card(card_id, pin)
    for i in range(len(account_id)):
        ATM.add_account(card_id,account_id[i],balance[i])
users= [12,23,24]
balance = [1200, 2300, 2400]
add_user_info(1,12,users, balance)
operation = ["See Balance", "Deposit", "Withdraw", "Illegal"]
money= ["1100", "1200", "800", "12"]
for i in range(len(users)):
    r = random.randint(0, 3)
    ATM.operate(1,12, users[i], [operation[r], money[r]])




##Logical Test
#Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw
print("______Logical TESTING____________")
add_user_info(3,1234, [1,2,3], [1000,2000,3000])
assert ATM.operate(3, 1234, 3, ["See Balance"])==3000
assert ATM.operate(3,1234, 1, ["See Balance"])==1000
assert ATM.operate(3, 1234, 2, ["See Balance"])==2000
assert ATM.operate(3,1234, 1, ["Deposit", 1000])==2000
assert ATM.operate(3,1234, 2, ["Deposit", 1000])==3000
assert ATM.operate(3,1234, 3, ["Deposit", 1000])==4000
assert ATM.operate(3,1234, 1, ["Withdraw", 2000])==0
assert ATM.operate(3,1234, 2, ["Withdraw", 3000])==0
assert ATM.operate(3,1234, 3, ["Withdraw", 4000])==0
assert ATM.operate(4,1234, 1, ["Withdraw", 2000])==False
assert ATM.operate(3,1231, 2, ["Withdraw", 3000])==0
assert ATM.operate(3,1234, 4, ["Withdraw", 4000])==0

cur=0
for i in range(100):
    assert ATM.operate(3, 1234, 1, ["See Balance"])==cur
    r = random.randint(0, 100000)
    cur+=r
    assert ATM.operate(3,1234, 1, ["Deposit", r])==cur
    z= random.randint(0, 100000)
    cur-=z
    assert ATM.operate(3,1234, 1, ["Withdraw", z])==cur
    

class Transaction:
    def cashin(self, amount, phone_number):
        return {"status": "success", "amount": amount, "phone": phone_number}
    
    def cashout(self, amount, phone_number):
        return {"status": "success", "amount": amount, "phone": phone_number}
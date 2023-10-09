class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        # Create a header with category name centered
        s = self.category.center(30, "*") + "\n"

        # Iterate through ledger items and format them
        for item in self.ledger:
            temp = f"{item['description'][:23]:23}{item['amount']:7.2f}"
            s += temp + "\n"

        # Add the total balance
        s += "Total: " + str(self.get_balance())
        return s

    def deposit(self, amount, description=""):
        # Create a dictionary to represent the transaction
        temp = {
            'amount': amount,
            'description': description
        }
        self.ledger.append(temp)

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            # Create a dictionary for the withdrawal transaction
            temp = {
                'amount': -amount,  # Negative amount indicates a withdrawal
                'description': description
            }
            self.ledger.append(temp)
            return True
        return False

    def get_balance(self):
        # Calculate the balance by summing all amounts in the ledger
        balance = sum(item['amount'] for item in self.ledger)
        return balance

    def transfer(self, amount, budget_cat):
        if self.check_funds(amount):
            # Withdraw from self and deposit into another category
            self.withdraw(amount, "Transfer to " + budget_cat.category)
            budget_cat.deposit(amount, "Transfer from " + self.category)
            return True
        return False

    def check_funds(self, amount):
        # Check if there are sufficient funds for a given amount
        return amount <= self.get_balance()


def create_spend_chart(categories):
    spend = []

    # Calculate the total spending for each category
    for category in categories:
        temp = sum(abs(item['amount']) for item in category.ledger if item['amount'] < 0)
        spend.append(temp)

    total = sum(spend)
    percentage = [i / total * 100 for i in spend]

    s = "Percentage spent by category"

    # Build the spending chart
    for i in range(100, -1, -10):
        s += "\n" + str(i).rjust(3) + "|"
        for j in percentage:
            if j > i:
                s += " o "
            else:
                s += "   "
        s += " "

    s += "\n    ----------"

    cat_length = [len(category.category) for category in categories]
    max_length = max(cat_length)

    # Build the category names at the bottom
    for i in range(max_length):
        s += "\n    "
        for j in range(len(categories)):
            if i < cat_length[j]:
                s += " " + categories[j].category[i] + " "
            else:
                s += "   "
        s += " "

    return s

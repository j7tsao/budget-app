class Category:

    def __init__(self, categoryName):
        self.name = categoryName
        self.ledger = list()
        self.total = 0
    
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = str()
        for item in self.ledger:
            items += f"{item['description'][:23]:23}" + f"{item['amount']:>7,.2f}" + '\n'
        display = title + items + "Total: " + str(self.total)
        return display

    def deposit(self, amount, description = ''):
        item = { "amount": amount, "description": description }
        self.ledger.append(item)
        self.total += amount
    
    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            item = { "amount": -amount, "description": description }
            self.ledger.append(item)
            self.total -= amount
            return True
        else:
            return False
    
    def get_balance(self):
        return self.total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw( amount, f"Transfer to {category.name}" )
            category.deposit( amount, f"Transfer from {self.name}" )
            return True
        return False
    
    def check_funds(self, amount):
        return False if amount > self.get_balance() else True

    def get_expenses(self):
        expenses = 0
        for item in self.ledger:
            if item['amount'] < 0:
                expenses += item['amount']
        return expenses


def create_spend_chart(categories):     # categories = a list of categories
    display = 'Percentage spent by category\n'

    expenses_all_cates = 0
    categoryExpenses = list()
    for category in categories:
        expenses_all_cates += category.get_expenses()
        categoryExpenses.append(category.get_expenses())

    categoriesNames = list()
    for category in categories:
        categoriesNames.append(category.name)
    
    catesPercent = list(map(lambda x: int(x / expenses_all_cates * 10) / 10, categoryExpenses))
    
    r = 100
    while r >= 0:
        dots = ' '
        for expense in catesPercent:
            if expense * 100 >= r:
                dots += "o  "
            else:
                dots += "   "
        display += str(r).rjust(3) + "|" + dots + '\n'
        r -= 10

    lines = " " * 4 + "---" * len(categoriesNames) + '-\n'
    maxlen = max(list(map(lambda x: len(x), categoriesNames)))

    names = str()
    for i in range(maxlen):
        oneLine = ' ' * 5
        for name in categoriesNames:
            if i >= len(name):
                oneLine += " " * 3
            else:
                oneLine += name[i] + " " * 2
        if i != maxlen - 1:
            oneLine += '\n'
        names += oneLine
    
    display += lines + names
    
    return display 

# instantiation & test
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))
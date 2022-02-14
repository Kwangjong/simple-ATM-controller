class controllerAPI: # pseudo-api for user interaction
	def insertCard(self): # simulate inserting card. Get arbituary card number as parameter.
		cardNum = raw_input("Enter card number: ") # get cardNumber as string

		if not cardNum.isdigit(): # return to main if non-numeric data is entered
			print "Please enter valid card number.\n"
			self.displayMain()

		self.enterPin(cardNum)

	def enterPin(self, cardNum): # enter pin for card already inserted.
		pin = raw_input("Enter PIN: ")

		if not pin.isdigit(): # return to main if non-numeric data is entered
			print "Please enter valid pin number.\n"
			self.displayMain()
		
		if not atm.readCard(cardNum, pin):
			self.invalidInfo()
		self.selectAccount()

	def invalidInfo(self): # called when given card number and pin is not valid
		print "Given information is invalid.\n"
		self.displayMain()

	def selectAccount(self):
		print "\nSelect account:\n1. Savings Account\n2. Checking Account\n3. Exit"
		try:
			action = int(raw_input())

			if action == 1 or action == 2: # account selected
				self.accountAction(action)

			elif action == 3:
				print ""
				atm.resetAccount() # exit
				self.displayMain()
			else:
				raise ValueError("Out Of Bound")

		except ValueError:
			print "Please select valid action."
			self.selectAccount()

	def accountAction(self, accountNum): # after account is selected ask for action to perform
		print "\nSelect Action:\n1. See Balance\n2. Deposit\n3. Withdraw\n4. Exit"
		try:
			action = int(raw_input())

			if action == 1:
				self.seeBalance(accountNum)
			elif action == 2:
				self.deposit(accountNum)
			elif action ==3:
				self.withdraw(accountNum)
			elif action == 4:
				print ""
				self.selectAccount() # return to select account
			else:
				raise ValueError("Out Of Bound")

		except ValueError:
			print "Please select valid action."
			self.accountAction(accountNum)

		self.accountAction(accountNum)

	def seeBalance(self, accountNum): # show balance of selected account
		balance = atm.getBalance(accountNum-1)
		if not balance:
			self.resetAccount()
			self.displayMain() # return to main if atm.getBalance() fails
		print "\nYour Account Balance: $"+str(balance)

	def deposit(self, accountNum): # deposit cash to selected account
		print "\nInsert Cash"
		try:
			amount = int(raw_input("amount: $"))
			if amount < 1:
				raise ValueError("You cannot deposit 0 or negative amount")
		except ValueError:
			print "Please select valid amount."
			self.deposit(accountNum)

		if not atm.deposit(amount, accountNum-1):
			atm.resetAccount()
			self.displayMain() # return to main if deposit fails
		print "Success!"
		self.seeBalance(accountNum)

	def withdraw(self, accountNum): # withdraw cash from selected account
		print "\nWithdraw Cash"
		try:
			amount = int(raw_input("amount: $"))
			if amount < 1:
				raise ValueError("You cannot withdraw 0 or negative amount")
		except ValueError:
			print "Please select valid amount."
			self.withdraw(accountNum)

		if not atm.withdraw(amount, accountNum-1): # if user trys to withdraw larger amounts than current balance return to accountAction
			print "Insufficient fund."
			self.accountAction(accountNum)

		print "Success!"
		self.seeBalance(accountNum)

	def setAtm(self, atm):
		self.atm = atm

	def displayMain(self):
		print "Welcome!\n1. Insert Card\n2. Exit"
		
		try:
			action = int(raw_input())

			if action == 1:
				self.insertCard()
			elif action == 2:
				exit()
			else:
				raise ValueError("Out Of Bound")
		except ValueError:
			print("Please select an action you wish to perfom.\n")
			self.displayMain()


class ATM:
	def __init__(self, bank, controller):
		self.__bank = bank
		self.__controller = controller
		self.__account = None

	def readCard(self, cardNum, pin): # called when a card was inserted and the pin is enterto the machine.
		self.__account = self.__bank.getAccount(cardNum, pin)

		if not self.__account: # return false when given information is invalid
			self.__account = None
			return False
		return True

	def getBalance(self, accountNum):  # 0 for savings 1 for checking
		if self.__account is None or accountNum not in [0,1]:
			return False # return false if no account is opened or accountNum out of bound

		return self.__account.balances[accountNum]


	def deposit(self, amount, accountNum):
		if self.__account is None or accountNum not in [0,1] or amount < 1:
			return False # return false if no account is opened or accountNum out of bound

		self.__account.balances[accountNum] += amount
		self.__bank.updateAccount(self.__account)
		return True

	def withdraw(self, amount, accountNum):
		if self.__account is None or accountNum not in [0,1] or amount < 1:
			return False # return false if no account is opened or accountNum out of bound

		if self.__account.balances[accountNum] - amount < 0: 
			return False # return false if amount is larger than balance

		self.__account.balances[accountNum] -= amount
		self.__bank.updateAccount(self.__account)
		return True

	def resetAccount(self): # flush opened account before exiting to main
		self.__account = None



class BankAPI: # pseudo-api for back-end banking system.

	def __init__(self, account_list):
		self.account_list = account_list

	def addAccount(self, account): # add account to the banking system for testing
		self.account_list.append(account)

	def getAccount(self, cardNum, pin): # get account with given card number if the pin is correct.
		for a in self.account_list:
			if a.cardNum == cardNum and a.pin == pin:
				return a

		return False # return false if card number or pin does not match

	def updateAccount(self, account): # update stored account with same card num to given account
		for i in range(len(self.account_list)):
			if self.account_list[i].cardNum == account.cardNum:
				self.account_list[i] = account



# class for bank accounts. Each account will have one debit card, one saving acount, and one checking account.
class Account: 
	def __init__(self, name, cardNum, pin, savings_balance, checking_balance):
		self.name = name # name of the account holder as String
		self.cardNum = cardNum	# cardNumber as string.   ex) "0001" != '1'
		self.pin = pin # pin as string
		self.balances = [savings_balance, checking_balance] # list of balances in two acccounts (0 for savings, 1 for checking)


def TestMain():
	print "Creating Testing data..."

	acc = [Account("kj", "12345678", "0000", 543, 50), Account("bear", "00000000", "1234", 300, 30), Account("Robot", "62831234", "7788", 100, 0)]
	bank = BankAPI(acc)
	ctrl = controllerAPI()
	atm = ATM(bank, ctrl)

	print "---------------------------------Test Data---------------------------------"
	print "name   card_number  pin   savings_account_balance  checking_account_balance"
	print "kj     12345678     0000  $543                     $50"
	print "bear   00000000     1234  $300                     $30"
	print "Robot  62831234     7788  $100                     $ 0"
	print "---------------------------------------------------------------------------\n"

	Test_readCard(atm)
	Test_getBalance(atm)
	Test_deposit(atm)
	Test_withdraw(atm)

	print "Ending Test...\n"

	return atm, ctrl, bank

def Test_readCard(atm): # test cases for readCard()
	print "Testing readCard()..."
	result = {True: "Passed!", False: "Failed."}

	print " test #1 check valid card number and pin :", result[atm.readCard("12345678", "0000")]
	atm.resetAccount()

	print " test #2 check valid card number and invalid pin :", result[not atm.readCard("12345678", "1234")]

	print " test #3 check invalid card number :", result[not atm.readCard("111111111", "0000")]
	print ""

def Test_getBalance(atm): # test cases for getBalance()
	print "Testing getBalance()..."
	result = {True: "Passed!", False: "Failed."}

	print " test #1 call getBalance() without calling readCard() in beforehand :", result[not atm.getBalance(0)]

	atm.readCard("12345678", "0000")
	print " test #2 call getBalance() with invalid accountNum :", result[not atm.getBalance(3)]

	print " test #3 call getBalance() with valid account :", result[543 == atm.getBalance(0)]
	atm.resetAccount()
	print ""

def Test_deposit(atm): # test cases for deposit()
	print "Testing deposit()..."
	result = {True: "Passed!", False: "Failed."}

	print " test #1 call deposit() without calling readCard() in beforehand :", result[not atm.deposit(100, 0)]

	atm.readCard("00000000", "1234")
	print " test #2 call deposit() with invalid accountNum :", result[not atm.deposit(100, 3)]

	print " test #3 deposit negative amount :", result[not atm.deposit(-100, 0)]

	out = atm.deposit(100, 0)
	print " test #4 call deposit() with valid parameters :", result[out and atm.getBalance(0) == 400]
	atm.resetAccount()
	print ""

def Test_withdraw(atm): # test cases for withdraw()
	print "Testing withdraw()..."
	result = {True: "Passed!", False: "Failed."}

	print " test #1 call withdraw() without calling readCard() in beforehand :", result[not atm.withdraw(100, 0)]

	atm.readCard("62831234", "7788")
	print " test #2 call withdraw() with invalid accountNum :", result[not atm.withdraw(100, 3)]

	print " test #3 withdraw negative amount :", result[not atm.withdraw(-100, 0)]

	print " test #4 withdraw more than current balance  :", result[not atm.withdraw(200, 0)]

	out = atm.withdraw(50, 0)
	print " test #5 call withdraw() with valid parameters :", result[out and atm.getBalance(0) == 50]
	atm.resetAccount()
	print ""


atm, ctrl, bank = TestMain()
ctrl.displayMain()





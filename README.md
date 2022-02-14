# simple-ATM-controller
simple atm controller in Python 2

## Classes
- **controllerAPI** : Pseudo-api for user interation.
- **ATM** : ATM controller
- **BankAPI** : Pseudo-api for banking system. 
- **Account** : Data structure for storing user's banking informations

## Account
Data structure for storing user's bank informations. Each account will have one debit card, one savings account, and one checking account
+ **name** : name of the account holder
+ **cardNum** : card number of the debit card linked to the account
+ **pin** : pin for the debit card
+ **balances** : list of integers for each account's balances. 0: savings account, 1: checking account

## ATM
ATM controller
+ **readCard(self, cardNum, pin)** : check for corresponding bank account with given card number and pin. when corresponding account is found it stores the account in its local scope. return false if given information is invalid, otherwise return true. readCard() should be called before performing any account actions.

+ **getBalance(self, accountNum)** : return balance for account that has been opended by readCard(). get accountNum as parameter for selecting savings or checking account. return false if no account is opened. true, otherwise.

+ **deposit(self, amount, accountNum)** : add balances by given amount. get accountNum as parameter for selecting savings or checking account. return false if no account is opened. true, otherwise.

+ **withdraw(self, amount, accountNum)** : subtract balance by given amount. get accountNum as parameter for selecting savings or checking accont. return false if no account is opend or amount being withdrawn is greater than account balance. true, otherwise.

+ resetAccount(self) : reset account stored in ATM's local scope. must be called when exiting.

## HOW-TO
- clone the repository or download atm.py file.
- run atm.py in Python 2, and test cases will automatically run.

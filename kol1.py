#!/usr/bin/python

class CustomerAccount:
	def __init__(self,name,balance):
		self.name=name
		self.balance=balance
	def withdraw(self,amount):
		self.balance+=amount
	def deposit(self,amount):
		self.balance+=amount
	def getBalance(self):
		return self.balance
class Bank:
	def __init__(self):
		self.customers= {}
	def addCustomer(self,name,balance):
		self.customers[name]=CustomerAccount(name,balance)
	def withdraw(self,customerName,ammount):
		self.customers[customerName].withdraw(ammount)
	def deposit(self,customerName,ammount):
		self.customers[customerName].deposit(ammount)
	def transfer(self,fromName,toName,ammount):
		self.withdraw(fromName,ammount)
		self.deposit(toName,ammount)
	def getBalance(self,customerName):
		return self.customers[customerName].getBalance()

newBank=Bank()
newBank.addCustomer("janek",1000)
newBank.addCustomer("marek",0)
print "Janek's balance:"+ str(newBank.getBalance("janek"))
print "Marek's balance:"+ str(newBank.getBalance("marek"))
newBank.withdraw("janek",200)
newBank.deposit("marek",50)
print "Janek's balance:"+ str(newBank.getBalance("janek"))
print "Marek's balance:"+ str(newBank.getBalance("marek"))
newBank.transfer("janek","marek",200)
print "Janek's balance:"+ str(newBank.getBalance("janek"))
print "Marek's balance:"+ str(newBank.getBalance("marek"))

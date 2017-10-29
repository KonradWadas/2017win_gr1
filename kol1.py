#!/usr/bin/python
import json


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (Customer, Bank)):
            return o.__dict__
        else:
            return json.JSONEncoder.encode(self, o)


class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance


class Bank:
    def __init__(self, prefix):
        self.customers = {}
        self.acc_num_prefix = str(prefix)
        self.next_number = 0

    def add_customer(self, name, balance):
        acc_number = self.acc_num_prefix + "-" + str(self.next_number)
        self.customers[acc_number] = Customer(name, balance)
        self.next_number += 1
        return acc_number

    def withdraw(self, number, amount):
        self.customers[number].withdraw(amount)

    def deposit(self, number, amount):
        self.customers[number].deposit(amount)

    def get_balance(self, number):
        return self.customers[number].get_balance()

    def dump(self):
        with open('result.json', 'a') as fp:
            for key in self.customers:
                json.dump(self.customers[key].__dict__, fp)


class BankingSystem:
    def __init__(self):
        self.banks = {}
        self.bank_names = {}
        self.acc_num_prefix = 0

    def add_bank(self, name):
        self.banks[str(self.acc_num_prefix)] = Bank(self.acc_num_prefix)
        self.bank_names[name] = str(self.acc_num_prefix)
        self.acc_num_prefix += 1

    def add_customer(self, bank_name, customer_name, balance):
        return self.banks[self.bank_names[bank_name]].add_customer(customer_name, balance)

    def withdraw(self, number, amount):
        self.banks[number.split('-')[0]].withdraw(number, amount)

    def deposit(self, number, amount):
        self.banks[number.split('-')[0]].deposit(number, amount)

    def transfer(self, from_acc, to_acc, amount):
        self.banks[from_acc.split('-')[0]].withdraw(from_acc, amount)
        self.banks[to_acc.split('-')[0]].deposit(to_acc, amount)

    def get_balance(self, number):
        return self.banks[number.split('-')[0]].get_balance(number)

    def dump(self, filename):
        with open(filename, 'a') as fp:
            json.dump(self.banks, fp, cls=CustomJsonEncoder)
            json.dump(self.bank_names, fp, cls=CustomJsonEncoder)


def show_help():
    print "Available commands:"
    print "add_bank: Add new bank"
    print "add_customer:  Add new customer"
    print "deposit: Deposit some amount"
    print "withdraw: Withdraw some amount"
    print "transfer: Transfer money"
    print "get_balance: Show balance"
    print "dump: Dump current program state as json"
    print "exit: Exit"


def add_customer():
    acc_number = banking_system.add_customer(raw_input('Enter bank name: '),
                                             raw_input('Enter customer name: '),
                                             raw_input('Enter balance: '))
    print "Your account number is" + acc_number


def add_bank():
    banking_system.add_bank(raw_input('Enter bank name: '))


def deposit():
    banking_system.deposit(raw_input('Enter account number: '), int(raw_input('Enter amount: ')))


def withdraw():
    banking_system.withdraw(raw_input('Enter account number: '), int(raw_input('Enter amount: ')))


def get_balance():
    print(banking_system.get_balance(raw_input('Enter account number: ')))


def transfer():
    banking_system.transfer(raw_input('Enter account number from: '),
                            raw_input('Enter account number to: '),
                            int(raw_input('Enter amount: ')))


def dump():
    banking_system.dump(raw_input('Enter dump file name: '))


def exit_program():
    exit(0)


if __name__ == "__main__":
    commands = {'help': show_help,
                'add_bank': add_bank,
                'add_customer': add_customer,
                'deposit': deposit,
                'withdraw': withdraw,
                'get_balance': get_balance,
                'transfer': transfer,
                'dump':dump,
                'exit': exit_program}
    banking_system = BankingSystem()
    banking_system.add_bank("superbank")
    banking_system.add_bank("turbobank")
    Andrzej_number = banking_system.add_customer("superbank", 'Andrzej', 1000)
    Mietek_number = banking_system.add_customer("turbobank", 'Mietek', 100)
    print "Andrzej's number:" + Andrzej_number
    print "Andrzej's number:" + Mietek_number
    print "Andrzej's balance:" + str(banking_system.get_balance(Andrzej_number))
    print "Mietek's balance:" + str(banking_system.get_balance(Mietek_number))
    banking_system.withdraw(Andrzej_number, 500)
    banking_system.deposit(Mietek_number, 100)
    print "Andrzej's balance:" + str(banking_system.get_balance(Andrzej_number))
    print "Mietek's balance:" + str(banking_system.get_balance(Mietek_number))
    banking_system.transfer(Andrzej_number, Mietek_number, 200)
    print "Andrzej's balance:" + str(banking_system.get_balance(Andrzej_number))
    print "Mietek's balance:" + str(banking_system.get_balance(Mietek_number))
    banking_system.dump("program_dump.json")
    while True:
        command = raw_input('Enter next command: ')
        if command in commands:
            commands[command]()
        else:
            print "Unsupported command, use help to list supported commands"

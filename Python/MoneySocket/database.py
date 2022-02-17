import pandas as pd
import copy

def DepositCash(user, amount):
    df = pd.read_csv('database.csv')
    data = copy.copy(df.iloc[-1])
    data[user] += amount
    df.loc[len(df)] = data
    df.to_csv('database.csv', index=False)
    

def WithdrawCash(user, amount):
    DepositCash(user, -1*amount)

def ApplyInterest(user, percentage):
    df = pd.read_csv('database.csv')
    data = copy.copy(df.iloc[-1])
    data[user] = data[user]*(1+percentage/100)
    df.loc[len(df)] = data
    df.to_csv('database.csv', index=False)

def CheckBalance():
    df = pd.read_csv('database.csv')
    data = df.iloc[-1]
    print(dict(data))


CheckBalance()
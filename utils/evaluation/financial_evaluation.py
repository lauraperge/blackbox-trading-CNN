import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os


def financial_evaluation(prices, signals, initial_capital = 10000.0, trading_commission= 1.0):
    """ 
    Returns financial evaluation measurements of an algorithmic trading strategy given prices and relevant trading signals.
    Assets are traded in any increments.

    Parameters
    -------------------------------
        prices : np.array or pd.Series (float)
            array, series of prices
        
        signals : np.array or pd.Series (string array of ["Buy", "Sell", "Hold"])
            array or series of trading signals, directly mapped to the prices

        initial_capital : np.float (default = 10000.0)
            amount of initial investment (capital)

        trading_commission : np.float (default = 1.0)
            amount subtracted from the capital per executed trade
    
    Returns
    ------------------------------
        cumulative_return : np.float
            (ending_capital - init_capital)/init_capital
        
        annualized_return_pct : np.float
            compounded annual return percentage
        
        all_trades : np.int
            number of trades carried out
        
        winners : np.int
            total number of winning trades
        
        losers : np.int
            total number of losing trades

        success_ratio : np.float
            winners/all_trades
        
        total_transaction_cost : np.float
            total amount spent on transaction fees
        
        avg_trade_profit : np.float
            total_profit/winners
        
        avg_trade_loss : np.float
            total_loss/losers

        num_buys : np.int
            number of executed buy orders

        num_sells : np.int
            number of executed sell orders

    """
    # list to track owned capital
    capital = []
    # initial capital
    capital.append(initial_capital)

    # list to track number of units in possession at each time step
    num_units = []
    # initial
    num_units.append(0)

    # list to track amount of cash owned
    money = []
    # initial cash
    money.append(initial_capital)



    # list to track number of profiting trades
    winners = 0
    # list to track number of losing trades
    losers = 0

    # variables to track number of executed trades
    buys = 0
    sells = 0

    # track transaction costs
    total_transaction_cost = 0

    for idx, order in enumerate(signals):
        if order == "Buy":
            ## given there is cash to spend
            if money[-1] != 0:
                ## amount of units bought, trading fee
                num_units.append((money[-1]-trading_commission)/prices[idx])
                total_transaction_cost += trading_commission

                ## increase number of executed buy orders
                buys += 1

                ## update money
                money.append(0)

                ## tracking capital
                capital.append(prices[idx] * num_units[-1])

                if capital[-1] > capital[-2]:
                    winners += 1
                elif capital[-1] < capital [-2]:
                    losers +=1
            else:
                ## HOLD
                ## still tracking
                num_units.append(num_units[-1])
                money.append(money[-1])

                ## tracking capital
                capital.append(prices[idx] * num_units[-1])

        elif order == "Sell":
            ## given there are units of the asset to sell
            if num_units[-1] != 0:
                ## amount of money received for sold units, trading fee
                money.append(num_units[-1] * prices[idx] - trading_commission)
                total_transaction_cost += trading_commission

                ## increase number of executed sell orders
                sells += 1

                ## update number of units
                num_units.append(0)

                ## tracking capital
                capital.append(money[-1])

                ## check if we won or lost with the trade
                if capital[-1] > capital[-2]:
                    winners += 1
                elif capital[-1] < capital[-2]:
                    losers += 1

            else:
                ## HOLD
                ## still tracking
                num_units.append(num_units[-1])
                money.append(money[-1])

                ## tracking capital
                capital.append(money[-1])

        elif order == "Hold":
            ## still tracking 
            num_units.append(num_units[-1])
            money.append(money[-1])

            ## tracking capital too
            if money[-1] != 0:
                capital.append(money[-1])
            else:
                capital.append(prices[idx] * num_units[-1])

    ending_capital = capital[-1]

    cumulative_return = (ending_capital - initial_capital) / initial_capital

    annualized_return = (ending_capital/initial_capital)**(260/(len(capital)-1)) - 1

    all_trades = buys + sells

    success_ratio = winners/all_trades

    if (ending_capital - initial_capital) > 0:
        avg_trade_profit = (ending_capital - initial_capital) / winners
        avg_trade_loss = None
    elif (ending_capital - initial_capital) < 0:
        avg_trade_profit = None
        avg_trade_loss = (ending_capital - initial_capital) / losers
    else:
        avg_trade_profit = None
        avg_trade_loss = None



    return cumulative_return, annualized_return, all_trades, winners, losers, success_ratio, total_transaction_cost, avg_trade_profit, avg_trade_loss, buys, sells

if __name__ == "__main__":
    prices = [.1, .5, .2, 1.1, .4, .8, .55, .12, .3, .14]
    signals = ["Sell", "Buy", "Hold", "Hold", "Buy", "Sell", "Hold", "Buy", "Buy", "Hold"]

    print(financial_evaluation(prices,signals))

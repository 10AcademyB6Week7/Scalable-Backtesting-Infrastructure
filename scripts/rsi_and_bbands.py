import pandas as pd
import vectorbt as vbt
import yfinance as yf


#
def rsi_backtest(coin):
    coin_price = vbt.YFData.download(coin, missing_index='drop').get("Close")
    coin_rsi = vbt.RSI.run(coin_price)
    entries = coin_rsi.rsi_crossed_below(30)
    exits = coin_rsi.rsi_crossed_above(70)

    # set up portfolio
    pf = vbt.Portfolio.from_signals(coin_price, entries, exits)
    ret = pf.total_return()
    sr = pf.sharpe_ratio()
    max_drawdown = pf.max_drawdown()
    num_trades = pf.stats()[11]
    percent_avg_win_trades = pf.stats()[18]
    percent_avg_loss_trades = pf.stats()[19]
    metrics = {"Return": ret, 
               "Number of trades": num_trades,
               "Winning trades (%)": percent_avg_win_trades,
               "Losing trades (%)": percent_avg_loss_trades,
              "Max drawdown": max_drawdown, "Sharpe ratio": sr}
    return metrics, pf
    
def bbands_backtests(coin):
    coin_price = vbt.YFData.download("BTC-USD", missing_index='drop').get("Close")
    coin_bbands = vbt.BBANDS.run(coin_price)
    entries = coin_bbands.close_crossed_below(coin_bbands.lower)
    exits = coin_bbands.close_crossed_above(coin_bbands.upper)
   
     # set up portfolio
    pf = vbt.Portfolio.from_signals(coin_price, entries, exits)
    ret = pf.total_return()
    sr = pf.sharpe_ratio()
    max_drawdown = pf.max_drawdown()
    num_trades = pf.stats()[11]
    percent_avg_win_trades = pf.stats()[18]
    percent_avg_loss_trades = pf.stats()[19]
    metrics = {"Return": ret, 
               "Number of trades": num_trades,
               "Winning trades (%)": percent_avg_win_trades,
               "Losing trades (%)": percent_avg_loss_trades,
              "Max drawdown": max_drawdown, "Sharpe ratio": sr}
    return metrics, pf    
    
    

def plot_pf(met):
    mets = met[0]
    for key,value in mets.items():
        print(key, " => ", value)
    met[1].plot().show()
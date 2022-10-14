import vectorbt as vbt
import pandas as pd



amz = vbt.YFData.download(
    ["AMZN"],
    start = "2021-10-14",
    end = "2022-10-13",
    missing_index = 'drop'
).get(["Close","Volume"])



# custom indicator 
def custom_ind(d_close,d_volume, sma_window,fma_window):
    
    amz_price =d_close
    amz_volume = d_volume
    df = pd.DataFrame()
    df["Close"] = d_close
    df["Volume"] = d_volume
    df["price_SMA"] = vbt.MA.run(amz_price,sma_window).ma
    df["price_FMA"] = vbt.MA.run(amz_price,fma_window).ma

    obv = vbt.OBV.run(close = amz_price,volume=amz_volume)
    df["OBV"] = obv.obv
    df["OBV_EMA"] = obv.obv.ewm(span=fma_window).mean()

    signal = []
    for i in range(0, len(df)):
      if df["OBV"][i] > df["OBV_EMA"][i] and df["price_FMA"][i]>df["price_SMA"][i]:
        flag = 1
      elif df["OBV"][i] < df["OBV_EMA"][i] and df["price_FMA"][i]<df["price_SMA"][i]:
        flag = -1
      else:
        flag = 0
      signal.append(flag)
    return signal


ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["d_close","d_volume"],
    param_names = ["sma_window","fma_window"],
    output_names = ["value"]
).from_apply_func(
    custom_ind,
    sma_window=50,
    fma_window=14,
    keep_pd=True # everything stays in pandas format
    # which makes the computation expensive, but allows us to use pandas features
)

res = ind.run(
    d_close=amz["Close"],
    d_volume=amz["Volume"],
    sma_window = [30,40,50,60,75,90,100],
    fma_window = [5,7,9,12],
    param_product = True

    
)

exits = res.value == -1
entries = res.value == 1

pf = vbt.Portfolio.from_signals(amz["Close"],entries,exits,init_cash=10000,fees=0.05)

print(pf.total_return())
returns = pf.total_return()
print(returns.idxmax())
print(returns.idxmin())





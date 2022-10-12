import vectorbt as vbt


class VectorbotPipeline():
    def __init__(self, init_cash=100, stock='LTC-USD', fast_ma=10, slow_ma=50, start='2021-10-10', end='2022-10-10', period=None, fees=0.005):
        self.init_cash = init_cash
        self.stock = stock
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.start = start
        self.end = end
        self.period = period
        self.fees = fees
        self.price = vbt.YFData.download(self.stock, start=self.start, end=self.end).get('Close')

    def setup_from_holding(self):
        self.pf = vbt.Portfolio.from_holding(self.price, init_cash=self.init_cash)
    
    def setup_sma(self):
        # price = vbt.YFData.download(self.stock, start=self.start, end=self.end).get('Close')
        self.calc_fast_ma = vbt.MA.run(self.price, self.fast_ma, short_name='fast_ma')
        self.calc_slow_ma = vbt.MA.run(self.price, self.slow_ma, short_name='slow_ma')
        entries = self.calc_fast_ma.ma_crossed_above(self.calc_slow_ma)
        exits = self.calc_fast_ma.ma_crossed_below(self.calc_slow_ma)
        self.pf = vbt.Portfolio.from_signals(self.price, entries, exits, init_cash=self.init_cash)

    def readbale_records(self):
        print(self.pf.orders.records_readable)
        print(self.pf.total_profit())

    def plot(self):
        fig = self.price.vbt.plot(trace_kwargs=dict(name='Close'))
        self.calc_fast_ma.ma.vbt.plot(trace_kwargs=dict(name='Fast MA'), fig=fig)
        self.calc_slow_ma.ma.vbt.plot(trace_kwargs=dict(name='Slow MA'), fig=fig)
        self.pf.positions.plot(close_trace_kwargs=dict(visible=False), fig=fig)
        # vbt.save('fig.png', fig)
        with open('img.png','wb') as f:
            f.write(fig.to_image(format='png'))

    


if __name__ == '__main__':
    vbtp = VectorbotPipeline()
    vbtp.setup_sma()
    vbtp.readbale_records()
    vbtp.plot()
    vbtp.setup_from_holding()
    vbtp.readbale_records()
import yfinance as yf
import pandas as pd

def tickDataload(ticker_list, start_date=None, end_date=None):
   df_download = yf.download(ticker_list, start=start_date, end=end_date).swaplevel(0,1, axis=1).sort_index(axis=1)

   dict_tickers = {}
   dict_tickers.update({ticker_:df_download[ticker_] for ticker_ in ticker_list})
   
   if '^GSPC' in list(dict_tickers.keys()):
      dict_tickers['SP500'] = dict_tickers.pop('^GSPC')
   if '^IXIC' in list(dict_tickers.keys()):
      dict_tickers['NASDAQ'] = dict_tickers.pop('^IXIC')
   if '^KS11' in list(dict_tickers.keys()):
      dict_tickers['KOSPI'] = dict_tickers.pop('^KS11')
   if '^KQ11' in list(dict_tickers.keys()):
      dict_tickers['KOSDAQ'] = dict_tickers.pop('^KQ11')

   return dict_tickers

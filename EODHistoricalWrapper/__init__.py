import requests
import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
    
class EODHistorical:
    
    class Fundamentals:
        
        class Earnings:
            def __init__(self, data):
                self.data = data
                
                self.history = pd.DataFrame(data['History'])
                self.trend = pd.DataFrame(data['Trend'])
                self.annual = pd.DataFrame(data['Annual'])
        
        class Financials:
            def __init__(self, data):
                self.data = data
                
                self.balance_sheet_quarterly = pd.DataFrame(data['Balance_Sheet']['quarterly'])
                self.balance_sheet_yearly = pd.DataFrame(data['Balance_Sheet']['yearly'])
                
                self.cash_flow_quarterly = pd.DataFrame(data['Cash_Flow']['quarterly'])
                self.cash_flow_yearly = pd.DataFrame(data['Cash_Flow']['yearly'])
                
                self.income_statement_quarterly = pd.DataFrame(data['Income_Statement']['quarterly'])
                self.income_statement_yearly = pd.DataFrame(data['Income_Statement']['yearly'])
                
        def __init__(self, api_key, symbol, allow_empty):
            # Get Fundamentals
            res = requests.get('https://eodhistoricaldata.com/api/fundamentals/%s?api_token=%s' % (symbol, api_key))

            if ((res.status_code >= 300) | (res.status_code < 200)) & (res.status_code < 400):
                raise ConnectionError('Fundamentals: Connection Error')
            
            if res.status_code == 404:
                if allow_empty:
                    self.general = None
                    self.highlights = None
                    self.valuation = None
                    self.sharesstats = None
                    self.technicals = None
                    self.splitsdividends = None
                    
                    self.earnings = None
                    self.financials = None
                else:
                    raise KeyError('Cannot retrieve Fundamentals for Symbol.')
            else:
                data = res.json()
                
                if 'General' in data.keys():
                    self.general = data['General']
                elif allow_empty:
                    self.general = None
                else:
                    raise KeyError('Cannot retrieve General for Symbol.')
                    
                if 'Highlights' in data.keys():
                    self.highlights = data['Highlights']
                elif allow_empty:
                    self.highlights = None
                else:
                    raise KeyError('Cannot retrieve Highlights for Symbol.')
                
                if 'Valuation' in data.keys():
                    self.valuation = data['Valuation']
                elif allow_empty:
                    self.valuation = None
                else:
                    raise KeyError('Cannot retrieve Valuation for Symbol.')
                    
                if 'SharesStats' in data.keys():
                    self.sharesstats = data['SharesStats']
                elif allow_empty:
                    self.sharesstats = None
                else:
                    raise KeyError('Cannot retrieve SharesStats for Symbol.')
                    
                if 'Technicals' in data.keys():
                    self.technicals = data['Technicals']
                elif allow_empty:
                    self.technicals = None
                else:
                    raise KeyError('Cannot retrieve Technicals for Symbol.')
                
                if 'SplitsDividends' in data.keys():
                    self.splitsdividends = data['SplitsDividends']
                elif allow_empty:
                    self.splitsdividends = None
                else:
                    raise KeyError('Cannot retrieve SplitsDividends for Symbol.')
                
                if 'Earnings' in data.keys():
                    self.earnings = EODHistorical.Fundamentals.Earnings(data['Earnings'])
                elif allow_empty:
                    self.earnings = None
                else:
                    raise KeyError('Cannot retrieve Earnings for Symbol.')
                
                if 'Financials' in data.keys():
                    self.financials = EODHistorical.Fundamentals.Financials(data['Financials'])
                elif allow_empty:
                    self.financials = None
                else:
                    raise KeyError('Cannot retrieve Financials for Symbol.')
        
    class Historical:
        def __init__(self, api_key, symbol, allow_empty):
            res = requests.get('https://eodhistoricaldata.com/api/shorts/%s?api_token=%s&fmt=json' % (symbol, api_key))
            
            if ((res.status_code >= 300) | (res.status_code < 200)) & (res.status_code < 400):
                raise ConnectionError('Short Interests: Connection Error')
            
            if res.status_code == 404:
                #if allow_empty:
                #    self.short_interest = None
                #else:
                #    raise KeyError('Cannot retrieve Short Interests for Symbol.')
                self.short_interest = pd.DataFrame([])
            else:
                self.short_interest = pd.DataFrame(res.json())
            
            res = requests.get('https://eodhistoricaldata.com/api/div/%s?api_token=%s&fmt=json' % (symbol, api_key))
            if ((res.status_code >= 300) | (res.status_code < 200)) & (res.status_code < 400):
                raise ConnectionError('Dividends: Connection Error')
            
            if res.status_code == 404:
                if allow_empty:
                    self.dividends = None
                else:
                    raise KeyError('Cannot retrieve Dividends for Symbol.')
            else:
                self.dividends = pd.DataFrame(res.json())
            
            res = requests.get('https://eodhistoricaldata.com/api/splits/%s?api_token=%s&fmt=json' % (symbol, api_key))
            if ((res.status_code >= 300) | (res.status_code < 200)) & (res.status_code < 400):
                raise ConnectionError('Splits: Connection Error')
            
            if res.status_code == 404:
                if allow_empty:
                    self.splits = None
                else:
                    raise KeyError('Cannot retrieve Splits for Symbol.')
            else:
                self.splits = pd.DataFrame(res.json())
            
            res = requests.get('https://eodhistoricaldata.com/api/eod/%s?api_token=%s&fmt=json' % (symbol, api_key))
            if ((res.status_code >= 300) | (res.status_code < 200)) & (res.status_code < 400):
                raise ConnectionError('EOD: Connection Error')
            
            if res.status_code == 404:
                if allow_empty:
                    self.prices = None
                else:
                    raise KeyError('Cannot retrieve EOD for Symbol.')
            else:
                self.prices = pd.DataFrame(res.json())
            
    def __init__(self, api_key, symbol, allow_empty=True):
        self.fundamentals = EODHistorical.Fundamentals(api_key, symbol, allow_empty)
        self.historical = EODHistorical.Historical(api_key, symbol, allow_empty)
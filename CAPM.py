import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

RISK_FREE_RATE = 0.05
MONTHS_IN_YEAR = 12

class CAPM:
    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
    
    def download_data(self):
        data = {}
        
        for stock in self.stocks:
            ticker = yf.download(stock, self.start_date, self.end_date)
            data[stock] = ticker['Adj Close']
            
        return pd.DataFrame(data)
    
    def initialize(self):
        stock_data = self.download_data()
        print(stock_data)
        
        stock_data = stock_data.resample('M').last()
        self.data = pd.DataFrame({'s_adjclose': stock_data[self.stocks[0]], 'm_adjclose': stock_data[self.stocks[1]]})
        
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']] /
                                                       self.data[['s_adjclose', 'm_adjclose']].shift(1))
        self.data = self.data.dropna()  # Drop the first row with NaN values due to shift
        
    def calculate_beta(self):
        covariance_matrix = np.cov(self.data["s_returns"], self.data["m_returns"])
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print("Beta from the formula: ", beta)
    
    def regression(self):
        beta,alpha = np.polyfit(self.data['m_returns'],self.data['s_returns'],deg =1 )
        print("beta from regression is : ",beta)
        expected_return = RISK_FREE_RATE + beta * (self.data['m_returns'].mean()*MONTHS_IN_YEAR-RISK_FREE_RATE)
        print("Expected return : ",expected_return)
        self.plot_regression(alpha,beta)
        
    def plot_regression(self,alpha,beta):
        fig,axis = plt.subplots(1,figsize =(20,10))
        axis.scatter(self.data["m_returns"],self.data["s_returns"],label = "Data points")
        axis.plot(self.data["m_returns"],beta*self.data["m_returns"]+alpha,color = 'red',label = 'CAPM Line')
        
        plt.title('CAPM, finding alpha and beta')
        plt.xlabel("Market Return $R_m$", fontsize = 18)
        plt.ylabel("Stock Return $R_a$")
        plt.text(0.08,0.05,r'$R_a = \beta * R_m + \alpha$',fontsize = 18)
        plt.legend()
        plt.grid(True)
        plt.show()        

if __name__ == '__main__':
    capm = CAPM(['IBM', '^GSPC'], '2010-01-01', '2017-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()

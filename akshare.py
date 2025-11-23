import akshare as ak

stocks = [
    ("002555", "sanqiyule"),
    ("002624", "wanmeishijie"), 
    ("600588", "yongyouwangluo"),
    ("688111", "jinshanbangong"),
    ("000063", "zhongxingtongxun"),
    ("002475", "lixunjingmi")
]

for code, name in stocks:
    # Get stock data
    stock_data = ak.stock_zh_a_hist(symbol=code,
                                    period="daily", 
                                    start_date="20160901",
                                    end_date="20250831", 
                                    adjust="qfq")  
    """
    qfq is used to adjust stock price K-line charts. 
    By retrospectively adjusting historical prices, it eliminates price 'gaps' caused by dividends, stock splits, and other actions.
    allowing the stock price trend to remain continuous and truly comparable.
    """

    # Save to CSV
    filename = f"{name}_{code}_history.csv"
    stock_data.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"{name} data saved to {filename}")
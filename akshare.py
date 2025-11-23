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
    
    # Save to CSV
    filename = f"{name}_{code}_history.csv"
    stock_data.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"{name} data saved to {filename}")
import pandas as pd
import streamlit as st

@st.cache_data
def load_stock_data():
    stock_paths = {
        '002555': r"D:\final_project\data\002555sanqiyule.csv",
        '002624': r"D:\final_project\data\002624_wanmeishijie.csv", 
        '600588': r"D:\final_project\data\600588_yongyouwangluo.csv",
        '688111': r"D:\final_project\data\688111_jinshanbangong.csv",
        '000063': r"D:\final_project\data\000063_zhongxingtongxun.csv",
        '002475': r"D:\final_project\data\002475_lixunjingmi.csv"
    }
    
    stocks = {}
    for code, path in stock_paths.items():
        try:
            df = pd.read_csv(path)
            
            if '日期' in df.columns:
                df['Date'] = pd.to_datetime(df['日期'])
            elif 'date' in df.columns:
                df['Date'] = pd.to_datetime(df['date'])
            else:
                df['Date'] = pd.to_datetime(df.iloc[:, 0])
            
            df.set_index('Date', inplace=True)
            
            if '收盘' in df.columns:
                close_col = '收盘'
            elif 'close' in df.columns:
                close_col = 'close'
            elif 'Close' in df.columns:
                close_col = 'Close'
            else:
                close_col = df.columns[3]
            
            df['Returns'] = df[close_col].pct_change().fillna(0)    #df['Returns'] = df[close_col].pct_change().fillna(0)
            stocks[code] = df
            
        except Exception as e:
            st.error(f"Error loading {code}: {e}")
    
    return stocks
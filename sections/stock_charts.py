import streamlit as st
import plotly.graph_objects as go

def render_stock_charts(stocks):
    st.header("2. Stock Price Charts (Candlestick)")
    st.write("This section displays candlestick charts showing opening, closing, high, and low prices.")
    
    selected_stock = st.selectbox("Select Stock for Detailed View:", list(stocks.keys()))
    
    if selected_stock in stocks:
        df = stocks[selected_stock].copy()
        
        if '开盘' in df.columns and '收盘' in df.columns and '最高' in df.columns and '最低' in df.columns:
            open_col, high_col, low_col, close_col = '开盘', '最高', '最低', '收盘'
        elif 'open' in df.columns and 'close' in df.columns and 'high' in df.columns and 'low' in df.columns:
            open_col, high_col, low_col, close_col = 'open', 'high', 'low', 'close'
        elif 'Open' in df.columns and 'Close' in df.columns and 'High' in df.columns and 'Low' in df.columns:
            open_col, high_col, low_col, close_col = 'Open', 'High', 'Low', 'Close'
        else:
            open_col, high_col, low_col, close_col = df.columns[2], df.columns[4], df.columns[5], df.columns[3]
        
        fig = go.Figure(data=[go.Candlestick(
            x=df.index[-100:],
            open=df[open_col].tail(100),
            high=df[high_col].tail(100),
            low=df[low_col].tail(100),
            close=df[close_col].tail(100),
            name=selected_stock
        )])
        
        df['MA5'] = df[close_col].rolling(window=5).mean()
        df['MA10'] = df[close_col].rolling(window=10).mean()
        df['MA30'] = df[close_col].rolling(window=30).mean()
        
        fig.add_trace(go.Scatter(
            x=df.index[-100:], y=df['MA5'].tail(100),
            mode='lines', name='MA5',
            line=dict(color='orange', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index[-100:], y=df['MA10'].tail(100),
            mode='lines', name='MA10', 
            line=dict(color='green', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index[-100:], y=df['MA30'].tail(100),
            mode='lines', name='MA30',
            line=dict(color='red', width=1)
        ))
        
        fig.update_layout(
            title=f'{selected_stock} Candlestick Chart with Moving Averages',
            xaxis_title='Date',
            yaxis_title='Price',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Candlestick Chart Indicators**:
    - **Candlestick and moving average**: Shows price trend. Red and green candles represent price movements
    - **Moving averages**: Indicate trend direction
    """)
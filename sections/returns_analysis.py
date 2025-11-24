import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def render_returns_analysis(stocks):
    st.header("3. Returns Analysis")
    st.write("This section analyzes daily returns and their distribution.")
    
    returns_data = pd.DataFrame()
    for code, df in stocks.items():
        returns_data[code] = df['Returns']
    
    st.subheader("Cumulative Returns Over Time")
    cumulative_returns = (1 + returns_data).cumprod()   #Calculate cumulative returns
    
    fig_returns = go.Figure()
    for column in cumulative_returns.columns:
        fig_returns.add_trace(go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns[column],
            name=column,
            mode='lines'
        ))
    
    fig_returns.update_layout(
        title="Cumulative Returns of All Stocks",
        xaxis_title="Date",
        yaxis_title="Cumulative Returns",
        height=400
    )
    st.plotly_chart(fig_returns, use_container_width=True)
    
    st.subheader("Individual Stock Performance Metrics")
    
    performance_data = []      #Calculation Metrics
    for code in stocks.keys():
        returns = returns_data[code].dropna()
        total_return = cumulative_returns[code].iloc[-1] - 1
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0
        
        performance_data.append({
            'Stock': code,
            'Total Return': total_return,
            'Annual Return': annual_return,
            'Annual Volatility': annual_volatility,
            'Sharpe Ratio': sharpe_ratio
        })
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True)
    st.info("""
    **Performance Metrics**:
    - **Total Return**: Overall gain/loss over investment period
    - **Annualized Return**: Average rate of return per year
    - **Annualized Volatility**: Degree of price fluctuation
    - **Sharpe Ratio**: Risk-adjusted return measure
    """)
    
    st.subheader("Risk-Return Scatter Plot")
    st.write("Compare absolute performance of 6 stocks (return vs. risk)")
    
    fig_scatter = go.Figure()
    
    for _, row in performance_df.iterrows():
        fig_scatter.add_trace(go.Scatter(
            x=[row['Annual Volatility']],
            y=[row['Annual Return']],
            mode='markers+text',
            name=row['Stock'],
            text=row['Stock'],
            textposition="middle center",
            marker=dict(
                size=15,
                color='blue',
                opacity=0.7
            ),
            hovertemplate=f"<b>{row['Stock']}</b><br>" +
                         f"Annual Return: {row['Annual Return']:.2%}<br>" +
                         f"Annual Volatility: {row['Annual Volatility']:.2%}<br>" +
                         f"Sharpe Ratio: {row['Sharpe Ratio']:.2f}<extra></extra>"
        ))

    fig_scatter.update_layout(
        title="Risk-Return Profile of Stocks",
        xaxis_title="Annual Volatility (Risk)",
        yaxis_title="Annual Return",
        height=500,
        showlegend=False,
        hovermode='closest'
    )
    
    avg_return = performance_df['Annual Return'].mean()
    avg_volatility = performance_df['Annual Volatility'].mean()
    
    fig_scatter.add_hline(y=avg_return, line_dash="dash", line_color="red", 
                         annotation_text="Average Return")
    fig_scatter.add_vline(x=avg_volatility, line_dash="dash", line_color="red",
                         annotation_text="Average Volatility")
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.info("""
    **Interpretation Guide**:
    - **Top-Left**: High return, low risk (ideal)
    - **Top-Right**: High return, high risk (aggressive)  
    - **Bottom-Left**: Low return, low risk (conservative)
    - **Bottom-Right**: Low return, high risk (poor)
    """)
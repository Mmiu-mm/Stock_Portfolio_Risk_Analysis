import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(weights * mean_returns)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return std, returns

def render_portfolio_optimization(stocks):
    st.header("5. Portfolio Optimization")
    st.write("This section constructs optimal portfolios using Modern Portfolio Theory.")
    
    returns_data = pd.DataFrame()
    for code, df in stocks.items():
        returns_data[code] = df['Returns']
    
    mean_returns = returns_data.mean() * 252
    cov_matrix = returns_data.cov() * 252
    
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    weight_list = []
    
    for i in range(num_portfolios):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        weight_list.append(weights)
        
        portfolio_std, portfolio_return = portfolio_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std
        results[1,i] = portfolio_return
        results[2,i] = portfolio_return / portfolio_std
    
    results_df = pd.DataFrame(results.T, columns=['Volatility', 'Return', 'Sharpe'])
    weights_df = pd.DataFrame(weight_list, columns=list(stocks.keys()))
    
    max_sharpe_idx = results_df['Sharpe'].idxmax()
    min_vol_idx = results_df['Volatility'].idxmin()
    
    st.subheader("Efficient Frontier")
    
    fig_frontier = go.Figure()
    
    fig_frontier.add_trace(go.Scatter(
        x=results_df['Volatility'],
        y=results_df['Return'],
        mode='markers',
        marker=dict(
            size=3,
            color=results_df['Sharpe'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe Ratio")
        ),
        name='Random Portfolios'
    ))
    
    fig_frontier.add_trace(go.Scatter(
        x=[results_df.loc[max_sharpe_idx, 'Volatility']],
        y=[results_df.loc[max_sharpe_idx, 'Return']],
        mode='markers',
        marker=dict(size=10, color='gold', symbol='star'),
        name='Max Sharpe Ratio'
    ))
    
    fig_frontier.add_trace(go.Scatter(
        x=[results_df.loc[min_vol_idx, 'Volatility']],
        y=[results_df.loc[min_vol_idx, 'Return']],
        mode='markers',
        marker=dict(size=10, color='red', symbol='x'),
        name='Min Volatility'
    ))
    
    fig_frontier.update_layout(
        title="Efficient Frontier - Portfolio Optimization",
        xaxis_title="Annualized Volatility",
        yaxis_title="Annualized Return",
        height=400,
        margin=dict(l=50, r=100, t=50, b=50),
        autosize=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    col1, col2 = st.columns([10, 1])
    
    with col1:
        st.plotly_chart(fig_frontier, use_container_width=True)
    
    with col2:
        st.write("")
        
    st.info("""
    **Efficient Frontier Analysis**:
    - **Minimum Volatility Portfolio**: Lowest risk configuration
    - **Maximum Sharpe Ratio Portfolio**: Highest return per unit of risk
    """)
    
    return results_df, weight_list, max_sharpe_idx, min_vol_idx, mean_returns, cov_matrix
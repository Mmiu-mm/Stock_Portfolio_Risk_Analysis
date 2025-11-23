import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render_portfolio_selection(stocks, results_df, weight_list, max_sharpe_idx, min_vol_idx):
    
    if results_df is None or weight_list is None:
        st.error("Portfolio optimization results not available. Please run optimization first.")
        return
    
    max_sharpe_weights = weight_list[max_sharpe_idx]
    min_vol_weights = weight_list[min_vol_idx]
    
    st.subheader("Portfolio Selection Rationale")
    
    max_sharpe_diversification = 1 - np.max(max_sharpe_weights)
    min_vol_diversification = 1 - np.max(min_vol_weights)
    
    max_sharpe_top3 = sorted(zip(stocks.keys(), max_sharpe_weights), key=lambda x: x[1], reverse=True)[:3]
    min_vol_top3 = sorted(zip(stocks.keys(), min_vol_weights), key=lambda x: x[1], reverse=True)[:3]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Maximum Sharpe Ratio Portfolio Analysis**")
        
        fig_pie_max = px.pie(
            values=max_sharpe_weights,
            names=list(stocks.keys()),
            title='Max Sharpe Ratio Portfolio Allocation'
        )
        st.plotly_chart(fig_pie_max, use_container_width=True)
        
        st.write(f"- **Diversification Level**: {max_sharpe_diversification:.2%}")
        st.write("- **Top 3 Holdings**:")
        for stock, weight in max_sharpe_top3:
            st.write(f"  - {stock}: {weight:.2%}")
        
        st.write("- **Strategy**: Maximize risk-adjusted returns")
        st.write("- **Suitable for**: Investors seeking best return per unit of risk")
        
        st.write("**Performance Characteristics**:")
        st.metric("Expected Return", f"{results_df.loc[max_sharpe_idx, 'Return']:.2%}")
        st.metric("Volatility", f"{results_df.loc[max_sharpe_idx, 'Volatility']:.2%}")
        st.metric("Sharpe Ratio", f"{results_df.loc[max_sharpe_idx, 'Sharpe']:.2f}")
    
    with col2:
        st.write("**Minimum Volatility Portfolio Analysis**")
        
        fig_pie_min = px.pie(
            values=min_vol_weights,
            names=list(stocks.keys()),
            title='Minimum Volatility Portfolio Allocation'
        )
        st.plotly_chart(fig_pie_min, use_container_width=True)
        
        st.write(f"- **Diversification Level**: {min_vol_diversification:.2%}")
        st.write("- **Top 3 Holdings**:")
        for stock, weight in min_vol_top3:
            st.write(f"  - {stock}: {weight:.2%}")
        
        st.write("- **Strategy**: Minimize overall risk")
        st.write("- **Suitable for**: Risk-averse investors")
        
        st.write("**Performance Characteristics**:")
        st.metric("Expected Return", f"{results_df.loc[min_vol_idx, 'Return']:.2%}")
        st.metric("Volatility", f"{results_df.loc[min_vol_idx, 'Volatility']:.2%}")
        st.metric("Sharpe Ratio", f"{results_df.loc[min_vol_idx, 'Sharpe']:.2f}")
    
    st.subheader("Portfolio Comparison")
    
    comparison_data = {
        'Metric': ['Expected Return', 'Volatility', 'Sharpe Ratio', 'Diversification'],
        'Max Sharpe': [
            f"{results_df.loc[max_sharpe_idx, 'Return']:.2%}",
            f"{results_df.loc[max_sharpe_idx, 'Volatility']:.2%}",
            f"{results_df.loc[max_sharpe_idx, 'Sharpe']:.2f}",
            f"{max_sharpe_diversification:.2%}"
        ],
        'Min Volatility': [
            f"{results_df.loc[min_vol_idx, 'Return']:.2%}",
            f"{results_df.loc[min_vol_idx, 'Volatility']:.2%}",
            f"{results_df.loc[min_vol_idx, 'Sharpe']:.2f}",
            f"{min_vol_diversification:.2%}"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    st.subheader("Portfolio Recommendation Based on Correlation Analysis")
    
    returns_data = pd.DataFrame()
    for code, df in stocks.items():
        returns_data[code] = df['Returns']
    corr_matrix = returns_data.corr()
    
    strong_positive_pairs = []
    strong_negative_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if corr_value > 0.7:
                strong_positive_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
            elif corr_value < -0.3:
                strong_negative_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
    
    if strong_positive_pairs:
        st.warning("**High Correlation Alert**:")
        st.write("Strong positive correlation (risk concentration):")
        for stock1, stock2, corr in strong_positive_pairs:
            st.write(f"- {stock1} & {stock2}: {corr:.3f}")
        st.write("Avoid heavy allocation to both stocks.")
    
    if strong_negative_pairs:
        st.success("**Diversification Opportunities**:")
        st.write("Negative correlation (good for diversification):")
        for stock1, stock2, corr in strong_negative_pairs:
            st.write(f"- {stock1} & {stock2}: {corr:.3f}")
        st.write("These pairs help reduce overall portfolio risk.")
    
    if results_df.loc[max_sharpe_idx, 'Sharpe'] > 0.5:
        st.success("""
        **RECOMMENDED: Maximum Sharpe Ratio Portfolio**
        
        **Reasoning**:
        - Superior risk-adjusted returns
        - Balanced approach
        - Suitable for most investors seeking growth
        
        **Implementation Tips**:
        - Allocate according to optimal weights
        - Monitor monthly, rebalance quarterly
        - Pay attention to correlated stock pairs
        """)
    else:
        st.info("""
        **RECOMMENDED: Minimum Volatility Portfolio**
        
        **Reasoning**:
        - Most stable returns
        - Lower risk exposure
        - Suitable for conservative investors
        
        **Implementation Tips**:
        - Allocate according to optimal weights
        - Monitor quarterly, rebalance semi-annually
        - Good during market uncertainty
        """)
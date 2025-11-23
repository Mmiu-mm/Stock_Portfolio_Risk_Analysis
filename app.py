import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sections.sidebar import render_sidebar
from sections.stock_charts import render_stock_charts
from sections.returns_analysis import render_returns_analysis
from sections.correlation_analysis import render_correlation_analysis
from sections.portfolio_optimization import render_portfolio_optimization
from sections.portfolio_selection import render_portfolio_selection
from sections.garch_model import render_garch_model
from utils.data_loader import load_stock_data

# Set page configuration
st.set_page_config(
    page_title="Stock Portfolio Risk Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(weights * mean_returns)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return std, returns

def render_project_background():
    st.header("Project Background")
    try:
        with open("project_background.txt", "r", encoding="utf-8") as file:
            background_content = file.read()
        st.markdown(background_content)
    except FileNotFoundError:
        st.error("Project background file not found.")

def render_stock_overview(stocks):
    st.subheader("1. Stock Overview")
    st.write("Basic information about the loaded stock data.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Stock Codes**")
        for code in stocks.keys():
            st.write(f"- {code}")
    
    with col2:
        st.write("**Data Period**")
        for code, df in stocks.items():
            start_date = df.index.min().strftime('%Y-%m-%d')
            end_date = df.index.max().strftime('%Y-%m-%d')
            st.write(f"{code}: {start_date} to {end_date}")
    
    with col3:
        st.write("**Data Points**")
        for code, df in stocks.items():
            st.write(f"{code}: {len(df):,} records")

def render_portfolio_optimization_section(stocks):
    st.subheader("5. Portfolio Optimization")
    st.write("This section constructs optimal portfolios considering risk-return trade-offs using Modern Portfolio Theory.")
    
    # Calculate returns data
    returns_data = pd.DataFrame()
    for code, df in stocks.items():
        returns_data[code] = df['Returns']
    
    # Calculate portfolio statistics
    mean_returns = returns_data.mean() * 252
    cov_matrix = returns_data.cov() * 252
    
    # Generate random portfolios
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
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results.T, columns=['Volatility', 'Return', 'Sharpe'])
    weights_df = pd.DataFrame(weight_list, columns=list(stocks.keys()))
    
    # Find optimal portfolios
    max_sharpe_idx = results_df['Sharpe'].idxmax()
    min_vol_idx = results_df['Volatility'].idxmin()
    
    # Plot efficient frontier
    fig_frontier = go.Figure()
    
    # Scatter plot of all portfolios
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
    
    # Mark optimal portfolios
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
        showlegend=True
    )
    
    st.plotly_chart(fig_frontier, use_container_width=True)
    
    st.info("""
    **Efficient Frontier Analysis**:
    - **Minimum Volatility Portfolio**: Located at the far left of the efficient frontier, lowest risk configuration
    - **Maximum Sharpe Ratio Portfolio**: Optimal risk-return point, highest return per unit of risk
    """)
    
    # Store results in session state
    st.session_state.portfolio_results = {
        'results_df': results_df,
        'weight_list': weight_list,
        'max_sharpe_idx': max_sharpe_idx,
        'min_vol_idx': min_vol_idx,
        'mean_returns': mean_returns,
        'cov_matrix': cov_matrix
    }

def render_portfolio_selection_section(stocks):
    st.subheader("6. Portfolio Selection")
    st.write("This section provides detailed analysis of optimal portfolio selection.")
    
    if 'portfolio_results' not in st.session_state:
        st.warning("Please run Portfolio Optimization first to get optimal portfolios.")
        return
    
    results_df = st.session_state.portfolio_results['results_df']
    weight_list = st.session_state.portfolio_results['weight_list']
    max_sharpe_idx = st.session_state.portfolio_results['max_sharpe_idx']
    min_vol_idx = st.session_state.portfolio_results['min_vol_idx']
    
    render_portfolio_selection(stocks, results_df, weight_list, max_sharpe_idx, min_vol_idx)

def render_technical_analysis(stocks):
    st.header("Technical Analysis")
    st.write("Select the analysis section you want to explore:")
    
    analysis_options = {
        "Stock Overview": "1. Stock Overview",
        "Stock Price Charts": "2. Stock Price Charts", 
        "Returns Analysis": "3. Returns Analysis",
        "Correlation Analysis": "4. Correlation Analysis",
        "Portfolio Optimization": "5. Portfolio Optimization",
        "Portfolio Selection": "6. Portfolio Selection"
    }
    
    selected_analysis = st.selectbox(
        "Choose Analysis Section:",
        list(analysis_options.keys()),
        format_func=lambda x: analysis_options[x]
    )
    
    if selected_analysis == "Stock Overview":
        render_stock_overview(stocks)
    elif selected_analysis == "Stock Price Charts":
        render_stock_charts(stocks)
    elif selected_analysis == "Returns Analysis":
        render_returns_analysis(stocks)
    elif selected_analysis == "Correlation Analysis":
        render_correlation_analysis(stocks)
    elif selected_analysis == "Portfolio Optimization":
        render_portfolio_optimization_section(stocks)
    elif selected_analysis == "Portfolio Selection":
        render_portfolio_selection_section(stocks)

def render_conclusions():
    st.header("Conclusions and Recommendations")
    
    st.subheader("Key Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Portfolio Optimization Results**")
        st.write("- Maximum Sharpe Ratio Portfolio provides optimal risk-adjusted returns")
        st.write("- Minimum Volatility Portfolio offers stable performance")
        st.write("- Diversification benefits across different stock combinations")
        
    with col2:
        st.write("**Risk Management Insights**")
        st.write("- GARCH models capture volatility clustering")
        st.write("- Correlation analysis reveals diversification opportunities")
        st.write("- Modern Portfolio Theory provides practical optimization")
    
    st.subheader("Investment Recommendations")
    
    st.info("""
    **Recommendations**:
    
    1. **Aggressive Investors**: Maximum Sharpe Ratio Portfolio for optimal returns
    2. **Conservative Investors**: Minimum Volatility Portfolio for stable performance
    3. **Portfolio Rebalancing**: Monitor quarterly, rebalance semi-annually
    4. **Risk Monitoring**: Use GARCH volatility forecasts
    """)
    
    st.subheader("Methodological Contributions")
    
    st.write("""
    This project demonstrates:
    - Application of Modern Portfolio Theory to Chinese A-shares
    - Implementation of GARCH models for volatility forecasting
    - Integration of quantitative analysis techniques
    - User-friendly visualization of financial analytics
    """)
    
    st.success("Integrated approach provides robust framework for stock portfolio risk analysis and optimization.")

def main():
    selected_module = render_sidebar()
    stocks = load_stock_data()
    
    if not stocks:
        st.error("No stock data loaded. Please check file paths and formats.")
        st.stop()
    
    if selected_module == "Project Background":
        render_project_background()
    elif selected_module == "GARCH Model":
        render_garch_model(stocks)
    elif selected_module == "Technical Analysis":
        render_technical_analysis(stocks)
    elif selected_module == "Conclusions":
        render_conclusions()

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from arch import arch_model

def fit_garch_models(returns_data):
    garch_results = {}
    volatilities = pd.DataFrame()
    failed_stocks = []
    
    for stock in returns_data.columns:
        try:
            returns = returns_data[stock].dropna()
            
            if len(returns) < 100:
                st.warning(f"Not enough data for {stock} (need at least 100 observations, got {len(returns)})")
                failed_stocks.append(stock)
                continue
            
            if returns.std() < 1e-6:   #calucate std
                st.warning(f"Returns for {stock} have very low variability")
                failed_stocks.append(stock)
                continue
                
            scaled_returns = returns * 100
            
            model = arch_model(scaled_returns, vol='Garch', p=1, q=1, 
                             mean='Constant', dist='normal')
            
            result = model.fit(disp='off', show_warning=False,       #fit the data
                             options={'maxiter': 1000, 'disp': False})
            
            if result is None or not hasattr(result, 'params'):
                st.warning(f"GARCH model failed to converge for {stock}")
                failed_stocks.append(stock)
                continue
                
            garch_results[stock] = result
            volatilities[stock] = result.conditional_volatility / 100    #gain the volatility
            
        except Exception as e:
            st.warning(f"GARCH fitting failed for {stock}: {str(e)}")
            failed_stocks.append(stock)
    
    if failed_stocks:
        st.info(f"GARCH models could not be fitted for: {', '.join(failed_stocks)}")
    
    return garch_results, volatilities

def render_garch_model(stocks):
    st.header("GARCH Volatility Modeling")
    st.write("""
    This section implements GARCH(1,1) model to estimate and forecast volatility.
    
    **GARCH Model Introduction:**
    The Generalized Autoregressive Conditional Heteroskedasticity (GARCH) model is widely used 
    in financial econometrics to model and forecast volatility. GARCH(1,1) captures the 
    volatility clustering phenomenon where periods of high volatility tend to be followed 
    by high volatility and periods of low volatility tend to be followed by low volatility.
    """)
    
    with st.expander("Learn more about GARCH Model Theory"):
        st.markdown("""
        **GARCH(1,1) Model Specification:**
        
        The GARCH(1,1) model can be written as:
        
        - **Mean Equation**: \( r_t = μ + ε_t \)
        - **Variance Equation**: \( σ_t^2 = ω + αε_{t-1}^2 + βσ_{t-1}^2 \)
        
        Where:
        - \( r_t \): Return at time t
        - \( μ \): Mean return
        - \( ε_t \): Error term at time t
        - \( σ_t^2 \): Conditional variance at time t
        - \( ω \): Constant term
        - \( α \): ARCH parameter (effect of past shock)
        - \( β \): GARCH parameter (effect of past variance)
        
        **Key Properties:**
        - **Volatility Clustering**: Captured by α and β parameters
        - **Persistence**: α + β measures volatility shock persistence
        - **Stationarity**: Requires α + β < 1
        """)
    
    with st.spinner('Fitting GARCH models... This may take a while.'):
        returns_data = pd.DataFrame()
        for code, df in stocks.items():
            returns_data[code] = df['Returns']
        
        garch_results, volatilities = fit_garch_models(returns_data)
    
    if garch_results:
        st.subheader("GARCH(1,1) Model Parameters")
        garch_params = []
        for stock, result in garch_results.items():
            try:
                params = result.params
                garch_params.append({
                    'Stock': stock,
                    'Omega (Constant)': params.get('omega', np.nan),
                    'Alpha (ARCH)': params.get('alpha[1]', np.nan),
                    'Beta (GARCH)': params.get('beta[1]', np.nan),
                    'Persistence': params.get('alpha[1]', 0) + params.get('beta[1]', 0),
                    'Log Likelihood': result.loglikelihood,
                    'AIC': result.aic,
                    'BIC': result.bic
                })
            except Exception as e:
                st.warning(f"Error extracting parameters for {stock}: {e}")
        
        if garch_params:
            garch_df = pd.DataFrame(garch_params)
            st.dataframe(garch_df, use_container_width=True)
            
            st.info("""
            **GARCH Parameter Interpretation:**
            - **Omega**: Constant term in volatility equation
            - **Alpha**: Effect of past squared returns (ARCH effect)
            - **Beta**: Effect of past volatility (GARCH effect)
            - **Persistence**: Alpha + Beta, measures volatility clustering
            - **Persistence close to 1**: Volatility shocks are highly persistent
            - **High Alpha**: Volatility is very responsive to market movements
            - **High Beta**: Volatility has strong memory of its own past
            """)
            
            st.subheader("Conditional Volatility (GARCH)")
            fig_vol = go.Figure()
            for column in volatilities.columns:
                fig_vol.add_trace(go.Scatter(
                    x=volatilities.index,
                    y=volatilities[column],
                    name=column,
                    mode='lines'
                ))
            
            fig_vol.update_layout(
                title="Conditional Volatility from GARCH(1,1) Model",
                xaxis_title="Date",
                yaxis_title="Conditional Volatility",
                height=400
            )
            st.plotly_chart(fig_vol, use_container_width=True)
            
            st.subheader("Volatility Forecast")
            st.write("Generate future volatility forecasts based on fitted GARCH models:")
            
            forecast_horizon = st.slider("Forecast Horizon (days)", 1, 30, 10)
            
            try:
                forecast_data = []
                for stock, result in garch_results.items():
                    try:
                        forecast = result.forecast(horizon=forecast_horizon)
                        forecast_variance = forecast.variance.iloc[-1] / (100**2)
                        forecast_volatility = np.sqrt(forecast_variance)
                        
                        for i, vol in enumerate(forecast_volatility):
                            forecast_data.append({
                                'Stock': stock,
                                'Day': i + 1,
                                'Forecasted Volatility': vol
                            })
                    except Exception as e:
                        st.warning(f"Forecast failed for {stock}: {e}")
                
                if forecast_data:
                    forecast_df = pd.DataFrame(forecast_data)
                    
                    fig_forecast = px.line(forecast_df, x='Day', y='Forecasted Volatility', 
                                          color='Stock', title=f'GARCH Volatility Forecast ({forecast_horizon} days)')
                    fig_forecast.update_layout(height=400)
                    st.plotly_chart(fig_forecast, use_container_width=True)
                    
                    st.subheader("Forecast Summary")
                    summary_data = []
                    for stock in forecast_df['Stock'].unique():
                        stock_forecasts = forecast_df[forecast_df['Stock'] == stock]
                        initial_vol = stock_forecasts['Forecasted Volatility'].iloc[0]
                        final_vol = stock_forecasts['Forecasted Volatility'].iloc[-1]
                        change = ((final_vol - initial_vol) / initial_vol) * 100
                        
                        summary_data.append({
                            'Stock': stock,
                            'Initial Volatility': initial_vol,
                            f'Day {forecast_horizon} Volatility': final_vol,
                            'Change (%)': change
                        })
                    
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True)
                    
            except Exception as e:
                st.warning(f"Volatility forecasting failed: {e}")
            
        else:
            st.warning("No GARCH parameters were successfully extracted.")
    else:
        st.warning("No GARCH models were successfully fitted. This could be due to:")
        st.write("- Insufficient data points")
        st.write("- Low variability in returns")
        st.write("- Numerical convergence issues")
        
        st.info("Alternative Approach: Use rolling historical volatility")
        
        returns_data = pd.DataFrame()
        for code, df in stocks.items():
            returns_data[code] = df['Returns']
            
        rolling_vol = returns_data.rolling(window=30).std() * np.sqrt(252)
        fig_alt = go.Figure()
        for column in rolling_vol.columns:
            fig_alt.add_trace(go.Scatter(
                x=rolling_vol.index,
                y=rolling_vol[column],
                name=column,
                mode='lines'
            ))
        
        fig_alt.update_layout(
            title="Rolling Historical Volatility (30-day window, Annualized)",
            xaxis_title="Date",
            yaxis_title="Annualized Volatility",
            height=400
        )
        st.plotly_chart(fig_alt, use_container_width=True)
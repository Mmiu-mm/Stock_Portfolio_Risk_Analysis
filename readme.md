# Stock Portfolio Risk Analysis System

A comprehensive web application for analyzing and optimizing stock portfolio risk using modern financial theory and quantitative methods.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

##  Project Overview

This project implements a sophisticated stock portfolio risk analysis system that applies Modern Portfolio Theory and advanced statistical models to Chinese A-shares. The system provides investors with scientific tools for portfolio optimization, risk assessment, and investment decision-making.

###  Key Objectives
- Build complete portfolio risk analysis system
- Apply modern portfolio theory to Chinese markets
- Develop intuitive risk visualization dashboard
- Provide scientific decision support tools

##  System Architecture

```
project/
├── app.py                 # Main application entry point
├── sections/              # Analysis modules
│   ├── sidebar.py         # Navigation sidebar
│   ├── stock_charts.py    # Price visualization
│   ├── returns_analysis.py # Returns analysis
│   ├── correlation_analysis.py # Correlation studies
│   ├── portfolio_optimization.py # MPT implementation
│   ├── portfolio_selection.py # Portfolio recommendations
│   └── garch_model.py    # Volatility modeling
├── utils/
│   └── data_loader.py    # Data management
└── requirements.txt      # Dependencies
```

##  Technical Analysis Modules

### 1. Stock Price Analysis
- **Candlestick Charts**: Interactive price charts with moving averages (MA5, MA10, MA30)
- **Technical Indicators**: Multiple timeframe analysis for trend identification
- **Visual Analytics**: Real-time price movement visualization

### 2. Returns Analysis
- **Cumulative Returns**: Performance tracking over time
- **Risk-Return Profiles**: Individual stock performance metrics
- **Sharpe Ratios**: Risk-adjusted return calculations
- **Comparative Analysis**: Side-by-side stock performance comparison

### 3. Correlation Analysis
- **Correlation Matrix**: Heatmap visualization of stock relationships
- **Diversification Analysis**: Identification of uncorrelated assets
- **Portfolio Benefits**: Quantification of diversification advantages

### 4. Portfolio Optimization (Modern Portfolio Theory)
- **Efficient Frontier**: Optimal risk-return portfolios
- **Random Portfolio Generation**: 10,000+ portfolio simulations
- **Optimization Algorithms**: Minimum variance and maximum Sharpe ratio portfolios
- **Weight Allocation**: Scientific asset distribution recommendations

### 5. GARCH Volatility Modeling
- **Volatility Forecasting**: Conditional variance predictions
- **Risk Clustering**: Identification of volatility patterns
- **Statistical Modeling**: ARCH/GARCH parameter estimation
- **Forecast Horizon**: Customizable prediction periods (1-30 days)

##  Dataset

### Stock Coverage
- **6 Representative A-Shares**: Cross-industry selection with varied market capitalizations
- **Industries**: Entertainment, Technology, Telecommunications, Manufacturing
- **Time Period**: September 2016 - August 2025

### Included Stocks
| Stock Code | Company | Industry |
|------------|---------|----------|
| 002555 | Sanqi Mutual Entertainment | Entertainment |
| 002624 | Perfect World | Gaming/Entertainment |
| 600588 | Yongyou Network | Enterprise Software |
| 688111 | Kingsoft Office | Office Software |
| 000063 | ZTE Corporation | Telecommunications |
| 002475 | Luxshare Precision | Electronics Manufacturing |

##  Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/Mmiu-mm/Stock_Portfolio_Risk_Analysis.git
cd Stock_Portfolio_Risk_Analysis

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Dependencies
```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.13.0
arch>=5.3.0
matplotlib>=3.5.0
```

##  Usage Guide

### Starting the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Navigation
1. **Project Background**: Overview and objectives
2. **Technical Analysis**: Comprehensive stock analysis modules
3. **GARCH Model**: Advanced volatility forecasting
4. **Conclusions**: Investment recommendations and insights

### Technical Analysis Modules
1. **Stock Overview**: Basic data information and statistics
2. **Stock Charts**: Interactive price visualization
3. **Returns Analysis**: Performance metrics and comparisons
4. **Correlation Analysis**: Inter-stock relationship studies
5. **Portfolio Optimization**: Efficient frontier construction
6. **Portfolio Selection**: Optimal portfolio recommendations

##  Key Features

### Interactive Visualizations
- **Plotly Charts**: Dynamic, interactive financial charts
- **Real-time Updates**: Live data processing and visualization
- **Customizable Parameters**: Adjustable analysis parameters
- **Responsive Design**: Mobile-friendly interface

### Advanced Analytics
- **Modern Portfolio Theory**: Scientific portfolio construction
- **Risk Quantification**: Volatility and Value-at-Risk metrics
- **Statistical Modeling**: GARCH for volatility forecasting
- **Performance Metrics**: Comprehensive return calculations

### User Experience
- **Intuitive Interface**: Streamlit-powered web application
- **Modular Design**: Independent analysis components
- **Educational Content**: Explanatory notes and interpretations
- **Professional Reporting**: Investment-grade analytics

##  Methodological Framework

### Modern Portfolio Theory (MPT)
- Efficient frontier construction
- Risk-return optimization
- Diversification benefits quantification
- Minimum variance and optimal portfolios

### Time Series Analysis
- GARCH(1,1) volatility modeling
- Conditional heteroskedasticity
- Volatility clustering detection
- Multi-period forecasting

### Statistical Methods
- Correlation analysis
- Returns distribution modeling
- Risk metric calculations
- Performance attribution

##  Investment Applications

### Portfolio Construction
- **Optimal Asset Allocation**: Scientific weight determination
- **Risk Management**: Volatility-based position sizing
- **Diversification Strategy**: Correlation-based asset selection

### Risk Assessment
- **Volatility Forecasting**: GARCH-based risk predictions
- **Scenario Analysis**: Stress testing capabilities
- **Sensitivity Analysis**: Parameter impact assessment

### Decision Support
- **Quantitative Recommendations**: Data-driven investment advice
- **Performance Monitoring**: Continuous portfolio evaluation
- **Strategic Insights**: Market condition interpretations

##  Technical Implementation

### Data Processing
```python
# Automated data loading and preprocessing
@st.cache_data
def load_stock_data():
    # Handles multiple data formats and column naming conventions
    # Automatic returns calculation and data validation
```

### Portfolio Optimization
```python
def portfolio_performance(weights, mean_returns, cov_matrix):
    # Implements Modern Portfolio Theory calculations
    # Handles large-scale portfolio simulations
```

### GARCH Modeling
```python
def fit_garch_models(returns_data):
    # Robust GARCH(1,1) implementation
    # Comprehensive error handling and convergence checks
```

##  Results Interpretation

### Portfolio Recommendations
- **Maximum Sharpe Ratio Portfolio**: Optimal risk-adjusted returns
- **Minimum Volatility Portfolio**: Lowest risk configuration
- **Custom Portfolios**: Risk-profile based allocations

### Risk Insights
- **Volatility Patterns**: Market condition assessments
- **Correlation Structures**: Diversification opportunities
- **Performance Attribution**: Return driver analysis

##  Future Enhancements

### Planned Features
- [ ] Real-time data integration
- [ ] Additional risk metrics (VaR, CVaR)
- [ ] Machine learning predictions
- [ ] Multi-asset class support
- [ ] Backtesting capabilities
- [ ] API integration for live data

### Research Extensions
- Alternative GARCH specifications
- Non-normal return distributions
- Bayesian portfolio optimization
- Behavioral finance factors

##  Contributors

- **Yalin Mo** - Developer & Researcher  
  Email: Yalin.Mo@efrei.net
- **Mano Joseph Mathew** - Project Supervisor  
  Email: mano.mathew@efrei.fr

### Academic Collaboration
- **EFREI Paris** - Graduate School of Digital Engineering
- **WUT** - Wuhan University of Technology

##  License

This project is developed for academic research purposes as part of the EFREI Data Stories program.

##  Links

- **GitHub Repository**: [Stock Portfolio Risk Analysis](https://github.com/Mmiu-mm/Stock_Portfolio_Risk_Analysis.git)
- **Streamlit Documentation**: [https://docs.streamlit.io](https://docs.streamlit.io)
- **EFREI Paris**: [https://www.efrei.fr](https://www.efrei.fr)


---

**Disclaimer**: This tool is for educational and research purposes only. Investment decisions should be made in consultation with qualified financial advisors. Past performance does not guarantee future results.
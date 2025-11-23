import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def render_correlation_analysis(stocks):
    st.header("4. Correlation Analysis")  
    st.write("This section examines correlation structure between different stocks.")
    
    # Calculate returns data
    returns_data = pd.DataFrame()
    for code, df in stocks.items():
        returns_data[code] = df['Returns']
    
    # Calculate correlation matrix
    corr_matrix = returns_data.corr()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Correlation Heatmap")
        
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        im = ax.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1)
        
        ax.set_xticks(np.arange(len(corr_matrix.columns)))
        ax.set_yticks(np.arange(len(corr_matrix.index)))
        ax.set_xticklabels(corr_matrix.columns, fontsize=7)
        ax.set_yticklabels(corr_matrix.index, fontsize=7)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        for i in range(len(corr_matrix.index)):
            for j in range(len(corr_matrix.columns)):
                text = ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                              ha="center", va="center", color="black" if abs(corr_matrix.iloc[i, j]) < 0.7 else "white",
                              fontsize=6)
        
        cbar = ax.figure.colorbar(im, ax=ax, shrink=0.7)
        cbar.ax.tick_params(labelsize=6)
        
        ax.set_title("Correlation Matrix", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Correlation Distribution")
        
        corr_values = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_values.append(corr_matrix.iloc[i, j])
        
        fig_hist, ax_hist = plt.subplots(figsize=(2.5, 2.5))
        ax_hist.hist(corr_values, bins=15, color='skyblue', edgecolor='black', alpha=0.7)
        ax_hist.axvline(x=0, color='red', linestyle='--', linewidth=1, label='Zero')
        ax_hist.set_xlabel('Correlation', fontsize=7)
        ax_hist.set_ylabel('Frequency', fontsize=7)
        ax_hist.set_title('Correlation Distribution', fontsize=8)
        ax_hist.legend(fontsize=6)
        ax_hist.grid(True, alpha=0.3)
        ax_hist.tick_params(axis='both', which='major', labelsize=6)
        st.pyplot(fig_hist)
    
    with col3:
        st.subheader("Average Correlation")
        
        avg_correlations = []
        for stock in corr_matrix.columns:
            other_correlations = [corr_matrix.loc[stock, other] for other in corr_matrix.columns if other != stock]
            avg_correlation = np.mean(other_correlations)
            avg_correlations.append({
                'Stock': stock,
                'Average Correlation': avg_correlation
            })
        
        avg_corr_df = pd.DataFrame(avg_correlations)
        
        fig_bar, ax_bar = plt.subplots(figsize=(2.5, 2.5))
        bars = ax_bar.bar(avg_corr_df['Stock'], avg_corr_df['Average Correlation'], 
                         color=['red' if x > 0.3 else 'blue' if x < -0.1 else 'gray' for x in avg_corr_df['Average Correlation']],
                         width=0.6)
        
        ax_bar.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax_bar.set_xlabel('Stocks', fontsize=7)
        ax_bar.set_ylabel('Avg Correlation', fontsize=7)
        ax_bar.set_title('Average Correlation', fontsize=8)
        
        for bar in bars:
            height = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom' if height >= 0 else 'top',
                       fontsize=5)
        
        plt.xticks(rotation=45, fontsize=6)
        plt.yticks(fontsize=6)
        plt.tight_layout()
        st.pyplot(fig_bar)
    
    st.subheader("Detailed Correlation Matrix")
    
    def color_correlation(val):
        color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'lightgreen' if val < -0.3 else 'white'
        return f'background-color: {color}'
    
    styled_corr = corr_matrix.style.format("{:.4f}").applymap(color_correlation)
    st.dataframe(styled_corr, use_container_width=True)
    st.info("""
    **Correlation Coefficient Explanation**:
    - **1**: Perfect positive correlation
    - **-1**: Perfect negative correlation  
    - **0**: No correlation between stock movements
    """)
    
    return corr_matrix
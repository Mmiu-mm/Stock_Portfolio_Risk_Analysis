import streamlit as st

def render_sidebar():
    with st.sidebar:
        try:
            st.image(r"D:\final_project\logo\efrei.png", caption="EFREI", width=150, use_container_width=False)
        except Exception as e:
            st.error(f"Could not load EFREI Logo: {e}")
            st.markdown("**EFREI Logo**")
        
        st.write("")
            
        try:
            st.image(r"D:\final_project\logo\WUT.png", caption="WUT", width=150, use_container_width=False)
        except Exception as e:
            st.error(f"Could not load WUT Logo: {e}")
            st.markdown("**WUT Logo**")  
        st.markdown("---")
        st.title("Course: Data Visualization 2025-Portfolio Risk Analysis")    
        st.markdown("---")
        st.subheader("Student Info")
        
        st.write("**Supervisor:** Prof. Mano Mathew")
        st.write("**Email:** mano.mathew@efrei.fr")
        st.markdown("[Check out this LinkedIn](https://www.linkedin.com/in/manomathew/)", unsafe_allow_html=True)
        st.write("**Student Name:** Yalin Mo")
        st.write("**Email:** Yalin.Mo@efrei.net")
        st.markdown("[Check out this GitHub](https://github.com/Mmiu-mm/Stock_Portfolio_Risk_Analysis.git)", unsafe_allow_html=True)
    
        st.markdown("---")
        
        st.subheader("Analysis Modules")
        
        selected_module = st.selectbox(
            "Choose Analysis Module:",
            ["Project Background", "GARCH Model", "Technical Analysis", "Conclusions"],
            index=0
        )
        
    
    return selected_module
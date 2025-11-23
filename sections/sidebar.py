import streamlit as st

def render_sidebar():
    with st.sidebar:
        try:
            st.image(r"D:\final_project\logo\efrei.png", caption="EFREI", width=180, use_container_width=False)
        except Exception as e:
            st.error(f"Could not load EFREI Logo: {e}")
            st.markdown("**EFREI Logo**")
        
        st.write("")
            
        try:
            st.image(r"D:\final_project\logo\WUT.png", caption="WUT", width=180, use_container_width=False)
        except Exception as e:
            st.error(f"Could not load WUT Logo: {e}")
            st.markdown("**WUT Logo**")
        
        st.markdown("---")

        st.title("Portfolio Risk Analysis")
    
        st.markdown("---")
        st.subheader("Student Info")
        
        st.write("**Supervisor:** Mano Joseph Mathew")
        st.write("**Email:** mano.mathew@efrei.fr")

        st.write("**Student Name:** Yalin Mo")
        st.write("**Email:** Yalin.Mo@efrei.net")
       
        st.markdown("---")
        
        st.subheader("Analysis Modules")
        
        selected_module = st.selectbox(
            "Choose Analysis Module:",
            ["Project Background", "GARCH Model", "Technical Analysis", "Conclusions"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("https://github.com/Mmiu-mm/Stock_Portfolio_Risk_Analysis.git")
    
    return selected_module
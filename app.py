import streamlit as st
from PIL import Image
import os
from ai_engine import analyze_circuit_image

# Page Configuration
st.set_page_config(
    page_title="AI Electronics Lab Assistant",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AI-Powered Electronics Lab Assistant")
st.caption("Upload a photo of your breadboard, PCB, or circuit schematic for instant component identification, analysis, and debugging assistance.")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ App Control Panel")
    st.write("This tool uses the multimodal Gemini API to analyze circuit images.")
    
    # Let the user choose between uploading a file or testing with a sample image
    app_mode = st.radio("Choose Input Method:", ["Upload an Image", "Use a Sample Circuit"])

# Left and Right layout columns
col1, col2 = st.columns([1, 1.2], gap="large")

img_to_analyze = None

with col1:
    if app_mode == "Upload an Image":
        st.subheader("📸 Upload Circuit Image")
        uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            img_to_analyze = Image.open(uploaded_file)
            st.image(img_to_analyze, caption="Uploaded Circuit Preview", use_container_width=True)
            
    else:
        st.subheader("📁 Select a Sample Circuit")
        st.write("No components on hand? Test the AI assistant with these pre-loaded lab examples:")
        
        # Simple selection box for samples
        sample_choice = st.selectbox(
            "Select Sample Lab Exercise:",
            ["None", "Example 1: LED Blink Circuit", "Example 2: RC Low-Pass Filter"]
        )
        
        # Hardcoded web URLs of standard circuits so you don't have to manage local image files
        if sample_choice == "Example 1: LED Blink Circuit":
            # Direct link to a public breadboard image
            img_url = "https://upload.wikimedia.org/wikipedia/commons/c/c2/Breadboard_LED_Circuit.jpg"
            try:
                import requests
                from io import BytesIO
                response = requests.get(img_url)
                img_to_analyze = Image.open(BytesIO(response.content))
                st.image(img_to_analyze, caption="Sample: LED Circuit", use_container_width=True)
            except:
                st.error("Failed to load sample image online. Make sure you are connected to the internet.")
                
        elif sample_choice == "Example 2: RC Low-Pass Filter":
            img_url = "https://upload.wikimedia.org/wikipedia/commons/e/e0/RC_Divider.svg"
            try:
                import requests
                from io import BytesIO
                response = requests.get(img_url)
                img_to_analyze = Image.open(BytesIO(response.content))
                st.image(img_to_analyze, caption="Sample: RC Filter Schematic", use_container_width=True)
            except:
                st.error("Failed to load sample image online.")

with col2:
    st.subheader("📊 AI Analysis Results")
    
    if img_to_analyze is not None:
        if st.button("🚀 Analyze Circuit Structure", type="primary"):
            with st.spinner("Analyzing components and circuit theory... Please wait..."):
                try:
                    raw_analysis = analyze_circuit_image(img_to_analyze)
                    
                    # Split the sections cleanly based on our markdown headers
                    sections = raw_analysis.split("### ")
                    
                    comp_id = "Processing issue. Could not isolate section."
                    theory = "Processing issue. Could not isolate section."
                    mistakes = "Processing issue. Could not isolate section."
                    
                    for section in sections:
                        if "Component Identification" in section:
                            comp_id = section.replace("Component Identification", "")
                        elif "Circuit Analysis & Theory" in section:
                            theory = section.replace("Circuit Analysis & Theory", "")
                        elif "Common Mistakes & Troubleshooting" in section:
                            mistakes = section.replace("Common Mistakes & Troubleshooting", "")

                    tab1, tab2, tab3 = st.tabs([
                        "🔍 Detected Components", 
                        "⚡ Circuit Theory & Analysis", 
                        "⚠️ Troubleshooting & Mistakes"
                    ])
                    
                    with tab1:
                        st.markdown(comp_id)
                    with tab2:
                        st.markdown(theory)
                    with tab3:
                        st.markdown(mistakes)
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Please provide a circuit image using the left panel to trigger the AI analysis.")
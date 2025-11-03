import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from sticker_maker import StickerMaker

st.set_page_config(
    page_title="Smart Face Sticker Generator",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 3.5rem; color: #FF6B9D; text-align: center; margin-bottom: 1rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.2); font-weight: bold; }
    .sub-header { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin: 0.5rem 0; }
    .sticker-preview { border: 3px dashed #FF6B9D; border-radius: 15px; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎨 Smart Face Sticker Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your photos into professional stickers • Pure Image Processing • No AI Required</p>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Sticker Settings")
    style = st.selectbox("🎨 Sticker Style", ['normal', 'black and white'], index=0)
    st.markdown("---")
    st.subheader("🖼️ Border Settings")
    border_thickness = st.slider("Border Thickness", 5, 30, 15, 1)
    st.markdown("---")
    st.subheader("🔧 Advanced Settings")
    use_grabcut = st.checkbox("Use GrabCut Refinement", value=True)
    edge_sensitivity = st.slider("Edge Detection Sensitivity", 1, 10, 1, 1)
    low_threshold = 100 + (edge_sensitivity * 20)
    high_threshold = 200 + (edge_sensitivity * 20)
    st.markdown("---")
    st.info("### 💡 Tips: Use clear background photos; adjust sensitivity for better edges.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Your Photo")
    uploaded_file = st.file_uploader("Choose a photo", type=['jpg', 'jpeg', 'png', 'bmp'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with col1:
        st.image(image_rgb, caption="Original Photo", use_column_width=True)
    
    with st.spinner(f"🎨 Creating your {style} sticker..."):
        maker = StickerMaker(style=style)
        results = maker.process(
            image,
            border_thickness=border_thickness,
            use_grabcut=use_grabcut,
            low_threshold=low_threshold,
            high_threshold=high_threshold
        )
    
    with col2:
        st.subheader("✨ Your Sticker")
        sticker_rgb = cv2.cvtColor(results['sticker'], cv2.COLOR_BGR2RGB)
        st.markdown('<div class="sticker-preview">', unsafe_allow_html=True)
        st.image(sticker_rgb, caption=f"{style.replace(' and ', ' & ').title()} Sticker", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Sticker Statistics")
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown(f'<div class="metric-card"><h3>🎯 Coverage</h3><h2>{results["coverage"]}%</h2><p>of image area</p></div>', unsafe_allow_html=True)
    with metric_cols[1]:
        st.markdown(f'<div class="metric-card"><h3>🖼️ Style</h3><h2>{style.replace(" and ", " & ").title()}</h2><p>applied effect</p></div>', unsafe_allow_html=True)
    with metric_cols[2]:
        st.markdown(f'<div class="metric-card"><h3>📏 Border</h3><h2>{border_thickness}px</h2><p>Default color</p></div>', unsafe_allow_html=True)
    with metric_cols[3]:
        st.markdown('<div class="metric-card"><h3>📝 Text</h3><h2>No</h2><p>none</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔬 Processing Steps")
    tab1, tab2, tab3 = st.tabs(["📸 Edge Detection", "🎭 Mask Creation", "🎨 Final Comparison"])
    with tab1:
        step_cols = st.columns(2)
        with step_cols[0]:
            edges_rgb = cv2.cvtColor(results['edges'], cv2.COLOR_GRAY2RGB)
            st.image(edges_rgb, caption="1. Edge Detection (Canny)", use_column_width=True)
        with step_cols[1]:
            closed_rgb = cv2.cvtColor(results['closed_edges'], cv2.COLOR_GRAY2RGB)
            st.image(closed_rgb, caption="2. Closed Edges", use_column_width=True)
    with tab2:
        mask_cols = st.columns(2)
        with mask_cols[0]:
            mask_rgb = cv2.cvtColor(results['mask'], cv2.COLOR_GRAY2RGB)
            st.image(mask_rgb, caption="3. Person Mask", use_column_width=True)
        with mask_cols[1]:
            overlay = image_rgb.copy()
            mask_colored = np.zeros_like(overlay)
            mask_colored[results['mask'] > 0] = [0, 255, 0]
            overlay_result = cv2.addWeighted(overlay, 0.7, mask_colored, 0.3, 0)
            st.image(overlay_result, caption="4. Mask Overlay", use_column_width=True)
    with tab3:
        comp_cols = st.columns(2)
        with comp_cols[0]:
            st.image(image_rgb, caption="🔴 Original", use_column_width=True)
        with comp_cols[1]:
            st.image(sticker_rgb, caption="✅ Sticker", use_column_width=True)
    
    st.markdown("---")
    st.markdown("### 💾 Download Your Sticker")
    download_cols = st.columns(3)
    with download_cols[0]:
        sticker_pil = Image.fromarray(sticker_rgb)
        buf = io.BytesIO()
        sticker_pil.save(buf, format="PNG")
        st.download_button("📥 Download Sticker (PNG)", buf.getvalue(), "my_sticker.png", "image/png")
    with download_cols[1]:
        transparent_rgba = cv2.cvtColor(results['transparent'], cv2.COLOR_BGRA2RGBA)
        trans_pil = Image.fromarray(transparent_rgba)
        buf2 = io.BytesIO()
        trans_pil.save(buf2, format="PNG")
        st.download_button("📥 Download Transparent (PNG)", buf2.getvalue(), "my_sticker_transparent.png", "image/png")
    with download_cols[2]:
        mask_pil = Image.fromarray(results['mask'])
        buf3 = io.BytesIO()
        mask_pil.save(buf3, format="PNG")
        st.download_button("📥 Download Mask", buf3.getvalue(), "sticker_mask.png", "image/png")

else:
    with col2:
        st.info("👈 Please upload a photo to start creating your sticker!")
        st.markdown('<div class="sticker-preview"><h2 style="color: #666;">🎨</h2><p style="color: #999; font-size: 1.2rem;">Your amazing sticker will appear here!</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #666; padding: 2rem 0;"><h3 style="color: #FF6B9D;">🎨 Smart Face Sticker Generator</h3><p><strong>Pure Image Processing</strong> • No AI Required • Real-World Optimized 🚀</p><p style="font-size: 0.9rem; margin-top: 1rem;">Built with: Canny Edge Detection • Morphological Operations • GrabCut Segmentation • Contour Detection</p></div>', unsafe_allow_html=True)
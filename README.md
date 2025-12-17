# Smart Face Sticker Generator

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Abhinav7301/Smart_face_sticker_Generator.svg?style=social)](https://github.com/Abhinav7301/Smart_face_sticker_Generator)

## 🎨 Overview

Smart Face Sticker Generator is a sophisticated image processing application that transforms photographs into professional-quality stickers using pure computer vision techniques. Built with **pure image processing algorithms** (no AI required), this tool leverages advanced edge detection, morphological operations, and contour analysis to create stunning sticker outputs.

### Key Highlights
- **Zero AI Dependency**: Utilizes classical computer vision algorithms
- **Multiple Sticker Styles**: Normal and Black & White variants
- **Interactive Web UI**: User-friendly Streamlit interface
- **Advanced Customization**: Fine-grained control over processing parameters
- **Real-time Preview**: Instant visual feedback with detailed processing steps
- **Export Options**: Multiple output formats and quality options

---

## ✨ Features

### Core Features
- ✅ **Canny Edge Detection**: Advanced edge identification for precise sticker boundaries
- ✅ **Morphological Operations**: Erosion, dilation, and closing for boundary refinement
- ✅ **GrabCut Segmentation**: Optional advanced foreground-background separation
- ✅ **Contour Detection**: Intelligent contour analysis and processing
- ✅ **Multiple Export Formats**: PNG (standard and transparent), JPG
- ✅ **Real-time Statistics**: Coverage percentage and processing metrics

### User Interface Features
- 🎯 Interactive parameter adjustment
- 📊 Multi-tab processing visualization
- 🖼️ Side-by-side comparison views
- 📈 Detailed processing step breakdown
- 🎨 Professional UI styling with custom CSS
- 📥 Direct browser download functionality

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abhinav7301/Smart_face_sticker_Generator.git
   cd Smart_face_sticker_Generator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Basic Usage

1. **Upload Photo**: Click "Choose a photo" to select your image (JPG, PNG, BMP formats supported)
2. **Select Style**: Choose between "Normal" or "Black and White" sticker style
3. **Adjust Settings**:
   - **Border Thickness**: Customize the sticker border width (5-30px)
   - **GrabCut Refinement**: Toggle advanced segmentation for better accuracy
   - **Edge Sensitivity**: Fine-tune edge detection (1-10 scale)
4. **View Results**: See real-time sticker generation in the preview pane
5. **Download**: Export as standard PNG, transparent PNG, or mask file

### Advanced Settings

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Border Thickness | 5-30px | 15px | Thickness of the sticker border |
| Edge Sensitivity | 1-10 | 1 | Controls Canny edge detection thresholds |
| GrabCut Refinement | On/Off | On | Enables advanced foreground segmentation |

### Processing Tabs

- **📸 Edge Detection**: View edge detection and morphological closing results
- **🎭 Mask Creation**: See mask overlay and segmentation results
- **🎨 Final Comparison**: Side-by-side comparison of original vs. sticker

---

## 📁 Project Structure

```
Smart_face_sticker_Generator/
├── app.py                 # Main Streamlit application
├── sticker_maker.py       # Core sticker processing logic
├── image_utils.py         # Image processing utilities
├── update_docx.py         # Document generation utilities
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
└── assets/               # Sample images and outputs
    ├── Original_Image.webp
    ├── Edge_Detection.jpg
    ├── Final_Sticker.jpg
    └── ...
```

---

## 🛠️ Technical Details

### Dependencies

- **OpenCV (cv2)**: Computer vision algorithms
- **Streamlit**: Web application framework
- **NumPy**: Numerical computing
- **Pillow (PIL)**: Image manipulation
- **python-docx**: Document generation (optional)

### Processing Pipeline

```
Input Image
    ↓
[Color Space Conversion] BGR → RGB/Grayscale
    ↓
[Canny Edge Detection] Identify object boundaries
    ↓
[Morphological Closing] Fill small holes in edges
    ↓
[Contour Detection] Extract main foreground contour
    ↓
[GrabCut Refinement] Optional advanced segmentation
    ↓
[Mask Generation] Create binary mask from contours
    ↓
[Border Application] Add configurable border
    ↓
[Style Application] Apply normal or B&W effect
    ↓
Output Sticker
```

### Algorithm Details

**Canny Edge Detection**
- Multi-stage edge detection algorithm
- Configurable thresholds based on sensitivity slider
- Provides high-quality edge maps

**Morphological Operations**
- Closing operation: dilation followed by erosion
- Fills small holes in the detected edges
- Creates continuous object boundaries

**GrabCut Segmentation** (Optional)
- Iterative energy minimization algorithm
- Refines foreground-background separation
- Improves handling of complex backgrounds

---

## 🎓 Example Workflow

### Input
A portrait photo with clear subject and background

### Processing
1. Convert to grayscale and apply Canny edge detection
2. Apply morphological closing to refine edges
3. Detect and extract main contours
4. Generate mask from contours
5. Apply GrabCut for refinement (optional)
6. Apply border and styling

### Output
Professional sticker with clean edges, customizable border, and multiple export options

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add comments for complex algorithms
- Update documentation for new features

---

## 📋 Roadmap

- [ ] Batch processing for multiple images
- [ ] Advanced color correction and enhancement
- [ ] Custom shape templates for stickers
- [ ] API endpoint for integration
- [ ] Mobile app version
- [ ] Real-time video sticker generation

---

## ⚙️ Configuration

No additional configuration required. All settings are adjustable through the UI.

**Recommended System Requirements**
- CPU: 2+ GHz processor
- RAM: 4GB minimum (8GB recommended)
- Storage: 500MB for dependencies

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abhinav** - [@Abhinav7301](https://github.com/Abhinav7301)

---

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision tools
- Streamlit for making web UI development accessible
- All contributors and users who provide feedback

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/Abhinav7301/Smart_face_sticker_Generator/issues)
- Check [Discussions](https://github.com/Abhinav7301/Smart_face_sticker_Generator/discussions)

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star! ⭐

---

**Last Updated**: December 2025
**Version**: 1.0.0

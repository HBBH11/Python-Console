# Python-Console

# Python Console 🐍

A modern, web-based Python console built with Streamlit, specifically designed for data science and machine learning experimentation. This interactive console provides a safe environment for code execution with built-in support for popular data science libraries.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.0+-red.svg)

## ✨ Features

- 🚀 Interactive Python code execution
- 📊 Built-in support for data science libraries (NumPy, Pandas, Matplotlib, Seaborn)
- 🛡️ Secure code execution with safety checks
- 📝 Execution history tracking
- 🎨 Modern, responsive UI with custom styling
- 📈 Real-time visualization support
- 💾 Session state persistence
- ⚠️ Comprehensive error handling

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-ai-lab-console.git
cd data-ai-lab-console
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📦 Dependencies

Create a `requirements.txt` file with the following content:
```
streamlit>=1.0.0
matplotlib>=3.3.0
seaborn>=0.11.0
numpy>=1.19.0
pandas>=1.2.0
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run python_console.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Start coding! Enter your Python code in the text area and click "Execute Code" to run it.

## 💡 Supported Features

### Allowed Libraries
The console supports a wide range of data science and machine learning libraries:
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy
- Scikit-learn
- TensorFlow
- PyTorch
- And many more!

### Code Execution
- Safe execution environment
- Import validation
- State persistence between executions
- Real-time output display
- Interactive plotting support

### Security Features
- Restricted access to system functions
- Blocked unsafe operations (file operations, system commands)
- Import restrictions to allowed modules only
- Execution timeout protection

## 🎨 UI Features

- Modern, responsive design
- Syntax highlighting
- Clear error messages
- Execution history with expandable cells
- Plot visualization
- Success/error status indicators

## 🔍 Code Structure

```
Python-console/
├── python_console.py      # Main application file
├── requirements.txt       # Project dependencies
├── README.md             # This documentation
└── LICENSE              # License file
```

### Main Components

1. **Session State Management**
   - Execution history tracking
   - Variable state persistence
   - Figure management

2. **Code Execution Engine**
   - Safe execution environment
   - Output capture
   - Error handling
   - State management

3. **Security Layer**
   - Code validation
   - Import restrictions
   - Pattern matching for unsafe operations

4. **User Interface**
   - Custom styling
   - Interactive components
   - Responsive layout
   - History display

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 🐛 Bug Reports

If you find a bug, please create an issue with:
- Detailed description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)


## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by Jupyter notebooks and Google Colab
- Styling enhanced with custom CSS

## 📞 Contact

For questions or feedback, please:
- Create an issue in this repository
- Contact the maintainer at [your-email@example.com]

## 🚀 Future Improvements

- [ ] Add support for file upload
- [ ] Implement code sharing functionality
- [ ] Add more visualization libraries
- [ ] Create custom widget support
- [ ] Add code completion
- [ ] Implement workspace saving/loading
- [ ] Add collaborative features

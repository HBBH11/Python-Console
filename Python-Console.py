import streamlit as st
import sys
import io
import re
import uuid
from typing import List, Tuple, Dict
import traceback
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Initialize session state for execution history and variable storage
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []
if 'execution_state' not in st.session_state:
    st.session_state.execution_state = {}

# Configuration and allowed modules
ALLOWED_MODULES = [
    'math', 're', 'random', 'time', 'datetime', 'collections',
    'itertools', 'functools', 'statistics', 'typing', 'operator',
    'json', 'csv', 'numpy', 'pandas', 'scipy', 'sklearn',
    'matplotlib', 'matplotlib.pyplot', 'seaborn', 'plotly',
    'torch', 'tensorflow', 'keras', 'sympy', 'networkx', 'pillow',
    'requests', 'beautifulsoup4', 'nltk', 'pytz', 'emoji', 'pytest'
]

# Streamlit page configuration with enhanced theme
st.set_page_config(
    page_title="Python Console",
    page_icon="🐍",
    layout="wide"
)

# Custom CSS style with modern and elegant design
st.markdown("""
    <style>
    /* Global theme */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Main title */
    .title {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
        background: linear-gradient(45deg, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
    }

    /* Code area */
    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border: 2px solid #3498db;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Fira Code', monospace;
    }

    /* Execute button */
    .stButton > button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #27ae60;
        transform: scale(1.05);
    }

    /* History cells */
    .stExpander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        padding: 10px;
    }

    /* Code and output */
    .stCodeBlock {
        background-color: #f1f3f5;
        border-left: 4px solid #3498db;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Fira Code', monospace;
    }

    /* Success and error messages */
    .stSuccess, .stError {
        border-radius: 8px;
        padding: 10px;
    }

    .stSuccess {
        background-color: rgba(46, 204, 113, 0.1);
        border-left: 4px solid #2ecc71;
    }

    .stError {
        background-color: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)


def execute_code_safely(code: str, execution_state: dict) -> Tuple[bool, str, List[plt.Figure]]:
    """
    Execute Python code safely with state persistence and custom error messages
    """
    old_stdin, old_stdout, old_stderr = sys.stdin, sys.stdout, sys.stderr
    stdin_capture = io.StringIO()
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    sys.stdin, sys.stdout, sys.stderr = stdin_capture, stdout_capture, stderr_capture

    captured_figures = []

    try:
        # Create execution environment with existing state
        exec_globals = {
            '__builtins__': __builtins__,
            'plt': plt,
            'sns': sns,
            'np': np,
            'pd': pd,
        }

        # Add existing state
        exec_globals.update(execution_state)

        # Handle imports and code execution
        import_statements = []
        code_without_imports = []

        for line in code.split('\n'):
            if line.strip().startswith(('import ', 'from ')):
                import_statements.append(line)
            else:
                code_without_imports.append(line)

        # Execute imports
        for import_stmt in import_statements:
            exec(import_stmt, exec_globals)

        # Execute main code
        exec('\n'.join(code_without_imports), exec_globals)

        # Update execution state with new variables
        execution_state.update({
            k: v for k, v in exec_globals.items()
            if not k.startswith('__') and k not in ('plt', 'sns', 'np', 'pd')
        })

        # Capture figures
        captured_figures = [plt.figure(num) for num in plt.get_fignums()]

        output = stdout_capture.getvalue()
        return True, output.strip() if output.strip() else "Code executed successfully.", captured_figures

    except Exception as e:
        # Customize error message
        if isinstance(e, NameError):
            # For undefined variable errors
            return False, f"'{e.name}' is not defined", []
        elif isinstance(e, TypeError):
            # For type errors
            return False, str(e).split(':')[-1].strip(), []
        elif isinstance(e, SyntaxError):
            # For syntax errors
            return False, f"Syntax error: {e.msg}", []
        elif isinstance(e, ImportError):
            # For import errors
            return False, f"Import error: {str(e)}", []
        else:
            # For any other type of error
            return False, str(e), []

    finally:
        sys.stdin, sys.stdout, sys.stderr = old_stdin, old_stdout, old_stderr
        stdin_capture.close()
        stdout_capture.close()
        stderr_capture.close()


def is_code_safe(code: str) -> Tuple[bool, str]:
    """
    Check if the code is safe to execute
    """
    unsafe_patterns = [r'open\(', r'exec\(', r'eval\(']

    for pattern in unsafe_patterns:
        if re.search(pattern, code):
            return False, "Unsafe code pattern detected"

    imports = re.findall(r'^import\s+(\w+)', code, re.MULTILINE)
    imports_from = re.findall(r'^from\s+(\w+)', code, re.MULTILINE)

    unauthorized_imports = [
        imp for imp in set(imports + imports_from)
        if not any(imp.startswith(allowed) for allowed in ALLOWED_MODULES)
    ]

    if unauthorized_imports:
        return False, f"Unauthorized imports: {', '.join(unauthorized_imports)}"

    return True, "Code appears safe"


def main():
    st.markdown('<h1 class="title">🐍 Python Console</h1>', unsafe_allow_html=True)

    # Create two columns for layout
    col1, col2 = st.columns([3, 1])

    with col1:
        # Code input area with informative placeholder
        new_code = st.text_area(
            "New Code Cell:",
            height=300,
        )

    # Execute button with icon
    if st.button("🚀 Execute Code"):
        if new_code.strip():
            # Check code safety
            is_safe, safety_message = is_code_safe(new_code)

            if not is_safe:
                st.error(f"⚠️ {safety_message}")
            else:
                # Execute code and store in history
                success, output, figures = execute_code_safely(
                    new_code,
                    st.session_state.execution_state
                )

                st.session_state.execution_history.append({
                    'code': new_code,
                    'output': output,
                    'figures': figures,
                    'success': success
                })

    # Display execution history in reverse order
    if st.session_state.execution_history:
        st.subheader("📜 Execution History")
        for cell in reversed(st.session_state.execution_history):
            with st.expander("Code Cell", expanded=True):
                st.code(cell['code'], language='python')
                if cell['success']:
                    st.success("✅ Output:")
                    if cell['output']:
                        st.code(cell['output'])
                    for fig in cell['figures']:
                        st.pyplot(fig)
                else:
                    st.error("❌ Error:")
                    st.error(cell['output'])
    else:
        st.info("🔍 No execution history. Start coding!")


if __name__ == "__main__":
    main()
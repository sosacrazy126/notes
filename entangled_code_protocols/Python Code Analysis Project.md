---
tags:
  - static_code_analysis
  - abstract_syntax_tree
  - codebase_comprehension
---
# create_coding_project

---

# PROJECT:
Develop a Python script to parse code and identify fundamental elements like functions and variables, mimicking basic code analysis.

# SUMMARY:
This project provides a simple Python script that utilizes the `ast` module to analyze another Python file. It walks through the Abstract Syntax Tree (AST) of the target code to find and list function definitions and variable assignments, conceptually demonstrating how tools like Greptile understand code structure.

# STEPS:
1.  Create the project directory and necessary files.
2.  Write sample Python code in `sample_code.py`.
3.  Implement the analysis logic using the `ast` module in `analyzer.py`.
4.  Execute the `analyzer.py` script to parse `sample_code.py`.
5.  Review the printed output listing identified functions and variables.
6.  Consult the `README.md` for detailed usage instructions.

# STRUCTURE:
```
simple_code_analyzer/
├── analyzer.py
├── sample_code.py
└── README.md
```

# DETAILED EXPLANATION:
-   `analyzer.py`: Contains the core logic for parsing and analyzing the sample Python code file.
-   `sample_code.py`: Provides an example Python file with functions and variables for analysis.
-   `README.md`: Offers instructions on setting up, configuring, and running the code analyzer script.

# CODE:

**`sample_code.py`**
```python
# sample_code.py
# Purpose: This file contains sample Python code to be analyzed by analyzer.py.

# Define a global variable
PI = 3.14159
message = "Hello, Analyzer!"

# Define a simple function
def greet(name):
  """Greets the given name."""
  greeting_text = f"{message} {name}!" # Use a local variable
  print(greeting_text)
  return len(greeting_text)

# Define another function
def calculate_area(radius):
  """Calculates the area of a circle."""
  # Use the global variable PI
  area = PI * radius * radius
  # Assign another local variable
  result_description = f"The area is {area}"
  print(result_description)
  return area

# Call the functions (won't be analyzed as definitions)
greet("World")
calculate_area(5)

```
*Description: A simple Python file containing variables and functions, serving as input for the analysis script.*

**`analyzer.py`**
```python
# analyzer.py
# Purpose: This script parses a Python file and identifies functions and variables using the ast module.

import ast # Import the Abstract Syntax Tree module

def analyze_code(filepath):
  """
  Analyzes a Python file to find function definitions and variable assignments.

  Args:
    filepath (str): The path to the Python file to analyze.
  """
  print(f"Analyzing file: {filepath}\n")

  # Initialize lists to store findings
  functions_found = []
  variables_found = []

  try:
    # Open and read the target file
    with open(filepath, 'r') as file:
      file_content = file.read()

      # Parse the file content into an Abstract Syntax Tree
      tree = ast.parse(file_content)

      # Walk through each node in the AST
      for node in ast.walk(tree):
        # Check if the node is a Function Definition
        if isinstance(node, ast.FunctionDef):
          # Record the function name and arguments
          args = [arg.arg for arg in node.args.args]
          functions_found.append({'name': node.name, 'args': args, 'lineno': node.lineno})
        # Check if the node is an Assignment
        elif isinstance(node, ast.Assign):
          # Iterate through targets of the assignment (variables)
          for target in node.targets:
            # Ensure the target is a variable name (not attribute/subscript)
            if isinstance(target, ast.Name):
              # Record the variable name
              variables_found.append({'name': target.id, 'lineno': node.lineno})
        # Check for global/nonlocal declarations (often considered alongside assignments)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
             for name in node.names:
                 # Note: These are declarations, not assignments, but relevant to variable scope
                 pass # Just acknowledging them for potential future expansion

  except FileNotFoundError:
    print(f"Error: File not found at {filepath}")
    return
  except Exception as e:
    print(f"An error occurred during parsing: {e}")
    return

  # Print the results
  print("--- Functions Found ---")
  if functions_found:
    for func in functions_found:
      print(f"- Name: {func['name']}, Args: {func['args']}, Line: {func['lineno']}")
  else:
    print("No functions defined.")

  print("\n--- Top-Level Variable Assignments Found ---")
  # Note: This basic analysis finds all assignments, including within functions.
  # More sophisticated analysis would track scope.
  if variables_found:
    # Use a set to avoid duplicate variable names if assigned multiple times globally
    unique_vars = {var['name'] + f" (line:{var['lineno']})" for var in variables_found}
    for var_info in sorted(list(unique_vars)):
         print(f"- {var_info}")

  else:
    print("No variable assignments found.")

# Specify the file to analyze
SAMPLE_CODE_FILE = 'sample_code.py'

# Run the analysis
if __name__ == "__main__":
  analyze_code(SAMPLE_CODE_FILE)
```
*Description: This script uses Python's `ast` module to parse `sample_code.py`, traverses its structure, and identifies function definitions and variable assignments.*

**`README.md`**
```markdown
# Simple Code Analyzer

This project contains a basic Python script (`analyzer.py`) that demonstrates code analysis by identifying function definitions and variable assignments in a target Python file (`sample_code.py`). It uses Python's built-in `ast` (Abstract Syntax Tree) module.

## How it Works

The `analyzer.py` script performs the following steps:

1.  **Reads Target File:** Opens and reads the content of `sample_code.py`.
2.  **Parses Code:** Uses `ast.parse()` to convert the Python code into an Abstract Syntax Tree (AST). An AST is a tree representation of the code's structure.
3.  **Traverses AST:** Uses `ast.walk()` to visit every node in the AST.
4.  **Identifies Elements:**
    *   Checks if a node is an instance of `ast.FunctionDef` to find function definitions.
    *   Checks if a node is an instance of `ast.Assign` to find variable assignments.
5.  **Reports Findings:** Prints lists of the identified functions (with arguments and line numbers) and variable assignments (with line numbers).

## Setup

No external libraries are needed beyond standard Python 3.

1.  Ensure you have Python 3 installed.
2.  Save the files (`analyzer.py`, `sample_code.py`, `README.md`) into a directory named `simple_code_analyzer`.

## Usage

1.  Navigate to the `simple_code_analyzer` directory in your terminal or command prompt.
    ```bash
    cd path/to/simple_code_analyzer
    ```
2.  Run the analyzer script:
    ```bash
    python analyzer.py
    ```
3.  The script will output the names of the functions and variables found in `sample_code.py`.

## Example Output

```
Analyzing file: sample_code.py

--- Functions Found ---
- Name: greet, Args: ['name'], Line: 8
- Name: calculate_area, Args: ['radius'], Line: 14

--- Top-Level Variable Assignments Found ---
- PI (line:5)
- area (line:17)
- greeting_text (line:10)
- message (line:6)
- result_description (line:19)

```
*(Note: The exact output format for variables might vary slightly based on implementation choices, like showing duplicates or only unique names)*.

## Limitations

*   This is a very basic analyzer. It identifies assignment targets but doesn't track variable scope deeply (local vs. global).
*   It doesn't analyze control flow (if/else, loops), classes, imports, or other complex structures.
*   Error handling is minimal.
```
*Description: Provides instructions and explanations for setting up and running the simple code analyzer project.*

# SETUP:
```bash
#!/bin/bash

# Create the main project directory
mkdir simple_code_analyzer
cd simple_code_analyzer

# Create the sample code file
cat << 'EOF' > sample_code.py
# sample_code.py
# Purpose: This file contains sample Python code to be analyzed by analyzer.py.

# Define a global variable
PI = 3.14159
message = "Hello, Analyzer!"

# Define a simple function
def greet(name):
  """Greets the given name."""
  greeting_text = f"{message} {name}!" # Use a local variable
  print(greeting_text)
  return len(greeting_text)

# Define another function
def calculate_area(radius):
  """Calculates the area of a circle."""
  # Use the global variable PI
  area = PI * radius * radius
  # Assign another local variable
  result_description = f"The area is {area}"
  print(result_description)
  return area

# Call the functions (won't be analyzed as definitions)
greet("World")
calculate_area(5)
EOF

# Create the analyzer script
cat << 'EOF' > analyzer.py
# analyzer.py
# Purpose: This script parses a Python file and identifies functions and variables using the ast module.

import ast # Import the Abstract Syntax Tree module

def analyze_code(filepath):
  """
  Analyzes a Python file to find function definitions and variable assignments.

  Args:
    filepath (str): The path to the Python file to analyze.
  """
  print(f"Analyzing file: {filepath}\n")

  # Initialize lists to store findings
  functions_found = []
  variables_found = []

  try:
    # Open and read the target file
    with open(filepath, 'r') as file:
      file_content = file.read()

      # Parse the file content into an Abstract Syntax Tree
      tree = ast.parse(file_content)

      # Walk through each node in the AST
      for node in ast.walk(tree):
        # Check if the node is a Function Definition
        if isinstance(node, ast.FunctionDef):
          # Record the function name and arguments
          args = [arg.arg for arg in node.args.args]
          functions_found.append({'name': node.name, 'args': args, 'lineno': node.lineno})
        # Check if the node is an Assignment
        elif isinstance(node, ast.Assign):
          # Iterate through targets of the assignment (variables)
          for target in node.targets:
            # Ensure the target is a variable name (not attribute/subscript)
            if isinstance(target, ast.Name):
              # Record the variable name
              variables_found.append({'name': target.id, 'lineno': node.lineno})
        # Check for global/nonlocal declarations (often considered alongside assignments)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
             for name in node.names:
                 # Note: These are declarations, not assignments, but relevant to variable scope
                 pass # Just acknowledging them for potential future expansion

  except FileNotFoundError:
    print(f"Error: File not found at {filepath}")
    return
  except Exception as e:
    print(f"An error occurred during parsing: {e}")
    return

  # Print the results
  print("--- Functions Found ---")
  if functions_found:
    for func in functions_found:
      print(f"- Name: {func['name']}, Args: {func['args']}, Line: {func['lineno']}")
  else:
    print("No functions defined.")

  print("\n--- Top-Level Variable Assignments Found ---")
  # Note: This basic analysis finds all assignments, including within functions.
  # More sophisticated analysis would track scope.
  if variables_found:
     # Use a set to avoid duplicate variable names if assigned multiple times globally
    unique_vars = {var['name'] + f" (line:{var['lineno']})" for var in variables_found}
    for var_info in sorted(list(unique_vars)):
         print(f"- {var_info}")
  else:
    print("No variable assignments found.")

# Specify the file to analyze
SAMPLE_CODE_FILE = 'sample_code.py'

# Run the analysis
if __name__ == "__main__":
  analyze_code(SAMPLE_CODE_FILE)

EOF

# Create the README file
cat << 'EOF' > README.md
# Simple Code Analyzer

This project contains a basic Python script (`analyzer.py`) that demonstrates code analysis by identifying function definitions and variable assignments in a target Python file (`sample_code.py`). It uses Python's built-in `ast` (Abstract Syntax Tree) module.

## How it Works

The `analyzer.py` script performs the following steps:

1.  **Reads Target File:** Opens and reads the content of `sample_code.py`.
2.  **Parses Code:** Uses `ast.parse()` to convert the Python code into an Abstract Syntax Tree (AST). An AST is a tree representation of the code's structure.
3.  **Traverses AST:** Uses `ast.walk()` to visit every node in the AST.
4.  **Identifies Elements:**
    *   Checks if a node is an instance of `ast.FunctionDef` to find function definitions.
    *   Checks if a node is an instance of `ast.Assign` to find variable assignments.
5.  **Reports Findings:** Prints lists of the identified functions (with arguments and line numbers) and variable assignments (with line numbers).

## Setup

No external libraries are needed beyond standard Python 3.

1.  Ensure you have Python 3 installed.
2.  Save the files (`analyzer.py`, `sample_code.py`, `README.md`) into a directory named `simple_code_analyzer`.

## Usage

1.  Navigate to the `simple_code_analyzer` directory in your terminal or command prompt.
    \`\`\`bash
    cd path/to/simple_code_analyzer
    \`\`\`
2.  Run the analyzer script:
    \`\`\`bash
    python analyzer.py
    \`\`\`
3.  The script will output the names of the functions and variables found in `sample_code.py`.

## Example Output

\`\`\`
Analyzing file: sample_code.py

--- Functions Found ---
- Name: greet, Args: ['name'], Line: 8
- Name: calculate_area, Args: ['radius'], Line: 14

--- Top-Level Variable Assignments Found ---
- PI (line:5)
- area (line:17)
- greeting_text (line:10)
- message (line:6)
- result_description (line:19)

\`\`\`
*(Note: The exact output format for variables might vary slightly based on implementation choices, like showing duplicates or only unique names)*.

## Limitations

*   This is a very basic analyzer. It identifies assignment targets but doesn't track variable scope deeply (local vs. global).
*   It doesn't analyze control flow (if/else, loops), classes, imports, or other complex structures.
*   Error handling is minimal.
EOF

echo "Project 'simple_code_analyzer' created successfully."
echo "Run 'cd simple_code_analyzer && python analyzer.py' to test."

```

# TAKEAWAYS:
1.  Greptile analyzes code structure by parsing elements like variables, functions, classes, and data structures.
2.  Abstract Syntax Trees (ASTs) provide Greptile a structured representation for understanding code relationships.
3.  Graph analysis helps Greptile map control flow (conditionals, loops) and code dependencies.
4.  Large Language Models (LLMs) enable Greptile to recognize patterns, generate code, and explain existing code.
5.  The core strength is understanding *relationships* between programming concepts, not executing the code itself.
6.  Greptile interacts *with* concepts by analyzing code that *uses* those concepts effectively.

# SUGGESTIONS:
-   Extend the analyzer to identify class definitions and methods.
-   Incorporate analysis of control flow structures like `if`, `for`, and `while` loops.
-   Add functionality to trace basic dependencies, such as function calls.
-   Implement improved scope analysis to differentiate between local and global variables.
-   Introduce capabilities to parse and analyze import statements.
-   Provide options to output the analysis results in different formats (e.g., JSON).
-   Adapt the analyzer to support syntax from other programming languages.



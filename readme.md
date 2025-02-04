# LTL Action Sequence Optimizer

This project combines LTL (Linear Temporal Logic) formula validation with action sequence optimization. It translates natural language instructions into LTL formulas, validates them, and uses the resulting atomic propositions to optimize action sequences.

## Features

- Translation of natural language instructions to LTL formulas
- LTL formula validation with atomic propositions extraction
- Context-aware sequence optimization
- Detailed analysis and logging of optimization steps
- Rich console output for analysis results

## Project Structure

```
project/
│
├── src/
│   ├── __init__.py
│   ├── models.py                 # Data models and types
│   ├── ltl/                      # LTL translation components
│   │   ├── __init__.py
│   │   └── translator.py
│   ├── optimization/             # Sequence optimization
│   │   ├── __init__.py
│   │   └── context_window.py
│   ├── pipeline/                 # Main processing pipeline
│   │   ├── __init__.py
│   │   └── action_processor.py
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── logging.py
│
├── tests/                        # Test directory
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [project-directory]
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
# Create .env file
ANTHROPIC_API_KEY=your-api-key
```

## Usage Example

```python
from src.pipeline.action_processor import ActionProcessor
from src.utils.logging import print_sequence_comparison

# Initialize the processor
processor = ActionProcessor(api_key='your-api-key')

# Define task and instruction
task = "Attach the thermometer to the window"
instruction = "Walk to the table, Grab the thermometer from the table, Walk to the window"

# Process the instruction
result = processor.process_instruction(instruction, task)

if result.success:
    print("\nProcessing successful!")
    original_sequence = result.data["original_sequence"]
    optimized_sequence = result.data["optimization_steps"]
    print_sequence_comparison(original_sequence, optimized_sequence)
else:
    print("\nProcessing failed:", result.error)
```

## Pipeline Flow

1. **LTL Translation**:
   - Natural language instruction is translated to LTL formula
   - Formula is validated and atomic propositions are extracted

2. **Sequence Optimization**:
   - Original sequence is analyzed using context windows
   - Atomic propositions guide the optimization process
   - Each action is evaluated for necessity and position

3. **Results Processing**:
   - Optimization steps are logged
   - Detailed analysis is saved
   - Comparison between original and optimized sequences

## Development

- Run tests:
```bash
pytest
```

- Format code:
```bash
black .
```

- Check types:
```bash
mypy .
```

- Sort imports:
```bash
isort .
```

## Notes

- Ensure your Anthropic API key has sufficient permissions
- The LTL validator requires internet connection
- Optimization results are saved in timestamped directories
- Rich console output provides detailed analysis visualization


## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
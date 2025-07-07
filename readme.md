<div align="center">

# VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots
A novel framework that combines Large Language Models with Linear Temporal Logic for systematic pre-execution verification of robotic task plans. 🤖

> [Danil S. Grigorev](https://github.com/)<sup>1,2</sup>, [Alexey K. Kovalev](https://github.com/)<sup>1,3</sup>, [Aleksandr I. Panov](https://github.com/)<sup>1,3</sup>
> 
> MIPT<sup>1</sup>, Pyatigorsk State University<sup>2</sup>, AIRI<sup>3</sup>

[\[📄Paper\]](https://arxiv.org/)  [\[🔥Project Page\]](https://verifyllm.github.io/) [\[🚀 Quick Start\]](#-quick-start) [\[✅ Performance\]](#-performance)

[\[🔧Installation\]](#-installation) [\[🧪 Experiments\]](#-experiments) [\[📊 Datasets\]](#-datasets-coming-soon)

</div>

## 📋 Abstract

Modern robotic planning systems generate action sequences that appear correct at first glance but contain hidden errors that only become evident during execution. To address this challenge, we propose **VerifyLLM** — a framework that combines Large Language Models (LLMs) with Linear Temporal Logic (LTL) for systematic pre-execution verification of robotic task plans.

Our approach consists of two key steps: (i) **Translation Module** that converts natural language instructions into LTL formulas, and (ii) **Verification Module** that analyzes action sequences using LLM reasoning enhanced by formal constraints. VerifyLLM identifies and corrects three critical types of plan inconsistencies: position errors, missing prerequisites, and redundant actions.

We evaluate VerifyLLM on specialized datasets with LTL annotations, achieving **40% reduction in order errors** and **2.6x better similarity** to ground truth plans compared to baseline methods.

## 🎯 Key Features

- **🔄 Two-Stage Architecture**: LTL Translation → LLM Verification for comprehensive plan analysis
- **🎯 Three Error Types**: Identifies position errors, missing prerequisites, and redundant actions
- **📝 Formal Constraints**: Uses Linear Temporal Logic for temporal dependency modeling
- **🔍 Sliding Window Analysis**: Optimal context window of 5 actions for efficient processing
- **🏠 Household Domain**: Specialized datasets for everyday robotic tasks
- **📈 Significant Improvements**: 40% reduction in ordering errors over baselines

## 🏆 Performance

| Method | LCS Similarity | Missing Actions | Extra Actions | Order Errors |
|--------|---------------|-----------------|---------------|--------------|
| Baseline (Llama-3.2-1B) | 0.0717 | 10.28 | 9.14 | 16.48 |
| CoT Optimizer | 0.0705 | 10.38 | 9.35 | 16.80 |
| VerifyLLM (Llama) | 0.0982 | 11.18 | 9.13 | 15.12 |
| **VerifyLLM (Claude)** | **0.183** | **10.17** | **8.32** | **9.47** |

### Key Improvements
- **40%** reduction in order errors compared to best baseline
- **2.6x** better LCS similarity to ground truth
- **Consistent improvements** across all error types

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key or Anthropic API key
- PyTorch 1.7.1+

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/verifyllm
cd verifyllm
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Create .env file
ANTHROPIC_API_KEY=your-api-key
# OR
OPENAI_API_KEY=your-api-key
```

### Basic Usage

```python
from src.pipeline.action_processor import ActionProcessor
from src.utils.logging import print_sequence_comparison

# Initialize the processor
processor = ActionProcessor(api_key='your-api-key')

# Define task and original plan
task = "Give milk to cat"
original_plan = [
    "Walk to home office",
    "Walk to bedroom", 
    "Walk to bedroom",
    "Walk to home office"
]

# Process and verify the plan
result = processor.verify_plan(original_plan, task)

if result.success:
    print("✅ Verification successful!")
    print(f"Original: {len(original_plan)} actions")
    print(f"Optimized: {len(result.optimized_plan)} actions")
    print_sequence_comparison(original_plan, result.optimized_plan)
else:
    print("❌ Verification failed:", result.error)
```

## 📁 Project Structure

```
verifyllm/
├── src/
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
├── datasets/                     # Specialized datasets
│   ├── alfred_ltl/              # ALFRED-LTL dataset
│   └── virtualhome_ltl/         # VirtualHome-LTL dataset
├── experiments/                  # Experimental scripts
├── tests/                       # Unit tests
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Installation

### Option 1: pip install (Recommended)
```bash
pip install verifyllm
```

### Option 2: From source
```bash
git clone https://github.com/your-username/verifyllm.git
cd verifyllm
pip install -e .
```

### Dependencies
- `anthropic>=0.18.0` or `openai>=1.0.0`
- `torch>=1.7.1`
- `spot>=3.2.0` (for LTL validation)
- `rich>=13.0.0` (for console output)

## 🧪 Experiments

### Running Evaluations

**Basic evaluation on VirtualHome dataset**:
```bash
python experiments/evaluate_virtualhome.py \
    --model claude-3-sonnet \
    --dataset datasets/virtualhome_ltl \
    --output results/virtualhome_claude.json
```

**Ablation studies**:
```bash
# Without LTL translation
python experiments/ablation.py --no-ltl

# Without LLM verification  
python experiments/ablation.py --no-llm

# Different window sizes
python experiments/window_size.py --sizes 3,5,7,9
```

**Custom dataset evaluation**:
```bash
python experiments/evaluate_custom.py \
    --input your_dataset.json \
    --task_field "instruction" \
    --plan_field "actions"
```

## 📊 Datasets (Coming Soon)

### ALFRED-LTL
- **Source**: Derived from ALFRED dataset
- **Tasks**: Household instruction following
- **Size**: 200 annotated task plans
- **LTL Annotations**: Temporal constraints and dependencies

### VirtualHome-LTL  
- **Source**: Adapted from VirtualHome dataset
- **Tasks**: Human-like daily activities
- **Size**: 200 action sequences
- **LTL Annotations**: Common-sense temporal relationships

### Dataset Format
```json
{
  "task_id": "make_tea_001",
  "instruction": "Make a cup of tea",
  "original_plan": ["heat water", "prepare cup", "pour tea", "add sugar"],
  "ltl_formula": "F(heat_water) ∧ F(prepare_cup) ∧ F(pour_tea)",
  "issues": ["missing_prerequisite", "position_error"],
  "corrected_plan": ["heat water", "prepare cup", "add tea bag", "pour hot water", "add sugar"]
}
```

## ⚙️ Configuration

### Window Size Optimization
```python
# Optimal window size (empirically determined)
WINDOW_SIZE = 5  # actions

# For different complexity levels:
# Simple tasks: 3
# Medium tasks: 5 (recommended)
# Complex tasks: 7
```

### Model Selection
```python
# Supported models
MODELS = {
    "claude-3-sonnet": "anthropic",
    "claude-3-opus": "anthropic", 
    "gpt-4": "openai",
    "gpt-4-turbo": "openai"
}
```

## 🔍 Algorithm Details

### Translation Module
1. **Input**: Natural language task description
2. **Process**: Few-shot prompting with LTL examples
3. **Validation**: Syntax checking using Spot library
4. **Output**: Formal LTL formula with atomic propositions

### Verification Module
1. **Input**: Action sequence + LTL formula
2. **Process**: Sliding window analysis with LLM reasoning
3. **Detection**: Three error types identification
4. **Correction**: Reordering, insertion, removal operations

## 📈 Results Analysis

### Error Type Distribution
```
Position Errors:    45% of total issues
Missing Prerequisites: 35% of total issues  
Redundant Actions:   20% of total issues
```

### Performance by Task Complexity
- **Simple (≤5 actions)**: 85% accuracy
- **Medium (6-10 actions)**: 72% accuracy  
- **Complex (>10 actions)**: 61% accuracy

## 🛠️ Advanced Usage

### Custom LTL Templates
```python
# Define custom LTL patterns
custom_templates = {
    "sequential": "F({action1}) ∧ F({action2}) ∧ ({action1} U {action2})",
    "conditional": "G({condition} → F({action}))",
    "eventually": "F({action})"
}

processor = ActionProcessor(ltl_templates=custom_templates)
```

### Batch Processing
```python
# Process multiple plans
plans = [plan1, plan2, plan3]
results = processor.verify_batch(plans, task_descriptions)

# Generate report
processor.generate_report(results, output_file="batch_results.html")
```

## 🧪 Testing

Run the test suite:
```bash
# All tests
python -m pytest tests/

# Specific components
python -m pytest tests/test_ltl_translation.py
python -m pytest tests/test_verification.py
python -m pytest tests/test_integration.py

# With coverage
python -m pytest tests/ --cov=src/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 src/ tests/
black src/ tests/
```

## 📄 Citation

```bibtex
@article{grigorev2024verifyllm,
  title={VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots},
  author={Grigorev, Danil S. and Kovalev, Alexey K. and Panov, Aleksandr I.},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2024}
}
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built upon the foundations of classical planning and modern LLM research
- Inspired by the need for reliable robotic task execution
- Special thanks to the ALFRED and VirtualHome dataset creators

---

<div align="center">

**[🔝 Back to Top](#verifyllm-llm-based-pre-execution-task-plan-verification-for-robots)**

Made with ❤️ by the VerifyLLM team

</div>

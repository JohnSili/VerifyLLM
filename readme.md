<div align="center">

# VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots
A novel framework that combines Large Language Models with Linear Temporal Logic for systematic pre-execution verification of robotic task plans. 🤖

> [Danil S. Grigorev](https://github.com/)<sup>1,2</sup>, [Alexey K. Kovalev](https://github.com/)<sup>1,3</sup>, [Aleksandr I. Panov](https://github.com/)<sup>1,3</sup>
> 
> MIPT<sup>1</sup>, Pyatigorsk State University<sup>2</sup>, AIRI<sup>3</sup>

[\[📄Paper\]](https://arxiv.org/)  [\[🔥Project Page\]](https://verifyllm.github.io/) [\[🚀 Quick Start\]](#-quick-start) [\[✅ Performance\]](#-performance)

[\[🔧Installation\]](#-installation) [\[📊 Datasets\]](#-datasets-coming-soon)

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
- **🏠 Household Domain**: Tested on household robotic tasks
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
- Anthropic API key (for Claude) or OpenAI API key
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
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Installation

### Dependencies
- `anthropic>=0.18.0` (for Claude)
- `torch>=1.7.1`
- `spot>=3.2.0` (for LTL validation)
- `rich>=13.0.0` (for console output)

## 📊 Datasets (Coming Soon)

### ALFRED-LTL
- **Source**: Derived from ALFRED dataset
- **Tasks**: Household instruction following
- **LTL Annotations**: Multiple temporal logic representations

### VirtualHome-LTL  
- **Source**: Adapted from VirtualHome dataset
- **Tasks**: Human-like daily activities
- **LTL Annotations**: Structured temporal constraints

### Dataset Format
```json
{
  "task_id": 111,
  "split": "train",
  "goal": "Cool a slice of bread and place it in the trash can.",
  "atomic_predicates": {
    "locations": ["at_table", "at_fridge", "at_trash_can"],
    "holding": ["have_knife", "have_bread_slice"],
    "object_states": ["bread_sliced", "knife_in_trash", "bread_cooled", "slice_in_trash"],
    "actions": ["turn_left", "step_forward", "pick_up_knife", "walk_around", "cut_bread", "place_knife", "pick_up_slice", "turn_around", "cool_bread", "remove", "walk_across", "place_slice"]
  },
  "sequential_ltl": "F(turn_left) ∧ F(step_forward) ∧ F(at_table) ∧ F(pick_up_knife) ∧ F(have_knife) ∧ F(walk_around) ∧ F(cut_bread) ∧ F(bread_sliced)...",
  "sequential_with_conditions": "F(turn_left ∧ X(step_forward)) ∧ F(step_forward ∧ X(at_table)) ∧ F(at_table ∧ X(pick_up_knife ∧ have_knife))...",
  "structured_ltl": "(¬slice_in_trash U (at_table ∧ have_knife ∧ F(bread_sliced ∧ knife_in_trash ∧ F(bread_cooled ∧ at_trash_can)))) ∧ F(slice_in_trash)"
}
```

### LTL Representations
- **Sequential LTL**: Basic temporal ordering with eventually operators
- **Sequential with Conditions**: Conditional sequencing with next operators  
- **Structured LTL**: High-level temporal constraints with until operators
- **Atomic Predicates**: Categorized state variables for locations, objects, and actions

## 🔍 Algorithm Details

### Translation Module
1. **Input**: Natural language task description
2. **Process**: Few-shot prompting with LTL examples
3. **Validation**: Syntax checking using Spot library
4. **Output**: Formal LTL formula with atomic propositions

### Verification Module
1. **Input**: Action sequence + LTL formula
2. **Process**: Sliding window analysis (window size: 5) with LLM reasoning
3. **Detection**: Three error types identification
4. **Correction**: Reordering, insertion, removal operations

## 📄 Citation

```bibtex
@article{grigorev2024verifyllm,
  title={VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots},
  author={Grigorev, Danil S. and Kovalev, Alexey K. and Panov, Aleksandr I.},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

---

<div align="center">

**[🔝 Back to Top](#verifyllm-llm-based-pre-execution-task-plan-verification-for-robots)**


</div>

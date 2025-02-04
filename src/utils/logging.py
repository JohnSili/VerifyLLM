from datetime import datetime
from typing import Dict, List
from rich.console import Console
from rich.table import Table
import json
import os

console = Console()

def create_log_directory() -> str:
    """Creates a directory for logs with current date and time"""
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"test_logs_{current_time}"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def save_analysis_results(log_dir: str, step_index: int, window_info: Dict, 
                         raw_response: str, processed_result: Dict):
    """Saves detailed information about each analysis step"""
    filename = f"step_{step_index}_analysis.json"
    filepath = os.path.join(log_dir, filename)
    
    analysis_data = {
        "step_info": {
            "step_number": step_index,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "window_analysis": window_info,
        "raw_model_response": raw_response,
        "processed_analysis": processed_result
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)

def print_sequence_comparison(original_sequence: List[str], optimized_sequence: List[str]):
    """Prints a comparative table of sequences"""
    table = Table(title="Sequence Comparison")
    table.add_column("Step", style="cyan")
    table.add_column("Original Action", style="yellow")
    table.add_column("Optimized Action", style="green")

    max_len = max(len(original_sequence), len(optimized_sequence))
    for i in range(max_len):
        orig_action = original_sequence[i] if i < len(original_sequence) else "-"
        opt_action = optimized_sequence[i] if i < len(optimized_sequence) else "-"
        table.add_row(str(i+1), orig_action, opt_action)

    console.print(table)

def save_comparison_results(log_dir: str, original_sequence: List[str], optimized_sequence: List[str]) -> str:
    """Saves sequence comparison results"""
    comparison_file = os.path.join(log_dir, "final_comparison.json")
    comparison_data = {
        "original_sequence": original_sequence,
        "optimized_sequence": optimized_sequence,
        "statistics": {
            "original_length": len(original_sequence),
            "optimized_length": len(optimized_sequence),
            "actions_removed": len(original_sequence) - len(optimized_sequence),
            "optimization_ratio": len(optimized_sequence) / len(original_sequence)
        }
    }

    with open(comparison_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)

    return comparison_file

def print_window_info(window_info: Dict, step: int, total_steps: int):
    """Prints window analysis information"""
    console.print(f"\n╭──────────── Analysis Window {step}/{total_steps} ────────────╮")
    console.print(f"│ Window Range: {window_info['window_start']} to {window_info['window_end']}")
    console.print(f"│ Previous actions: {window_info['previous_actions']}")
    console.print(f"│ Current action: {window_info['current_action']}")
    console.print(f"│ Next actions: {window_info['next_actions']}")
    console.print("╰" + "─" * 46 + "╯")

def print_analysis_result(action: str, analysis: Dict, step: int, total_steps: int):
    """Prints analysis results"""
    console.print(f"\n╭{'─' * 47} Analysis Result {step}/{total_steps} {'─' * 46}╮")
    console.print(f"│ Action: {action}")
    if "optimization_decision" in analysis:
        decision = analysis["optimization_decision"]
        console.print(f"│ Position optimal: {analysis['position_analysis']['is_position_optimal']}")
        console.print(f"│ Action necessary: {analysis['necessity_analysis']['is_action_necessary']}")
        console.print(f"│ Decision: {decision['decision']}")
        console.print(f"│ Details: {decision['details']}")
    console.print("╰" + "─" * 105 + "╯")
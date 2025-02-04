from ..models import ProcessingResult, WindowInfo
from rich.console import Console
from rich.table import Table
from datetime import datetime
from anthropic import Anthropic
from typing import Dict, List
import json
import os

class ContextWindowOptimizer:
    def __init__(self, api_key: str, look_back: int = 2, look_forward: int = 2, 
                 model: str = "claude-3-opus-20240229"):
        self.look_back = look_back
        self.look_forward = look_forward
        self.log_dir = self.create_log_directory()
        self.console = Console()
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def create_log_directory(self) -> str:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = f"test_logs_{current_time}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def get_window_info(self, sequence: List[str], current_index: int) -> WindowInfo:
        start_idx = max(0, current_index - self.look_back)
        end_idx = min(len(sequence), current_index + self.look_forward + 1)
        return WindowInfo(
            window_start=start_idx,
            window_end=end_idx,
            current_action=sequence[current_index],
            current_index=current_index,
            previous_actions=sequence[start_idx:current_index],
            next_actions=sequence[current_index + 1:end_idx],
            full_window=sequence[start_idx:end_idx]
        )

    def create_context_prompt(self, window_info: WindowInfo, task: str, atomic_propositions: List[str]) -> str:
        base_context = """You are a robotic action sequence optimizer. Analyze the current action in context of surrounding actions and the overall task to determine if any optimizations are needed.

TASK:
{task}

ATOMIC PROPOSITIONS:
The following atomic propositions have been validated for this task:
{atomic_props}

CONTEXT:
Previous {look_back} actions: {prev_actions}
Current action: {current}
Next {look_forward} actions: {next_actions}

Consider the following aspects:
1. Is the current action in the right position relative to its context and the atomic propositions?
2. Are there any missing actions needed between current and surrounding actions?
3. Is this action redundant given the context and atomic propositions?
4. Does this action align with the validated atomic propositions?

RESPOND EXACTLY IN THIS FORMAT:
{{
    "window_analysis": {{
        "current_action": "{current}",
        "window_range": {{"start": {start}, "end": {end}}},
        "analyzed_window": {full_window}
    }},
    "position_analysis": {{
        "is_position_optimal": true/false,
        "optimal_position": "before/after X action or current",
        "reasoning": "Explain why the position should or should not change"
    }},
    "necessity_analysis": {{
        "is_action_necessary": true/false,
        "redundancy_reason": null or "Explain why action is redundant",
        "missing_actions": [],
        "reasoning": "Explain why action is necessary or redundant and why certain actions might be missing"
    }},
    "optimization_decision": {{
        "decision": "keep/move/remove/augment",
        "details": "Detailed explanation of the decision",
        "suggested_changes": {{
            "position_change": null or "index:number",
            "actions_to_add": [],
            "remove_action": false
        }}
    }}
}}"""

        return base_context.format(
            task=task,
            atomic_props=", ".join(atomic_propositions),
            look_back=self.look_back,
            look_forward=self.look_forward,
            prev_actions=json.dumps(window_info.previous_actions),
            current=window_info.current_action,
            next_actions=json.dumps(window_info.next_actions),
            start=window_info.window_start,
            end=window_info.window_end,
            full_window=json.dumps(window_info.full_window)
        )

    def generate_response(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def apply_sequence_optimizations(self, sequence: List[str], analysis_results: List[Dict]) -> List[str]:
        optimized_sequence = sequence.copy()
        modifications = []

        for result in analysis_results:
            if "analysis" in result:
                decision = result["analysis"]["optimization_decision"]
                changes = decision["suggested_changes"]
                modifications.append({
                    "index": result["action_index"],
                    "action": result["action"],
                    "decision": decision["decision"],
                    "changes": changes
                })

        # Handle removals first
        modifications_remove = [m for m in modifications if m["decision"] == "remove"]
        for mod in reversed(modifications_remove):
            if mod["changes"].get("remove_action", False):
                del optimized_sequence[mod["index"]]

        # Handle additions
        modifications_add = [m for m in modifications if m["decision"] == "augment"]
        for mod in modifications_add:
            actions_to_add = mod["changes"].get("actions_to_add", [])
            for action in actions_to_add:
                optimized_sequence.insert(mod["index"], action)

        # Handle moves last
        modifications_move = [m for m in modifications if m["decision"] == "move"]
        for mod in modifications_move:
            position_change = mod["changes"].get("position_change")
            if position_change:
                try:
                    current_index = optimized_sequence.index(mod["action"])
                    new_index = int(position_change.split(":")[1])
                    if new_index >= 0 and new_index < len(optimized_sequence):
                        action = optimized_sequence.pop(current_index)
                        optimized_sequence.insert(new_index, action)
                except (ValueError, IndexError):
                    continue

        return optimized_sequence

    def optimize_sequence(self, sequence: List[str], atomic_propositions: List[str], task: str) -> ProcessingResult:
        results = []
        sequence_evolution = {
            "original_sequence": sequence,
            "steps": [],
            "atomic_propositions": atomic_propositions
        }

        try:
            for i in range(len(sequence)):
                window_info = self.get_window_info(sequence, i)
                self.console.print(f"\n[bold blue]Analyzing action {i + 1}/{len(sequence)}: {sequence[i]}[/bold blue]")
                
                prompt = self.create_context_prompt(window_info, task, atomic_propositions)
                response = self.generate_response(prompt)
                
                try:
                    json_start = response.find('{')
                    json_end = response.rfind('}') + 1
                    json_response = response[json_start:json_end]
                    analysis = json.loads(json_response)

                    results.append({
                        "action_index": i,
                        "action": sequence[i],
                        "window_info": window_info,
                        "analysis": analysis
                    })

                    sequence_evolution["steps"].append({
                        "step_number": i,
                        "current_action": sequence[i],
                        "window_info": window_info,
                        "analysis_result": analysis,
                        "current_sequence_state": sequence.copy()
                    })

                except json.JSONDecodeError as e:
                    error_info = {
                        "action_index": i,
                        "action": sequence[i],
                        "window_info": window_info,
                        "error": str(e),
                        "raw_response": response
                    }
                    results.append(error_info)
                    sequence_evolution["steps"].append({
                        "step_number": i,
                        "error": str(e),
                        "raw_response": response,
                        "current_sequence_state": sequence.copy()
                    })

            # Apply optimizations based on results
            optimized_sequence = self.apply_sequence_optimizations(sequence, results)
            
            return ProcessingResult(
                success=True,
                data={
                    "original_sequence": sequence,
                    "optimized_sequence": optimized_sequence,
                    "optimization_steps": sequence_evolution
                }
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                data={},
                error=str(e)
            )
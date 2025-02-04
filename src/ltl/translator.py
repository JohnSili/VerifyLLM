from ..models import LTLResult
from anthropic import Anthropic
import requests
from typing import Dict

class LTLTranslator:
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.base_prompt = """Translate the following natural language instruction into an LTL (Linear Temporal Logic) formula and explain your translation step by step.

Key LTL operators:
- X: "next"
- U: "until"
- G: "globally" (always)
- F: "finally" (eventually)
- GF: "infinitely often"

The formula should only contain atomic propositions or operators |, &, !, ->, <->, X, U, G, F.

Important: Use atomic propositions in grounded format:
- Combine words using underscores
- Use lowercase
- No spaces or parentheses within propositions
- Use descriptive names that reflect specific actions/conditions

The LTL formula should always be enclosed within "START:" and "FINISH.".

Examples:
1. Instruction: "Open the fridge and eventually pick up a cup"
   LTL: START: open_fridge & F(pick_up_cup) FINISH.
   Explanation: First open the fridge and then eventually pick up a cup.

2. Instruction: "Clean the room while monitoring the robot's battery level. If battery is low, recharge before continuing"
   LTL: START: G((clean_room & monitor_battery) U room_clean) & G(battery_low -> (X recharge & F resume_cleaning)) FINISH.
   Explanation: Continuously clean and monitor battery until room is clean, and if battery gets low, immediately recharge then eventually resume.

3. Instruction: "Whenever entering kitchen check if fridge is open, if so close it"
   LTL: START: G(enter_kitchen -> (check_fridge & (fridge_open -> X close_fridge))) FINISH.
   Explanation: Globally, when entering kitchen, check fridge and if it's open, close it in the next step."""

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

    def extract_ltl_formula(self, claude_response: str) -> str:
        try:
            start_idx = claude_response.find("START:")
            end_idx = claude_response.find("FINISH.")
            if start_idx == -1 or end_idx == -1:
                return ""
            formula = claude_response[start_idx:end_idx + 7].strip()
            return formula
        except Exception as e:
            print(f"Error extracting LTL formula: {str(e)}")
            return ""

    def validate_ltl_formula(self, ltl_formula: str) -> Dict:
        url = "http://45.86.180.122/formula/validate"
        cleaned_formula = ltl_formula.replace("START:", "").replace("FINISH.", "").strip()
        payload = {"formula_text": cleaned_formula}
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def create_prompt(self, instruction: str, error: str = "") -> str:
        prompt = self.base_prompt
        if error:
            prompt += f"\nConsider the following error in the previous formula: {error}\n"
        prompt += f"\nPlease revise and translate the following instruction into a corrected LTL formula, following the syntax guidelines above:\n\n{instruction}"
        return prompt

    def translate_and_validate(self, instruction: str, error: str = "") -> LTLResult:
        prompt = self.create_prompt(instruction, error)
        response = self.generate_response(prompt)
        formula = self.extract_ltl_formula(response)
        validation_result = self.validate_ltl_formula(formula)
        
        if validation_result["success"]:
            return LTLResult(
                formula=formula,
                atomic_propositions=validation_result["atomic_propositions"],
                success=True
            )
        return LTLResult(
            formula=formula,
            atomic_propositions=[],
            success=False,
            error=validation_result["error"]
        )
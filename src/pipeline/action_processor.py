from ..ltl.translator import LTLTranslator
from ..optimization.context_window import ContextWindowOptimizer
from ..models import ProcessingResult, LTLResult

class ActionProcessor:
    def __init__(self, api_key: str, look_back: int = 2, look_forward: int = 2):
        self.api_key = api_key
        self.ltl_translator = LTLTranslator(api_key)
        self.optimizer = ContextWindowOptimizer(api_key, look_back, look_forward)

    def process_instruction(self, instruction: str, task: str, max_retries: int = 3) -> ProcessingResult:
        # First, translate to LTL and get atomic propositions
        ltl_result = self.ltl_translator.translate_and_validate(instruction)
        
        retry_count = 0
        while not ltl_result.success and retry_count < max_retries:
            print(f"LTL validation failed. Retrying... (Attempt {retry_count + 1}/{max_retries})")
            ltl_result = self.ltl_translator.translate_and_validate(
                instruction, 
                error=ltl_result.error
            )
            retry_count += 1

        if not ltl_result.success:
            return ProcessingResult(
                success=False,
                data={},
                error="Failed to generate valid LTL formula"
            )

        # Split instruction into sequence
        sequence = instruction.split(", ")
        
        # Use atomic propositions for sequence optimization
        return self.optimizer.optimize_sequence(
            sequence=sequence,
            atomic_propositions=ltl_result.atomic_propositions,
            task=task
        )
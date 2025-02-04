from src.pipeline.action_processor import ActionProcessor
from src.utils.logging import print_sequence_comparison

def main():
    API_KEY = 'your-api-key'  # Replace with your Anthropic API key
    processor = ActionProcessor(api_key=API_KEY)
    
    # Example task and instruction
    task = "Attach the thermometer to the window"
    instruction = "Walk to the table, Grab the thermometer from the table, Walk to the window"
    
    result = processor.process_instruction(instruction, task)
    
    if result.success:
        print("\nProcessing successful!")
        original_sequence = result.data["original_sequence"]
        optimized_sequence = result.data["optimization_steps"]
        print_sequence_comparison(original_sequence, optimized_sequence)
    else:
        print("\nProcessing failed:", result.error)

if __name__ == "__main__":
    main()
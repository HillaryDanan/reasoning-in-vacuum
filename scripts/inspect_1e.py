#!/usr/bin/env python3
import json

# Load GPT-4 1e results
with open('data/results/raw/exp1e_transfer_gpt-4-0125-preview_20251007_103212.json', 'r') as f:
    gpt4 = json.load(f)

print("GPT-4 Condition 1e Analysis:")
print("="*60)

control_correct = 0
transfer_correct = 0

for r in gpt4['responses']:
    if r['correct']:
        # Try to determine if control or transfer
        expected = r['expected_output']
        input_seq = r['input']
        
        # Rotate-by-1: last → first
        rotate1 = [input_seq[-1]] + input_seq[:-1]
        # Rotate-by-2: last two → first
        rotate2 = input_seq[-2:] + input_seq[:-2] if len(input_seq) >= 3 else input_seq
        
        print(f"\nItem {r['item_number']}:")
        print(f"  Input: {input_seq}")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {r['model_output_parsed']}")
        print(f"  Rotate-by-1 would be: {rotate1}")
        print(f"  Rotate-by-2 would be: {rotate2}")
        
        if expected == rotate1:
            print(f"  → This is a CONTROL item (rotate-by-1)")
            control_correct += 1
        elif expected == rotate2:
            print(f"  → This is a TRANSFER item (rotate-by-2)")
            transfer_correct += 1

print(f"\nSummary:")
print(f"Control correct: {control_correct}/10")
print(f"Transfer correct: {transfer_correct}/10")
print(f"Total: {control_correct + transfer_correct}/20")

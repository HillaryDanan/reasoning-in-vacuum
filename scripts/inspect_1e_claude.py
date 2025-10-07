#!/usr/bin/env python3
import json

with open('data/results/raw/exp1e_transfer_claude-3-5-sonnet-20241022_20251007_103324.json', 'r') as f:
    claude = json.load(f)

print("Claude Condition 1e Analysis:")
print("="*60)

control_correct = 0
transfer_correct = 0

for r in claude['responses']:
    if r['correct']:
        expected = r['expected_output']
        input_seq = r['input']
        
        rotate1 = [input_seq[-1]] + input_seq[:-1]
        rotate2 = input_seq[-2:] + input_seq[:-2] if len(input_seq) >= 3 else input_seq
        
        print(f"\nItem {r['item_number']}:")
        print(f"  Input: {input_seq}")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {r['model_output_parsed']}")
        
        if expected == rotate1:
            print(f"  → This is a CONTROL item (rotate-by-1)")
            control_correct += 1
        elif expected == rotate2:
            print(f"  → This is a TRANSFER item (rotate-by-2)")
            transfer_correct += 1

print(f"\nSummary:")
print(f"Control correct: {control_correct}/10")
print(f"Transfer correct: {transfer_correct}/10")

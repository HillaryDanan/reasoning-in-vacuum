#!/usr/bin/env python3
"""
Generate figures for paper submission.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# Create outputs directory
FIGURES_DIR = Path("outputs/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Figure 1: Performance Across All Conditions
def create_figure_1():
    """Bar chart showing performance collapse across conditions."""
    
    conditions = ['Version 1\n(20 examples)', 'Version 1b\n(3 examples)', 
                  'Condition 1c\n(Ambiguity)', 'Condition 1d\n(Scaling)', 
                  'Condition 1e\n(Control)']
    
    gpt4_scores = [100, 30, 65, 45, 0]
    claude_scores = [100, 10, 45, 10, 0]
    chance_levels = [16.7, 16.7, 50, 16.7, 16.7]  # Approximate for 1d
    
    x = np.arange(len(conditions))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Bars
    bars1 = ax.bar(x - width, gpt4_scores, width, label='GPT-4', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, claude_scores, width, label='Claude 3.5', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, chance_levels, width, label='Chance Level', 
                   color='#95a5a6', alpha=0.5, edgecolor='black', linewidth=1.2, 
                   hatch='///')
    
    # Formatting
    ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Experimental Condition', fontsize=14, fontweight='bold')
    ax.set_title('Systematic Performance Collapse Across Conditions', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=11)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    ax.set_ylim(0, 110)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    
    # Add significance markers
    # Version 1: significant
    ax.text(0, 105, '***', ha='center', fontsize=16, fontweight='bold')
    # Others: not significant (NS)
    for i in range(1, 5):
        ax.text(i, max(gpt4_scores[i], claude_scores[i]) + 8, 'NS', 
                ha='center', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure1_performance_collapse.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure1_performance_collapse.pdf', bbox_inches='tight')
    print("✓ Figure 1 created")
    plt.close()

# Figure 2: Example Stimuli
def create_figure_2():
    """Show example stimuli from each condition."""
    
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle('Example Stimuli Across Experimental Conditions', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Version 1 (abundant examples)
    ax = axes[0, 0]
    ax.text(0.5, 0.9, 'Version 1: Abundant Examples (20)', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    example_text = "Training (20 examples shown):\n⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n...(18 more examples)...\n\nTest:\n⬯ ⨇ ⨝ → ?"
    ax.text(0.1, 0.5, example_text, fontsize=11, family='monospace', 
            verticalalignment='center', transform=ax.transAxes)
    ax.axis('off')
    
    # Version 1b (minimal examples)
    ax = axes[0, 1]
    ax.text(0.5, 0.9, 'Version 1b: Minimal Examples (3)', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    example_text = "Training (only 3 examples):\n⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n⨆ ⨇ ⨈ → ⨈ ⨆ ⨇\n\nTest:\n⬯ ⨇ ⨝ → ?"
    ax.text(0.1, 0.5, example_text, fontsize=11, family='monospace', 
            verticalalignment='center', transform=ax.transAxes)
    ax.axis('off')
    
    # Condition 1c (ambiguity)
    ax = axes[1, 0]
    ax.text(0.5, 0.9, 'Condition 1c: Ambiguity (2 rules)', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    example_text = "Training:\n⨀ ⨁ ⨂ ★ → ⨂ ⨀ ⨁  (rotate)\n⨃ ⨄ ⨅ ★ → ⨅ ⨃ ⨄\n⨆ ⨇ ⨈ ★ → ⨈ ⨆ ⨇\n\n⨉ ⨊ ⨋ ◆ → ⨋ ⨊ ⨉  (reverse)\n⨌ ⨍ ⨎ ◆ → ⨎ ⨍ ⨌\n⨏ ⨐ ⨑ ◆ → ⨑ ⨐ ⨏\n\nTest:\n⬯ ⨇ ⨝ ★ → ?"
    ax.text(0.05, 0.5, example_text, fontsize=10, family='monospace', 
            verticalalignment='center', transform=ax.transAxes)
    ax.axis('off')
    
    # Condition 1d (scaling)
    ax = axes[1, 1]
    ax.text(0.5, 0.9, 'Condition 1d: Complexity Scaling', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    example_text = "Training (3-symbol):\n⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n⨆ ⨇ ⨈ → ⨈ ⨆ ⨇\n\nTest:\n3-symbol: ⬯ ⨇ ⨝ → ?\n4-symbol: ⬯ ⨇ ⨝ ◊ → ?\n5-symbol: ⬯ ⨇ ⨝ ◊ ⨥ → ?"
    ax.text(0.05, 0.5, example_text, fontsize=10, family='monospace', 
            verticalalignment='center', transform=ax.transAxes)
    ax.axis('off')
    
    # Condition 1e (transfer)
    ax = axes[2, 0]
    ax.text(0.5, 0.9, 'Condition 1e: Rule Transfer', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    example_text = "Training (rotate-by-1):\n⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n⨆ ⨇ ⨈ → ⨈ ⨆ ⨇\n\nTest Control (rotate-by-1):\n⬯ ⨇ ⨝ → ⨝ ⬯ ⨇\n\nTest Transfer (rotate-by-2):\n⬯ ⨇ ⨝ → ⨇ ⨝ ⬯"
    ax.text(0.05, 0.5, example_text, fontsize=10, family='monospace', 
            verticalalignment='center', transform=ax.transAxes)
    ax.axis('off')
    
    # Design principle
    ax = axes[2, 1]
    ax.text(0.5, 0.9, 'Key Design Principle', 
            ha='center', fontsize=13, fontweight='bold', transform=ax.transAxes)
    principle_text = "Critical Feature:\n\nTraining and test use\nCOMPLETELY DISJOINT\nsymbol sets.\n\nNo symbol appears in both.\n\nPrevents memorization,\nforces abstraction."
    ax.text(0.5, 0.45, principle_text, fontsize=11, ha='center',
            verticalalignment='center', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure2_stimuli_examples.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure2_stimuli_examples.pdf', bbox_inches='tight')
    print("✓ Figure 2 created")
    plt.close()

# Figure 3: Statistical Summary
def create_figure_3():
    """Statistical comparison across conditions."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: P-values
    conditions = ['V1b\n(3 ex)', '1c\n(ambig)', '1e\n(control)']
    gpt4_p = [0.102, 0.132, 1.0]  # 1.0 for 0/10 is clearly NS
    claude_p = [0.870, 0.824, 1.0]
    
    x = np.arange(len(conditions))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, gpt4_p, width, label='GPT-4', 
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x + width/2, claude_p, width, label='Claude 3.5', 
                    color='#e74c3c', alpha=0.8, edgecolor='black')
    
    ax1.axhline(y=0.05, color='red', linestyle='--', linewidth=2, 
                label='α = 0.05 (significance threshold)')
    ax1.set_ylabel('p-value', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Condition', fontsize=13, fontweight='bold')
    ax1.set_title('Statistical Significance Tests\n(vs. Chance Performance)', 
                  fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_ylim(0, 1.05)
    ax1.text(0.02, 0.98, 'None significant (all p > 0.05)', 
             transform=ax1.transAxes, fontsize=11, 
             verticalalignment='top', style='italic',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Panel B: Performance drop from V1
    conditions_drop = ['V1b\n(3 ex)', '1c\n(ambig)', '1d\n(scale)', '1e\n(control)']
    gpt4_drop = [70, 35, 55, 100]  # Percentage point drops
    claude_drop = [90, 55, 90, 100]
    
    x2 = np.arange(len(conditions_drop))
    
    bars3 = ax2.bar(x2 - width/2, gpt4_drop, width, label='GPT-4', 
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars4 = ax2.bar(x2 + width/2, claude_drop, width, label='Claude 3.5', 
                    color='#e74c3c', alpha=0.8, edgecolor='black')
    
    ax2.set_ylabel('Performance Drop from V1 (%)', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Condition', fontsize=13, fontweight='bold')
    ax2.set_title('Magnitude of Performance Collapse\n(from 100% in Version 1)', 
                  fontsize=14, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(conditions_drop)
    ax2.legend(loc='upper left', fontsize=10)
    ax2.set_ylim(0, 110)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'figure3_statistical_summary.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'figure3_statistical_summary.pdf', bbox_inches='tight')
    print("✓ Figure 3 created")
    plt.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GENERATING FIGURES FOR PAPER SUBMISSION")
    print("="*60 + "\n")
    
    create_figure_1()
    create_figure_2()
    create_figure_3()
    
    print("\n" + "="*60)
    print("✓ ALL FIGURES GENERATED")
    print("="*60)
    print(f"\nFiles saved to: {FIGURES_DIR}")
    print("  - figure1_performance_collapse.png/pdf")
    print("  - figure2_stimuli_examples.png/pdf")
    print("  - figure3_statistical_summary.png/pdf")
    print("\nReady for journal submission!")
    print("="*60 + "\n")

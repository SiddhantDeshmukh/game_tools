#!/home/sdeshmukh/anaconda3/bin/python
# Quickly check hyperbolic stacking for a reasonable range of values
from ror2_stats import exponential_stacking, hyperbolic_stacking
import sys
import numpy as np


def main():
  alpha = float(sys.argv[1])
  num_stacks = np.array(range(0, 11))
  chances = exponential_stacking(num_stacks, alpha)
  inverse_chances = exponential_stacking(num_stacks, 1 / alpha)
  # Usually want both normal and inverse
  for i, (chance, inverse_chance) in enumerate(zip(chances, inverse_chances)):
    print(f"{i} stacks: {chance*100:.2f}%, {inverse_chance*100:.2f}%")


if __name__ == "__main__":
  main()

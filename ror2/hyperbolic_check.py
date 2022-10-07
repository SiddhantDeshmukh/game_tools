#!/home/sdeshmukh/anaconda3/bin/python
# Quickly check hyperbolic stacking for a reasonable range of values
from ror2_stats import hyperbolic_stacking
import sys
import numpy as np


def main():
  alpha = float(sys.argv[1])
  num_stacks = np.array(range(0, 36))
  chances = hyperbolic_stacking(num_stacks, alpha)
  for i, chance in enumerate(chances):
    print(f"{i} stacks: {chance*100:.2f}%")


if __name__ == "__main__":
  main()

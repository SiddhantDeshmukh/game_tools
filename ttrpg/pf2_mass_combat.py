# From https://www.reddit.com/r/Pathfinder2e/comments/dwxpba/mass_combat_for_pathfinder_2nd_edition/
# Quickly figure out scaling and interpolate between values based on the
# values in the table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Creature:
  # Basic PF2 Creature with stats to create Armies out of them
  strength: int
  dexterity: int
  constitution: int
  intelligence: int
  wisdom: int
  charisma: int
  hp: int
  level: int

  def __init__(self, strength: int, dexterity: int, constitution: int,
               intelligence: int, wisdom: int, charisma: int, hp: int,
               level: int) -> None:
    pass


def random_creature(ranges={"strength": (-5, 5),
                            "dexterity": (-5, 5),
                            "constitution": (-5, 5),
                            "intelligence": (-5, 5),
                            "wisdom": (-5, 5),
                            "charisma": (-5, 5)}):
  # Random stats
  return creature


class Army:
  size: str  # qualitative
  num_units: int
  level_adjust: int
  stat_adjust: int
  hp_adjust: int
  army_level: int

  def __init__(self, creature: Creature, size: str, num_units: int,
               level_adjust: int, stat_adjust: int, hp_adjust: int,
               army_level: int) -> None:
    pass

  @classmethod
  def from_random_creature(cls):

    army = cls(...)
    return army


def main():
  data_dir = "./res"
  reference_df = pd.read_csv(f"{data_dir}/pf2_mass_combat_table.csv")
  print(reference_df)


if __name__ == "__main__":
  main()


"""
TODO:
  - Create an Army out of a Creature
  - Combine different Creatures into different Armies
"""

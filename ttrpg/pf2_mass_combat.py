# From https://www.reddit.com/r/Pathfinder2e/comments/dwxpba/mass_combat_for_pathfinder_2nd_edition/
# Quickly figure out scaling and interpolate between values based on the
# values in the table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev


# Global variables for creature ranges and scaling for armies
# TODO: - move to a separate library
STANDARD_CREATURE_RANGES = {
    "strength": (-5, 5),
    "dexterity": (-5, 5),
    "constitution": (-5, 5),
    "intelligence": (-5, 5),
    "wisdom": (-5, 5),
    "charisma": (-5, 5),
    "hp": (1, 200),
    "level": (-1, 20)
}

DATA_DIR = "./res"
ARMY_SCALING_DF = pd.read_csv(f"{DATA_DIR}/pf2_mass_combat_table.csv")


def prettify_string(s): return s.replace("_", " ").title()


class Scaler:
  def __init__(self, scaling_df: pd.DataFrame, x_key='num_units') -> None:
    # 'x' is 'num_units' by default, any key with 'adjust' is a 'y_i'
    self.scaling_df = scaling_df
    self.x_key = x_key
    self.y_keys = [k for k in scaling_df.keys() if k.endswith("adjust")]
    self.x = np.array([int(x_i) for x_i in self.scaling_df[self.x_key]])
    self.y_arrs = np.array([[int(y_i) for y_i in scaling_df[y_key]]
                            for y_key in self.y_keys])

    # Compute scaling relations for each key
    self.splreps = {k: splrep(self.x, y)
                    for k, y in zip(self.y_keys, self.y_arrs)}

  def plot_scaling(self, eval_x=np.linspace(1, 2000, num=300)):
    # Plot scaling for all y_keys as f(x)
    fig, axes = plt.subplots(ncols=2, nrows=len(self.y_keys) // 2)
    for i, y_key in enumerate(self.y_keys):
      i_x, i_y = i // 2, i % 2
      # Scaling
      axes[i_x, i_y].plot(self.x, self.scale(self.x, y_key))
      # Points
      axes[i_x, i_y].plot(self.x, self.y_arrs[i],
                          ls="none", marker="o", c="k", mfc="r")
      # Aesthetics
      axes[i_x, i_y].set_xlabel(prettify_string(self.x_key))
      axes[i_x, i_y].set_ylabel(prettify_string(y_key))

    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    return fig, axes

  def scale(self, x, y_key):
    # By default, cast return to an int
    y_out = splev(x, self.splreps[y_key])
    return y_out


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
    self.strength = strength
    self.dexterity = dexterity
    self.constitution = constitution
    self.intelligence = intelligence
    self.wisdom = wisdom
    self.charisma = charisma
    self.hp = hp
    self.level = level

  def __str__(self) -> str:
    output = "Creature:\n"
    output += f"\tSTR: {self.strength:+}\n"
    output += f"\tDEX: {self.dexterity:+}\n"
    output += f"\tCON: {self.constitution:+}\n"
    output += f"\tWIS: {self.wisdom:+}\n"
    output += f"\tINT: {self.intelligence:+}\n"
    output += f"\tCHA: {self.charisma:+}\n"
    output += f"\tHP: {self.hp}\n"
    output += f"\tLevel: {self.level}\n"

    return output

  @classmethod
  def from_random_stats(cls, ranges=STANDARD_CREATURE_RANGES):
    # Generate a random integer stat foreach property
    # NOTE: does not check if a value is missing from 'ranges'!
    stats = {}
    for stat_name, stat_range in ranges.items():
      stats[stat_name] = np.random.randint(stat_range[0], stat_range[1])

    creature = cls(**stats)
    return creature


class Army:
  def __init__(self, creature: Creature, num_units: int,
               level_adjust: int, stat_adjust: int, hp_adjust: int,
               army_level_adjust: int) -> None:
    self.creature = creature  # base creature type
    self.num_units = num_units

    self.strength = int(creature.strength + stat_adjust)
    self.dexterity = int(creature.dexterity + stat_adjust)
    self.constitution = int(creature.constitution + stat_adjust)
    self.intelligence = int(creature.intelligence + stat_adjust)
    self.wisdom = int(creature.wisdom + stat_adjust)
    self.charisma = int(creature.charisma + stat_adjust)
    self.hp = int(creature.hp + hp_adjust)
    self.level = int(creature.level + level_adjust)
    self.army_level = int(self.level + army_level_adjust)

  def __str__(self) -> str:
    output = f"Army with {self.num_units} creatures:\n"
    output += f"\tSTR: {self.strength:+}\n"
    output += f"\tDEX: {self.dexterity:+}\n"
    output += f"\tCON: {self.constitution:+}\n"
    output += f"\tWIS: {self.wisdom:+}\n"
    output += f"\tINT: {self.intelligence:+}\n"
    output += f"\tCHA: {self.charisma:+}\n"
    output += f"\tHP: {self.hp}\n"
    output += f"\tLevel: {self.level}\n"
    output += f"\tArmy Level: {self.army_level}\n"

    return output

  @classmethod
  def from_creature(cls, creature: Creature, scaler: Scaler, num_units=10):
    # Scale a Creature using Scaler to be an Army of 'num_units'
    # NOTE:
    # - 'y_keys' must match attributes that Army has apart from 'creature', 'num_units'
    scaled_values = {k: scaler.scale(num_units, k) for k in scaler.y_keys}
    army = cls(creature, num_units, **scaled_values)
    return army

  @classmethod
  def from_random_creature(cls, scaler: Scaler,
                           ranges=STANDARD_CREATURE_RANGES, num_units=10):
    # Scale a random creature to 'num_units' using standard scaling routines
    creature = Creature.from_random_stats(ranges=ranges)
    army = cls.from_creature(creature, scaler, num_units=num_units)
    return army


def main():
  np.random.seed(42)
  scaler = Scaler(ARMY_SCALING_DF)
  fig, axes = scaler.plot_scaling()
  plt.savefig("./figs/scaling.png", bbox_inches="tight")

  random_creature = Creature.from_random_stats()
  print(random_creature)
  num_units = 150  # 'medium'
  random_army = Army.from_creature(random_creature, scaler,
                                   num_units=num_units)
  more_random_army = Army.from_random_creature(scaler, num_units=num_units)
  print(random_army)
  print(more_random_army)


if __name__ == "__main__":
  main()


"""
TODO:
  - Create an Army out of a Creature
  - Combine different Creatures into different Armies
  - Refactor into different files and make a PF2 directory to hold this in
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 22:23:45 2024

@author: mariamraheem
"""

# Mariam Raheem

from numpy import random, mean

"""
Adaptation of the Schelling model of segregation in Python from lecture 18
Model has a world with size and 200 agents
"""

params = {'world_size': (5, 5),
          'num_agents': 100,
          'out_path': '/Users/mariamraheem/Documents/GitHub/lab-9b/lab 9b_abm.csv'}


class Agent:
    def __init__(self, world):
        self.world = world
        self.location = None

    def move(self):
        vacancies = self.world.find_vacant(return_all=True)
        if vacancies:
            for patch in vacancies:
                self.world.grid[self.location] = None
                self.location = patch
                self.world.grid[patch] = self
                return
        # If no vacant patches available, set agent location to None
        self.location = None


class World:
    def __init__(self, params):
        self.params = params
        self.grid = self.build_grid(params['world_size'])
        self.agents = self.build_agents(params['num_agents'])

    def build_grid(self, world_size):
        locations = [(i, j) for i in range(world_size[0]) for j in range(world_size[1])]
        return {l: None for l in locations}

    def build_agents(self, num_agents):
        agents = [Agent(self) for _ in range(num_agents)]
        random.shuffle(agents)
        return agents

    def find_vacant(self, return_all=False):
        empties = [loc for loc, occupant in self.grid.items() if occupant is None]
        if empties:
            if return_all:
                return empties
            else:
                return random.choice(empties)
        else:
            return None  # Return None if there are no vacant patches left
    

    def run_simulation(self):
        agents_without_home = []
        agents_with_home = []

        with open(self.params['out_path'], 'w') as f:
            for i in range(self.params['num_agents']):
                agent = self.agents[i]
                agent.move()
                self.print_grid(f)
                f.write(f"Agent {i + 1}/{self.params['num_agents']} moved.\n")

                if agent.location is None:
                    agents_without_home.append(i + 1)
                else:
                    agents_with_home.append(i + 1)

                # Shuffle agents after each move
                random.shuffle(self.agents)

            f.write(f"\nAgents without homes ({len(agents_without_home)}): {agents_without_home}\n")
            f.write(f"Agents with homes ({len(agents_with_home)}): {agents_with_home}\n")

            print(f"Agents without homes: {len(agents_without_home)}")
            print(f"Agents with homes: {len(agents_with_home)}")

    def print_grid(self, f):
        for i in range(self.params['world_size'][0]):
            for j in range(self.params['world_size'][1]):
                agent = self.grid[(i, j)]
                if agent:
                    f.write('X')
                else:
                    f.write('.')
            f.write('\n')
        f.write('\n')

# Create world and run simulation
world = World(params)
world.run_simulation()

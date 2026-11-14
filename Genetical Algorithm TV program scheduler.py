"""Interactive TV scheduling genetic algorithm, adapted from the supplied notebook.
Run: streamlit run "Genetical Algorithm TV program scheduler.py"
Requires: streamlit, pandas
"""
from pathlib import Path
import random

import pandas as pd
import streamlit as st

GEN = 100
POP = 50
EL_S = 2
DATA_PATH = Path(__file__).with_name('program_ratings (changed).csv')

st.set_page_config(page_title='Genetic Algorithm TV Scheduler', page_icon='📺')
st.title('📺 Genetic Algorithm — TV Program Scheduling')
st.write('Change the parameters below and run the genetic algorithm to generate a TV schedule.')

CO_R = st.slider('CO_R — Crossover Rate', min_value=0.0, max_value=0.95, value=0.80, step=0.01)
MUT_R = st.number_input('MUT_R — Mutation Rate', min_value=0.0, max_value=1.0, value=0.20, step=0.01, format='%.2f', help='The assignment requests a default of 0.20 but permits values only from 0.01 to 0.05.')
valid_mutation = 0.01 <= MUT_R <= 0.05
if not valid_mutation:
    st.warning('Mutation Rate must be between 0.01 and 0.05. Change the initial 0.20 value to run the algorithm.')

st.write(f'**Selected crossover rate:** {CO_R:.2f} | **Selected mutation rate:** {MUT_R:.2f}')

@st.cache_data
def load_ratings(path: str):
    data = pd.read_csv(path)
    programs = data.iloc[:, 0].astype(str).tolist()
    hours = [int(c.strip().split()[-1]) for c in data.columns[1:]]
    values = data.iloc[:, 1:].apply(pd.to_numeric, errors='raise')
    if values.isna().any().any() or not programs or not hours:
        raise ValueError('CSV contains missing ratings or an empty schedule.')
    return programs, hours, values.to_numpy(dtype=float)

def genetic_algorithm(programs, ratings, generations=GEN, population_size=POP, crossover_rate=0.8, mutation_rate=0.2, elitism_size=EL_S):
    n_hours = ratings.shape[1]
    n_programs = len(programs)

    def fitness(schedule):
        return sum(ratings[program_idx, hour_idx] for hour_idx, program_idx in enumerate(schedule))

    def crossover(a, b):
        if n_hours < 3:
            return a.copy(), b.copy()
        point = random.randint(1, n_hours - 2)
        return a[:point] + b[point:], b[:point] + a[point:]

    def mutate(schedule):
        child = schedule.copy()
        child[random.randrange(n_hours)] = random.randrange(n_programs)
        return child

    population = [[random.randrange(n_programs) for _ in range(n_hours)] for _ in range(population_size)]
    history = []
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        history.append(fitness(population[0]))
        next_population = [p.copy() for p in population[:elitism_size]]
        while len(next_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
            next_population.extend((child1, child2))
        population = next_population[:population_size]
    population.sort(key=fitness, reverse=True)
    history.append(fitness(population[0]))
    return population[0], fitness(population[0]), history

if st.button('Run Genetic Algorithm', type='primary', disabled=not valid_mutation):
    try:
        programs, hours, ratings = load_ratings(str(DATA_PATH))
        best, total, history = genetic_algorithm(programs, ratings, crossover_rate=CO_R, mutation_rate=MUT_R)
        st.success('Genetic Algorithm completed!')
        st.metric('Total Ratings', f'{total:.2f}')
        st.dataframe(pd.DataFrame({'Time Slot': [f'{h:02d}:00' for h in hours], 'Program': [programs[i] for i in best], 'Rating': [ratings[i, j] for j, i in enumerate(best)]}), hide_index=True, use_container_width=True)
        st.subheader('Best fitness by generation')
        st.line_chart(pd.DataFrame({'Best Fitness': history}))
    except (OSError, ValueError) as exc:
        st.error(f'Unable to load ratings data: {exc}')

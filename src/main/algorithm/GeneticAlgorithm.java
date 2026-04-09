package main.algorithm;

import main.model.Chromosome;
import main.model.Task;
import main.utils.FitnessCalculator;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class GeneticAlgorithm {

    private static final Random RANDOM = new Random();
    private final int popSize = 24;
    private final int generations = 60;
    private final double mutationRate = 0.12;
    public final List<Double> history = new ArrayList<>();

    public Chromosome run(Task[] tasks, int vmCount) {
        Chromosome[] population = new Chromosome[popSize];
        for (int i = 0; i < popSize; i++) {
            population[i] = new Chromosome(tasks.length, vmCount); // Random task allocation
        }
      // Fitness Evaluation
        evaluatePopulation(population, tasks, vmCount);
        Chromosome elite = Selection.selectBest(population);
        history.clear();
        history.add((double) FitnessCalculator.getMakespan(elite, tasks, vmCount));

        for (int generation = 0; generation < generations; generation++) {
            Chromosome[] next = new Chromosome[popSize];
            next[0] = new Chromosome(elite);

            for (int i = 1; i < popSize; i++) {
                Chromosome parent1 = tournament(population);
                Chromosome parent2 = tournament(population);
                Chromosome child = Crossover.crossover(parent1, parent2, vmCount);
                Mutation.mutate(child, vmCount, mutationRate);
                child.fitness = FitnessCalculator.calculate(child, tasks, vmCount);
                next[i] = child;
            }

            population = next;
            Chromosome currentBest = Selection.selectBest(population);
            if (currentBest.fitness > elite.fitness) {
                elite = new Chromosome(currentBest);
            }
            history.add((double) FitnessCalculator.getMakespan(elite, tasks, vmCount));
        }

        return elite;
    }

    private void evaluatePopulation(Chromosome[] population, Task[] tasks, int vmCount) {
        for (Chromosome chromosome : population) {
            chromosome.fitness = FitnessCalculator.calculate(chromosome, tasks, vmCount);
        }
    }

    private Chromosome tournament(Chromosome[] population) {
        Chromosome best = population[RANDOM.nextInt(population.length)];
        for (int i = 0; i < 3; i++) {
            Chromosome challenger = population[RANDOM.nextInt(population.length)];
            if (challenger.fitness > best.fitness) {
                best = challenger;
            }
        }
        return best;
    }
}

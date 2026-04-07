package main.model;

import java.util.Random;

public class Chromosome {
    public int[] allocation;
    public double fitness;

    public Chromosome(int taskCount, int vmCount) {
        allocation = new int[taskCount];
        Random rand = new Random();
        for (int i = 0; i < taskCount; i++) {
            allocation[i] = rand.nextInt(vmCount);
        }
    }

    public Chromosome(Chromosome source) {
        this.allocation = source.allocation.clone();
        this.fitness = source.fitness;
    }
}

package main.algorithm;

import main.model.Chromosome;

import java.util.Random;

public class Crossover {

    private static final Random RANDOM = new Random();

    public static Chromosome crossover(Chromosome p1, Chromosome p2, int vmCount) {
        int length = p1.allocation.length;
        Chromosome child = new Chromosome(length, vmCount);
        int pivot = RANDOM.nextInt(length);
        for (int i = 0; i < length; i++) {
            child.allocation[i] = i < pivot ? p1.allocation[i] : p2.allocation[i];
        }
        return child;
    }
}

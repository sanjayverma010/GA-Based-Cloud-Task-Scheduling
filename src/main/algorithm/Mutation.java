package main.algorithm;

import main.model.Chromosome;

import java.util.Random;

public class Mutation {

    private static final Random RANDOM = new Random();

    public static void mutate(Chromosome ch, int vmCount, double rate) {
        for (int i = 0; i < ch.allocation.length; i++) {
            if (RANDOM.nextDouble() < rate) {
                ch.allocation[i] = RANDOM.nextInt(vmCount);
            }
        }
    }
}

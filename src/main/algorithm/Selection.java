package main.algorithm;

import main.model.Chromosome;

public class Selection {

    public static Chromosome selectBest(Chromosome[] pop) {
        Chromosome best = pop[0];
        for (Chromosome c : pop) {
            if (c.fitness > best.fitness) {
                best = c;
            }
        }
        return best;
    }
}

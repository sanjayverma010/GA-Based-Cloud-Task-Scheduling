package main.utils;

import main.model.Chromosome;
import main.model.Task;

public class FitnessCalculator {

    public static double calculate(Chromosome ch, Task[] tasks, int vmCount) {
        int makespan = getMakespan(ch, tasks, vmCount);
        return 1.0 / (makespan + 1.0);
    }

    public static int getMakespan(Chromosome ch, Task[] tasks, int vmCount) {
        int[] load = new int[vmCount];
        for (int i = 0; i < tasks.length; i++) {
            load[ch.allocation[i]] += tasks[i].executionTime;
        }

        int max = 0;
        for (int l : load) {
            if (l > max) {
                max = l;
            }
        }
        return max;
    }
}

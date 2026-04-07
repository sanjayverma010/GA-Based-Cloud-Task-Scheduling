package main.service;

import main.algorithm.FCFS;
import main.algorithm.GeneticAlgorithm;
import main.model.Chromosome;
import main.model.ScheduleResult;
import main.model.Task;
import main.utils.FitnessCalculator;

import java.util.ArrayList;
import java.util.List;

public class SchedulerService {

    private final GeneticAlgorithm ga = new GeneticAlgorithm();

    public ScheduleResult schedule(Task[] tasks, int vmCount) {
        long start = System.currentTimeMillis();
        Chromosome best = ga.run(tasks, vmCount);
        long executionMs = System.currentTimeMillis() - start;
        int gaMakespan = FitnessCalculator.getMakespan(best, tasks, vmCount);
        int fcfsMakespan = FCFS.schedule(tasks, vmCount);
        return new ScheduleResult(best, gaMakespan, fcfsMakespan, executionMs, new ArrayList<>(ga.history));
    }

    public List<Double> getHistory() {
        return new ArrayList<>(ga.history);
    }
}

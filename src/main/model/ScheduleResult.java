package main.model;

import java.util.List;

public class ScheduleResult {
    public final Chromosome bestSolution;
    public final int gaMakespan;
    public final int fcfsMakespan;
    public final double improvementPercent;
    public final long executionMs;
    public final List<Double> history;

    public ScheduleResult(Chromosome bestSolution, int gaMakespan, int fcfsMakespan, long executionMs, List<Double> history) {
        this.bestSolution = bestSolution;
        this.gaMakespan = gaMakespan;
        this.fcfsMakespan = fcfsMakespan;
        this.executionMs = executionMs;
        this.history = history;
        this.improvementPercent = fcfsMakespan > 0 ? ((fcfsMakespan - gaMakespan) * 100.0) / fcfsMakespan : 0;
    }
}

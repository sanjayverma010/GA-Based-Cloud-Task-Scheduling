package main.algorithm;

import main.model.Task;

public class FCFS {

    public static int schedule(Task[] tasks, int vmCount) {
        int[] load = new int[vmCount];

        for (Task task : tasks) {
            int bestVm = 0;
            for (int vm = 1; vm < vmCount; vm++) {
                if (load[vm] < load[bestVm]) {
                    bestVm = vm;
                }
            }
            load[bestVm] += task.executionTime;
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

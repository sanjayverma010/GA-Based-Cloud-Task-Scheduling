# Quick Start Guide

## Prerequisites
- Java 8 or higher installed
- Command line access

## Compilation

**Windows (Command Prompt):**
```bash
cd c:\Users\abc\Desktop\DF\CloudScheduler
javac -d out src\main\**\*.java
```

**Linux/Mac:**
```bash
cd ~/CloudScheduler
javac -d out src/main/**/*.java
```

## Running the Application

**Windows:**
```bash
cd c:\Users\abc\Desktop\DF\CloudScheduler
java -cp out main.App
```

**Linux/Mac:**
```bash
cd ~/CloudScheduler
java -cp out main.App
```

## User Interface Guide

### Input Section (Top Left)
1. **Tasks**: Enter the number of tasks (e.g., 10)
2. **VMs**: Enter the number of virtual machines (e.g., 4)
3. **Execution Times**: Enter comma-separated execution times (e.g., 5,8,3,6,12,4,7,2,9,11)

### Control Buttons
- **Run**: Execute the scheduler with current inputs
- **Reset**: Clear all fields and results
- **Export CSV**: Save metrics and allocation to CSV file

### Output Section (Left Panel)
Shows 4 metrics in real-time:
- **FCFS Makespan**: Simple first-come-first-served baseline
- **GA Makespan**: Genetic algorithm optimized solution
- **Improvement**: Percentage improvement of GA over FCFS
- **Execution Time**: How long the algorithm took (milliseconds)

Below metrics is a **Task Allocation Table** showing which task goes to which VM.

### Gantt Chart (Right Panel, Top)
- **Horizontal bars**: Represent each task
- **Vertical alignment**: Corresponds to VM placement
- **Color coding**: 6 different colors for visual distinction
- **Animation**: Tasks appear one by one as computation progresses
- **Time axis**: Bottom shows the timeline

### Generation Graph (Right Panel, Bottom)
- **Blue curve**: Makespan value over generations
- **X-axis**: Generation number (0 to 60)
- **Y-axis**: Makespan (problem size)
- **Animation**: Line draws progressively
- **Grid**: Reference grid for easy reading

## Example Workflow

### Step 1: Launch Application
```bash
java -cp out main.App
```

### Step 2: Enter Problem Parameters
- Tasks: **8**
- VMs: **3**
- Times: **5,12,3,8,6,14,2,9**

### Step 3: Click Run
- Allow 1-2 seconds for computation
- Watch animations complete

### Step 4: Analyze Results
- Check if GA improvement is positive (goal: >0%)
- View task-to-VM mapping in table
- Observe Gantt chart for load distribution
- Check graph for convergence pattern

### Step 5: Export Results (Optional)
- Click "Export CSV"
- Choose location to save
- Open CSV in Excel for further analysis

## Typical Performance Metrics

| Tasks | VMs | Expected Improvement | Exec Time |
|-------|-----|----------------------|-----------|
| 5     | 2   | 10-30%              | 200-400ms |
| 10    | 3   | 15-40%              | 400-800ms |
| 20    | 4   | 20-50%              | 800-1500ms|
| 50    | 8   | 25-60%              | 2-3 sec   |

## CSV Export Format

```
Metric,Value
FCFS Makespan,50
GA Makespan,35
Improvement (%),30.00
Execution Time (ms),800

Task,VM
Task 0,VM 0
Task 1,VM 2
Task 2,VM 1
...
```

## Troubleshooting

### "Invalid Input!" or Input Validation Error
- Ensure task count matches number of execution times
- All values must be positive integers
- No spaces at start/end (system auto-trims)

### Slow Performance
- More tasks/VMs = longer execution
- Typical: 500-2000ms for reasonable inputs
- Close other applications to free memory

### Graph/Gantt Not Animating
- This is normal on first load
- Click Run again to see animation
- Animation speed: 70ms per frame (graph), 120ms per frame (Gantt)

### CSV Export Not Working
- Ensure you have write permission to target folder
- Try saving to Documents or Desktop
- Check for existing file name conflicts

## Tips for Best Results

1. **Start Small**: Test with 5-10 tasks first
2. **Balance Load**: More VMs ≠ always faster (need enough tasks)
3. **Read Improvement %**: Positive = GA better than FCFS (goal)
4. **Check Graph**: Should show downward trend (makespan decreasing)
5. **View Gantt**: Should show balanced distribution across VMs

## Advanced: Modifying Algorithm Parameters

Edit `src/main/algorithm/GeneticAlgorithm.java`:

```java
private final int popSize = 24;        // Population size (increase for slower, better solutions)
private final int generations = 60;    // Generations (increase for more convergence)
private final double mutationRate = 0.12;  // Mutation rate (0.1-0.2 is typical)
```

Recompile after changes.

## Advanced: Improving FCFS

Edit `src/main/algorithm/FCFS.java` to switch from best-fit to round-robin:

```java
// Current: Best-fit (assigns to least-loaded VM)
int bestVm = 0;
for (int vm = 1; vm < vmCount; vm++) {
    if (load[vm] < load[bestVm]) bestVm = vm;
}
load[bestVm] += task.executionTime;

// Alternative: Round-robin
load[i % vmCount] += task.executionTime;
```

---

**For full documentation, see MODERNIZATION_REPORT.md**

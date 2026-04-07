from pathlib import Path
path = Path(r'c:\Users\abc\Desktop\DF\CloudScheduler\src\main\gui\MainFrame.java')
content = '''package main.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;

import javax.swing.*;

import main.model.ScheduleResult;
import main.model.Task;
import main.service.SchedulerService;

import java.io.File;
import java.io.FileWriter;

public class MainFrame extends JFrame {

    private static final Color BACKGROUND = new Color(30, 30, 30);

    private final InputPanel inputPanel = new InputPanel();
    private final OutputPanel outputPanel = new OutputPanel();
    private final GraphPanel graphPanel = new GraphPanel();
    private final GanttChartPanel ganttPanel = new GanttChartPanel();
    private final SchedulerService schedulerService = new SchedulerService();

    private ScheduleResult lastResult;
    private Task[] lastTasks;

    public MainFrame() {
        setTitle("Cloud Scheduler Dashboard");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(1280, 820);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(14, 14));
        getContentPane().setBackground(BACKGROUND);

        add(buildHeader(), BorderLayout.NORTH);
        add(buildContent(), BorderLayout.CENTER);

        inputPanel.runBtn.addActionListener(e -> runSchedule());
        inputPanel.resetBtn.addActionListener(e -> resetDashboard());
        inputPanel.exportBtn.addActionListener(e -> exportCsv());

        setVisible(true);
    }

    private void runSchedule() {
        try {
            int taskCount = inputPanel.getTaskCount();
            int vmCount = inputPanel.getVmCount();
            int[] times = inputPanel.getExecutionTimes();

            Task[] tasks = new Task[taskCount];
            for (int i = 0; i < taskCount; i++) {
                tasks[i] = new Task(i, times[i]);
            }

            ScheduleResult result = schedulerService.schedule(tasks, vmCount);
            lastResult = result;
            lastTasks = tasks;

            outputPanel.updateMetrics(result.fcfsMakespan, result.gaMakespan, result.improvementPercent, result.executionMs);
            outputPanel.updateAllocation(result.bestSolution, tasks);

            graphPanel.animate(result.history);
            ganttPanel.animate(result.bestSolution, tasks, vmCount);

        } catch (IllegalArgumentException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Input Validation", JOptionPane.WARNING_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Unable to schedule tasks. Please verify input and try again.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private JComponent buildHeader() {
        JPanel header = new JPanel(new BorderLayout(6, 6));
        header.setBackground(BACKGROUND);
        header.setBorder(BorderFactory.createEmptyBorder(12, 18, 12, 18));

        JLabel title = new JLabel("Cloud Task Scheduling Dashboard");
        title.setForeground(Color.WHITE);
        title.setFont(new Font("Segoe UI", Font.BOLD, 24));

        JLabel subtitle = new JLabel("Genetic algorithm optimization, performance metrics, Gantt planning, and generation trend analysis");
        subtitle.setForeground(Color.LIGHT_GRAY);
        subtitle.setFont(new Font("Segoe UI", Font.PLAIN, 14));

        header.add(title, BorderLayout.NORTH);
        header.add(subtitle, BorderLayout.SOUTH);

        return header;
    }

    private JComponent buildContent() {
        JPanel leftPanel = new JPanel();
        leftPanel.setBackground(BACKGROUND);
        leftPanel.setLayout(new BoxLayout(leftPanel, BoxLayout.Y_AXIS));
        leftPanel.add(inputPanel);
        leftPanel.add(Box.createRigidArea(new Dimension(0, 14)));
        leftPanel.add(outputPanel);
        leftPanel.add(Box.createVerticalGlue());

        JPanel rightPanel = new JPanel(new BorderLayout(14, 14));
        rightPanel.setBackground(BACKGROUND);
        rightPanel.add(ganttPanel, BorderLayout.CENTER);
        rightPanel.add(graphPanel, BorderLayout.SOUTH);

        JSplitPane split = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, leftPanel, rightPanel);
        split.setResizeWeight(0.34);
        split.setBorder(null);
        split.setDividerSize(6);
        split.setBackground(BACKGROUND);

        return split;
    }

    private void resetDashboard() {
        inputPanel.resetFields();
        outputPanel.clear();
        graphPanel.clear();
        ganttPanel.clear();
        lastResult = null;
        lastTasks = null;
    }

    private void exportCsv() {
        if (lastResult == null || lastTasks == null) {
            JOptionPane.showMessageDialog(this, "Generate a schedule before exporting.", "Export CSV", JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        JFileChooser chooser = new JFileChooser();
        chooser.setDialogTitle("Export schedule to CSV");
        chooser.setSelectedFile(new File("cloud-task-schedule.csv"));

        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = chooser.getSelectedFile();
            try (FileWriter writer = new FileWriter(file)) {
                writer.write("Metric,Value\n");
                writer.write("FCFS Makespan," + lastResult.fcfsMakespan + "\n");
                writer.write("GA Makespan," + lastResult.gaMakespan + "\n");
                writer.write("Improvement (%)," + String.format("%.2f", lastResult.improvementPercent) + "\n");
                writer.write("Execution Time (ms)," + lastResult.executionMs + "\n\n");
                writer.write("Task,VM\n");
                for (Task task : lastTasks) {
                    writer.write("Task " + task.id + ",VM " + lastResult.bestSolution.allocation[task.id] + "\n");
                }
                JOptionPane.showMessageDialog(this, "Schedule exported to " + file.getAbsolutePath(), "Export Complete", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Unable to save CSV file.", "Export Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
'''
path.write_text(content, encoding='utf-8')
print('MainFrame rewritten')

from pathlib import Path

base = Path(r"c:\Users\abc\Desktop\DF\CloudScheduler")
files = {
    "src\\main\\gui\\MainFrame.java": '''package main.gui;

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
''',
    "src\\main\\gui\\InputPanel.java": '''package main.gui;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import java.awt.*;

public class InputPanel extends JPanel {

    public final JTextField taskField = new JTextField(4);
    public final JTextField vmField = new JTextField(4);
    public final JTextField timeField = new JTextField(28);
    public final JButton runBtn = new JButton("Run");
    public final JButton resetBtn = new JButton("Reset");
    public final JButton exportBtn = new JButton("Export CSV");

    public InputPanel() {
        setBackground(new Color(45, 45, 45));
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), "Cloud Configuration", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14), Color.WHITE));
        setLayout(new GridBagLayout());

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 10, 8, 10);
        gbc.anchor = GridBagConstraints.WEST;

        addLabel("Tasks:", 0, 0, gbc);
        addField(taskField, 1, 0, gbc);
        addLabel("VMs:", 0, 1, gbc);
        addField(vmField, 1, 1, gbc);
        addLabel("Execution Times:", 0, 2, gbc);
        addField(timeField, 1, 2, gbc);

        JPanel buttonRow = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        buttonRow.setBackground(new Color(45, 45, 45));

        styleButton(runBtn);
        styleButton(resetBtn);
        styleButton(exportBtn);

        buttonRow.add(runBtn);
        buttonRow.add(resetBtn);
        buttonRow.add(exportBtn);

        gbc.gridwidth = 2;
        gbc.gridx = 0;
        gbc.gridy = 3;
        add(buttonRow, gbc);
    }

    private void addLabel(String text, int x, int y, GridBagConstraints gbc) {
        gbc.gridx = x;
        gbc.gridy = y;
        JLabel label = new JLabel(text);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        add(label, gbc);
    }

    private void addField(JTextField field, int x, int y, GridBagConstraints gbc) {
        gbc.gridx = x;
        gbc.gridy = y;
        field.setPreferredSize(new Dimension(240, 30));
        styleField(field);
        add(field, gbc);
    }

    private void styleField(JTextField field) {
        field.setBackground(new Color(60, 60, 60));
        field.setForeground(Color.WHITE);
        field.setCaretColor(Color.WHITE);
        field.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        field.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), BorderFactory.createEmptyBorder(6, 8, 6, 8)));
    }

    private void styleButton(JButton button) {
        button.setBackground(new Color(0, 153, 255));
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Segoe UI", Font.BOLD, 13));
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));
    }

    public int getTaskCount() {
        try {
            int count = Integer.parseInt(taskField.getText().trim());
            if (count <= 0) {
                throw new IllegalArgumentException("Task count must be a positive integer.");
            }
            return count;
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("Enter a valid number of tasks.");
        }
    }

    public int getVmCount() {
        try {
            int count = Integer.parseInt(vmField.getText().trim());
            if (count <= 0) {
                throw new IllegalArgumentException("VM count must be a positive integer.");
            }
            return count;
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("Enter a valid number of VMs.");
        }
    }

    public int[] getExecutionTimes() {
        String raw = timeField.getText().trim();
        if (raw.isEmpty()) {
            throw new IllegalArgumentException("Execution times cannot be empty.");
        }

        String[] parts = raw.split(",");
        int taskCount = getTaskCount();
        if (parts.length != taskCount) {
            throw new IllegalArgumentException("Provide exactly " + taskCount + " execution times separated by commas.");
        }

        int[] times = new int[taskCount];
        for (int i = 0; i < taskCount; i++) {
            try {
                times[i] = Integer.parseInt(parts[i].trim());
                if (times[i] <= 0) {
                    throw new IllegalArgumentException("Each execution time must be a positive integer.");
                }
            } catch (NumberFormatException ex) {
                throw new IllegalArgumentException("Execution times must be integers.");
            }
        }
        return times;
    }

    public void resetFields() {
        taskField.setText("");
        vmField.setText("");
        timeField.setText("");
    }
}
''',
    "src\\main\\gui\\OutputPanel.java": '''package main.gui;

import main.model.Chromosome;
import main.model.Task;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class OutputPanel extends JPanel {

    private final JLabel fcfsValue = createMetricValueLabel("-");
    private final JLabel gaValue = createMetricValueLabel("-");
    private final JLabel improvementValue = createMetricValueLabel("-");
    private final JLabel timeValue = createMetricValueLabel("-");
    private final DefaultTableModel allocationModel = new DefaultTableModel(new String[]{"Task", "VM"}, 0) {
        @Override
        public boolean isCellEditable(int row, int column) {
            return false;
        }
    };
    private final JTable allocationTable = new JTable(allocationModel);

    public OutputPanel() {
        setBackground(new Color(45, 45, 45));
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), "Performance Metrics", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14), Color.WHITE));
        setLayout(new BorderLayout(12, 12));

        JPanel metricsPanel = new JPanel(new GridLayout(2, 2, 10, 10));
        metricsPanel.setBackground(new Color(45, 45, 45));
        metricsPanel.add(createMetricPanel("FCFS Makespan", fcfsValue));
        metricsPanel.add(createMetricPanel("GA Makespan", gaValue));
        metricsPanel.add(createMetricPanel("Improvement", improvementValue));
        metricsPanel.add(createMetricPanel("Execution Time", timeValue));

        add(metricsPanel, BorderLayout.NORTH);

        allocationTable.setFillsViewportHeight(true);
        allocationTable.setRowHeight(28);
        allocationTable.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        allocationTable.setBackground(new Color(35, 35, 35));
        allocationTable.setForeground(Color.WHITE);
        allocationTable.setGridColor(new Color(70, 70, 70));
        allocationTable.setShowGrid(true);
        allocationTable.getTableHeader().setFont(new Font("Segoe UI", Font.BOLD, 13));
        allocationTable.getTableHeader().setBackground(new Color(50, 50, 50));
        allocationTable.getTableHeader().setForeground(Color.WHITE);

        JScrollPane scrollPane = new JScrollPane(allocationTable);
        scrollPane.setBackground(new Color(45, 45, 45));
        scrollPane.setBorder(BorderFactory.createEmptyBorder(4, 4, 4, 4));
        add(scrollPane, BorderLayout.CENTER);
    }

    private JPanel createMetricPanel(String title, JLabel value) {
        JPanel panel = new JPanel(new BorderLayout(4, 4));
        panel.setBackground(new Color(40, 40, 40));
        panel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLineBorder(new Color(70, 70, 70)), BorderFactory.createEmptyBorder(10, 10, 10, 10)));

        JLabel titleLabel = new JLabel(title);
        titleLabel.setForeground(new Color(180, 180, 180));
        titleLabel.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        panel.add(titleLabel, BorderLayout.NORTH);

        panel.add(value, BorderLayout.CENTER);
        return panel;
    }

    private JLabel createMetricValueLabel(String text) {
        JLabel label = new JLabel(text);
        label.setForeground(Color.WHITE);
        label.setFont(new Font("Segoe UI", Font.BOLD, 20));
        return label;
    }

    public void updateMetrics(int fcfsMakespan, int gaMakespan, double improvementPercent, long executionMs) {
        fcfsValue.setText(String.valueOf(fcfsMakespan));
        gaValue.setText(String.valueOf(gaMakespan));
        improvementValue.setText(String.format("%.2f %%", improvementPercent));
        timeValue.setText(executionMs + " ms");
    }

    public void updateAllocation(Chromosome solution, Task[] tasks) {
        allocationModel.setRowCount(0);
        for (Task task : tasks) {
            allocationModel.addRow(new Object[]{"Task " + task.id, "VM " + solution.allocation[task.id]});
        }
    }

    public void clear() {
        fcfsValue.setText("-");
        gaValue.setText("-");
        improvementValue.setText("-");
        timeValue.setText("-");
        allocationModel.setRowCount(0);
    }
}
''',
    "src\\main\\gui\\GraphPanel.java": '''package main.gui;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.GeneralPath;
import java.util.ArrayList;
import java.util.List;

public class GraphPanel extends JPanel {

    private static final Color BACKGROUND = new Color(20, 20, 20);
    private static final Color GRID_COLOR = new Color(55, 55, 55);
    private static final Color AXIS_COLOR = new Color(180, 180, 180);
    private static final Color LINE_COLOR = new Color(0, 180, 255);

    private final List<Double> history = new ArrayList<>();
    private int currentFrame;
    private Timer animationTimer;

    public GraphPanel() {
        setPreferredSize(new Dimension(0, 250));
        setBackground(BACKGROUND);
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), "Generations vs Makespan", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14), Color.WHITE));
    }

    public void animate(List<Double> data) {
        history.clear();
        if (data != null) {
            history.addAll(data);
        }
        currentFrame = Math.min(1, history.size());

        if (animationTimer != null && animationTimer.isRunning()) {
            animationTimer.stop();
        }

        if (history.size() <= 1) {
            repaint();
            return;
        }

        animationTimer = new Timer(70, e -> {
            currentFrame++;
            repaint();
            if (currentFrame >= history.size()) {
                ((Timer) e.getSource()).stop();
            }
        });
        animationTimer.start();
    }

    public void clear() {
        if (animationTimer != null) {
            animationTimer.stop();
        }
        history.clear();
        currentFrame = 0;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        int width = getWidth();
        int height = getHeight();
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(BACKGROUND);
        g2.fillRect(0, 0, width, height);

        g2.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        g2.setColor(Color.WHITE);
        g2.drawString("Generation performance curve", 18, 22);

        if (history.size() < 2) {
            g2.drawString("Run the scheduler to see the makespan trend.", 18, 44);
            return;
        }

        int left = 56;
        int right = 24;
        int top = 34;
        int bottom = 50;
        int plotWidth = width - left - right;
        int plotHeight = height - top - bottom;

        double max = history.stream().mapToDouble(Double::doubleValue).max().orElse(1.0);
        double min = history.stream().mapToDouble(Double::doubleValue).min().orElse(0.0);
        double range = Math.max(1, max - min);

        drawGrid(g2, left, top, plotWidth, plotHeight, min, max);

        g2.setStroke(new BasicStroke(3f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g2.setColor(LINE_COLOR);
        GeneralPath path = new GeneralPath();
        int displayCount = Math.min(currentFrame, history.size());

        for (int i = 0; i < displayCount; i++) {
            double value = history.get(i);
            int x = left + (int) (plotWidth * (i / (double) (history.size() - 1)));
            int y = top + plotHeight - (int) ((value - min) / range * plotHeight);
            if (i == 0) {
                path.moveTo(x, y);
            } else {
                path.lineTo(x, y);
            }
        }
        g2.draw(path);

        for (int i = 0; i < displayCount; i++) {
            double value = history.get(i);
            int x = left + (int) (plotWidth * (i / (double) (history.size() - 1)));
            int y = top + plotHeight - (int) ((value - min) / range * plotHeight);
            g2.fillOval(x - 4, y - 4, 8, 8);
        }

        g2.setFont(new Font("Segoe UI", Font.BOLD, 12));
        g2.setColor(Color.WHITE);
        g2.drawString("Generations", left + plotWidth / 2 - 32, height - 18);

        g2.rotate(-Math.PI / 2);
        g2.drawString("Makespan", -height / 2 - 18, 18);
        g2.rotate(Math.PI / 2);

        g2.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        g2.drawString("Current generation: " + displayCount + " / " + history.size(), left, top - 10);
    }

    private void drawGrid(Graphics2D g2, int left, int top, int width, int height, double min, double max) {
        g2.setColor(GRID_COLOR);
        g2.setStroke(new BasicStroke(1f));
        for (int i = 0; i <= 10; i++) {
            int y = top + (height * i / 10);
            g2.drawLine(left, y, left + width, y);
        }
        for (int i = 0; i <= 10; i++) {
            int x = left + (width * i / 10);
            g2.drawLine(x, top, x, top + height);
        }

        g2.setColor(AXIS_COLOR);
        g2.drawRect(left, top, width, height);

        g2.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        g2.setColor(Color.LIGHT_GRAY);
        for (int i = 0; i <= 5; i++) {
            double value = max - (max - min) * (i / 5.0);
            int y = top + (height * i / 5);
            g2.drawString(String.format("%.0f", value), 10, y + 4);
        }

        for (int i = 0; i <= 5; i++) {
            int generation = i * (Math.max(1, history.size() - 1) / 5);
            int x = left + (width * i / 5);
            g2.drawString(String.valueOf(generation), x - 8, top + height + 18);
        }
    }
}
''',
    "src\\main\\gui\\GanttChartPanel.java": '''package main.gui;

import main.model.Chromosome;
import main.model.Task;

import javax.swing.*;
import java.awt.*;

public class GanttChartPanel extends JPanel {

    private static final Color BACKGROUND = new Color(25, 25, 25);
    private static final Color GRID_COLOR = new Color(55, 55, 55);
    private static final Color LABEL_COLOR = new Color(200, 200, 200);
    private static final Color[] TASK_COLORS = {
            new Color(0, 153, 255),
            new Color(0, 204, 153),
            new Color(255, 140, 0),
            new Color(155, 89, 182),
            new Color(52, 152, 219),
            new Color(46, 204, 113)
    };

    private Chromosome solution;
    private Task[] tasks;
    private int vmCount;
    private int visibleTasks;
    private Timer animationTimer;

    public GanttChartPanel() {
        setBackground(BACKGROUND);
        setPreferredSize(new Dimension(0, 340));
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), "Gantt Chart", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14), Color.WHITE));
    }

    public void animate(Chromosome solution, Task[] tasks, int vmCount) {
        this.solution = solution;
        this.tasks = tasks;
        this.vmCount = vmCount;
        this.visibleTasks = 0;

        if (animationTimer != null && animationTimer.isRunning()) {
            animationTimer.stop();
        }

        if (tasks == null || tasks.length == 0) {
            repaint();
            return;
        }

        animationTimer = new Timer(120, e -> {
            visibleTasks++;
            repaint();
            if (visibleTasks >= tasks.length) {
                ((Timer) e.getSource()).stop();
            }
        });
        animationTimer.start();
    }

    public void clear() {
        if (animationTimer != null) {
            animationTimer.stop();
        }
        solution = null;
        tasks = null;
        vmCount = 0;
        visibleTasks = 0;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(BACKGROUND);
        g2.fillRect(0, 0, getWidth(), getHeight());

        if (solution == null || tasks == null || vmCount <= 0) {
            g2.setColor(Color.WHITE);
            g2.setFont(new Font("Segoe UI", Font.PLAIN, 13));
            g2.drawString("Run the scheduler to display task allocation across VMs.", 18, 30);
            return;
        }

        int width = getWidth();
        int leftPadding = 100;
        int topPadding = 34;
        int rowHeight = 50;
        int totalTime = calculateMakespan(solution, tasks, vmCount);
        int plotWidth = Math.max(220, width - leftPadding - 40);
        double scale = plotWidth / (double) Math.max(totalTime, 1);

        g2.setFont(new Font("Segoe UI", Font.PLAIN, 12));

        for (int vm = 0; vm < vmCount; vm++) {
            int y = topPadding + vm * rowHeight;
            g2.setColor(new Color(40, 40, 40));
            g2.fillRect(leftPadding, y, plotWidth, rowHeight - 12);
            g2.setColor(GRID_COLOR);
            g2.drawLine(leftPadding, y + rowHeight - 12, leftPadding + plotWidth, y + rowHeight - 12);
            g2.setColor(LABEL_COLOR);
            g2.setFont(new Font("Segoe UI", Font.BOLD, 13));
            g2.drawString("VM " + vm, 16, y + rowHeight / 2 + 4);
        }

        int[] currentTime = new int[vmCount];
        for (int i = 0; i < Math.min(visibleTasks, tasks.length); i++) {
            int vm = solution.allocation[i];
            int duration = tasks[i].executionTime;
            int x = leftPadding + (int) (currentTime[vm] * scale);
            int y = topPadding + vm * rowHeight + 6;
            int widthRect = Math.max(4, (int) (duration * scale));
            Color taskColor = TASK_COLORS[i % TASK_COLORS.length];
            g2.setColor(taskColor);
            g2.fillRoundRect(x, y, widthRect, rowHeight - 20, 12, 12);
            g2.setColor(Color.WHITE);
            g2.setFont(new Font("Segoe UI", Font.BOLD, 12));
            g2.drawString("T" + tasks[i].id, x + 8, y + (rowHeight - 20) / 2 + 5);
            currentTime[vm] += duration;
        }

        int tickStep = Math.max(1, totalTime / 10);
        g2.setColor(GRID_COLOR);
        g2.setStroke(new BasicStroke(1f));
        for (int time = 0; time <= totalTime; time += tickStep) {
            int x = leftPadding + (int) (time * scale);
            g2.drawLine(x, topPadding, x, topPadding + vmCount * rowHeight - 12);
            g2.setColor(LABEL_COLOR);
            g2.setFont(new Font("Segoe UI", Font.PLAIN, 11));
            g2.drawString(String.valueOf(time), x - 10, topPadding + vmCount * rowHeight + 18);
            g2.setColor(GRID_COLOR);
        }

        g2.setColor(Color.WHITE);
        g2.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        g2.drawString("Time", leftPadding + plotWidth / 2 - 12, topPadding + vmCount * rowHeight + 36);
    }

    private int calculateMakespan(Chromosome solution, Task[] tasks, int vmCount) {
        int[] time = new int[vmCount];
        for (int i = 0; i < tasks.length; i++) {
            int vm = solution.allocation[i];
            if (vm >= 0 && vm < vmCount) {
                time[vm] += tasks[i].executionTime;
            }
        }
        int max = 0;
        for (int value : time) {
            if (value > max) {
                max = value;
            }
        }
        return max;
    }
}
''',
    "src\\main\\algorithm\\GeneticAlgorithm.java": '''package main.algorithm;

import main.model.Chromosome;
import main.model.Task;
import main.utils.FitnessCalculator;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class GeneticAlgorithm {

    private static final Random RANDOM = new Random();
    private final int popSize = 24;
    private final int generations = 60;
    private final double mutationRate = 0.12;
    public final List<Double> history = new ArrayList<>();

    public Chromosome run(Task[] tasks, int vmCount) {
        Chromosome[] population = new Chromosome[popSize];
        for (int i = 0; i < popSize; i++) {
            population[i] = new Chromosome(tasks.length, vmCount);
        }

        evaluatePopulation(population, tasks, vmCount);
        Chromosome elite = Selection.selectBest(population);
        history.clear();
        history.add((double) FitnessCalculator.getMakespan(elite, tasks, vmCount));

        for (int generation = 0; generation < generations; generation++) {
            Chromosome[] next = new Chromosome[popSize];
            next[0] = new Chromosome(elite);

            for (int i = 1; i < popSize; i++) {
                Chromosome parent1 = tournament(population);
                Chromosome parent2 = tournament(population);
                Chromosome child = Crossover.crossover(parent1, parent2, vmCount);
                Mutation.mutate(child, vmCount, mutationRate);
                child.fitness = FitnessCalculator.calculate(child, tasks, vmCount);
                next[i] = child;
            }

            population = next;
            Chromosome currentBest = Selection.selectBest(population);
            if (currentBest.fitness > elite.fitness) {
                elite = new Chromosome(currentBest);
            }
            history.add((double) FitnessCalculator.getMakespan(elite, tasks, vmCount));
        }

        return elite;
    }

    private void evaluatePopulation(Chromosome[] population, Task[] tasks, int vmCount) {
        for (Chromosome chromosome : population) {
            chromosome.fitness = FitnessCalculator.calculate(chromosome, tasks, vmCount);
        }
    }

    private Chromosome tournament(Chromosome[] population) {
        Chromosome best = population[RANDOM.nextInt(population.length)];
        for (int i = 0; i < 3; i++) {
            Chromosome challenger = population[RANDOM.nextInt(population.length)];
            if (challenger.fitness > best.fitness) {
                best = challenger;
            }
        }
        return best;
    }
}
''',
    "src\\main\\algorithm\\FCFS.java": '''package main.algorithm;

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
''',
    "src\\main\\service\\SchedulerService.java": '''package main.service;

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
''',
    "src\\main\\model\\Chromosome.java": '''package main.model;

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
''',
    "src\\main\\algorithm\\Crossover.java": '''package main.algorithm;

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
''',
    "src\\main\\algorithm\\Mutation.java": '''package main.algorithm;

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
''',
    "src\\main\\algorithm\\Selection.java": '''package main.algorithm;

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
''',
    "src\\main\\utils\\FitnessCalculator.java": '''package main.utils;

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
''',
    "src\\main\\model\\ScheduleResult.java": '''package main.model;

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
'''
}

for relative_path, content in files.items():
    target = base / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
print("Files rewritten successfully.")

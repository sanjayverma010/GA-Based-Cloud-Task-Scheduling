package main.gui;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;

import javax.swing.BorderFactory;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.border.TitledBorder;

import main.model.Chromosome;
import main.model.Task;

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
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)), "Gantt Chart",
                TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14), Color.WHITE));
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

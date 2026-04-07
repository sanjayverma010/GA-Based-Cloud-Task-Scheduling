package main.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridLayout;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;

import main.model.Chromosome;
import main.model.Task;

public class OutputPanel extends JPanel {

    private final JLabel fcfsValue = createMetricValueLabel("-");
    private final JLabel gaValue = createMetricValueLabel("-");
    private final JLabel improvementValue = createMetricValueLabel("-");
    private final JLabel timeValue = createMetricValueLabel("-");
    private final DefaultTableModel allocationModel = new DefaultTableModel(new String[] { "Task", "VM" }, 0) {
        @Override
        public boolean isCellEditable(int row, int column) {
            return false;
        }
    };
    private final JTable allocationTable = new JTable(allocationModel);

    public OutputPanel() {
        setBackground(new Color(45, 45, 45));
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)),
                "Performance Metrics", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14),
                Color.WHITE));
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
        panel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLineBorder(new Color(70, 70, 70)),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)));

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
            allocationModel.addRow(new Object[] { "Task " + task.id, "VM " + solution.allocation[task.id] });
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

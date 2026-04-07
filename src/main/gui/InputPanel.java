package main.gui;

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

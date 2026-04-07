package main.gui;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.GeneralPath;
import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.border.TitledBorder;

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
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(80, 80, 80)),
                "Generations vs Makespan", TitledBorder.LEADING, TitledBorder.TOP, new Font("Segoe UI", Font.BOLD, 14),
                Color.WHITE));
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

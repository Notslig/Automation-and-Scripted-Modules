import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;




public class reminder{
    public static void main(String[] args) {
        
        JFrame window = new JFrame("Scheduler");
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setSize(900,700);
        window.setLayout(new BorderLayout());

        JPanel daysPanel = new JPanel(new GridLayout(1, 7, 10, 10));
        String[] days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
      
        
        HashMap<String, List<String>> scheduleData = new HashMap<>();
        for (String d : days) scheduleData.put(d, new ArrayList<>());


        for (String day : days) {
            JButton dayBox = new JButton(day);
            dayBox.setFont(new Font("Arial", Font.BOLD, 12));
            JPanel dayButtonsAlign = new JPanel(new FlowLayout(FlowLayout.CENTER));
            dayBox.setPreferredSize(new Dimension(150,550));
            

            dayBox.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    String time = JOptionPane.showInputDialog(window, "Enter time for " + day + ":");
                    String title = JOptionPane.showInputDialog(window, "Enter title for " + day + ":");

                    if (time != null && title != null) {
                        String entry = time + " - " + title;
                        scheduleData.get(day).add(entry);

                        
                        StringBuilder display = new StringBuilder("<html><center>" + day + "<br/>");
                        for (String r : scheduleData.get(day)) {
                            display.append(r).append("<br/>");
                        }
                        display.append("</center></html>");
                        dayBox.setText(display.toString());
                    }
                }
            });
            dayButtonsAlign.add(dayBox);
            daysPanel.add(dayBox);
        }

        
        JButton exportBtn = new JButton("Export Schedule");
        exportBtn.setFont(new Font("Arial", Font.BOLD, 16));


        exportBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                JFileChooser chooser = new JFileChooser();
                chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

                int choice = chooser.showSaveDialog(window);
                if (choice == JFileChooser.APPROVE_OPTION) {
                    File dir = chooser.getSelectedFile();
                    File report = new File(dir, "Reminder.txt");

                    try (BufferedWriter writer = new BufferedWriter(new FileWriter(report))) {
                        for (String d : days) {
                            writer.newLine();
                            writer.write("=== " + d + " ===");
                            writer.newLine();
                            List<String> reminders = scheduleData.get(d);
                            if (reminders.isEmpty()) {
                                writer.write("  ");
                            } else {
                                for (String r : reminders) {
                                    writer.write("  task: " + r);
                                    writer.newLine();
                                }
                            }
                            writer.newLine();
                        }
                        JOptionPane.showMessageDialog(window, "Report saved at: " + report.getAbsolutePath());
                    } catch (IOException ex) {
                        JOptionPane.showMessageDialog(window, "Error saving file: " + ex.getMessage());
                    }
                }
            }
        });

        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        exportBtn.setPreferredSize(new Dimension(300, 80)); 
        bottomPanel.add(exportBtn);

        
        window.add(daysPanel, BorderLayout.CENTER);
        window.add(bottomPanel, BorderLayout.SOUTH);

        window.setVisible(true);
    }
}


import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class ImageScalerApp extends JFrame {

    private JLabel imageLabel;
    private BufferedImage originalImage;
    private BufferedImage scaledImage;

    public ImageScalerApp() {
        setTitle("Image Scaler");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        initUI();
    }

    private void initUI() {
        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout());

        imageLabel = new JLabel();
        mainPanel.add(new JScrollPane(imageLabel), BorderLayout.CENTER);

        JPanel controlPanel = new JPanel();
        JButton openButton = new JButton("Open Image");
        JButton scaleUpButton = new JButton("Scale Up");
        JButton scaleDownButton = new JButton("Scale Down");

        openButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                openImage();
            }
        });

        scaleUpButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                scaleImage(1.2);
            }
        });

        scaleDownButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                scaleImage(0.8);
            }
        });

        controlPanel.add(openButton);
        controlPanel.add(scaleUpButton);
        controlPanel.add(scaleDownButton);

        mainPanel.add(controlPanel, BorderLayout.SOUTH);

        add(mainPanel);
    }

    private void openImage() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showOpenDialog(this);

        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                originalImage = ImageIO.read(selectedFile);
                displayImage(originalImage);
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

    private void scaleImage(double scaleFactor) {
        if (originalImage == null) {
            return;
        }

        int newWidth = (int) (originalImage.getWidth() * scaleFactor);
        int newHeight = (int) (originalImage.getHeight() * scaleFactor);

        scaledImage = new BufferedImage(newWidth, newHeight, originalImage.getType());
        Graphics2D g2d = scaledImage.createGraphics();
        g2d.drawImage(originalImage, 0, 0, newWidth, newHeight, null);
        g2d.dispose();

        displayImage(scaledImage);
    }

    private void displayImage(BufferedImage image) {
        ImageIcon icon = new ImageIcon(image);
        imageLabel.setIcon(icon);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ImageScalerApp app = new ImageScalerApp();
            app.setVisible(true);
        });
    }
}

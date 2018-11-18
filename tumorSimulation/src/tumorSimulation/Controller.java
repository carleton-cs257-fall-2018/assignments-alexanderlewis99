/**
 * Controller.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a controller that creates a lattice.
 */


package tumorSimulation;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.shape.Rectangle;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.awt.*;
import java.util.Timer;
import java.util.TimerTask;
import javafx.embed.swing.SwingFXUtils;


public class Controller {
    final private double FRAMES_PER_SECOND = 20.0;

    @FXML private Button pauseButton;
    @FXML private Label timeLabel;
    @FXML private AnchorPane simulationView;
    @FXML private AnchorPane window;
    @FXML private AnchorPane settings;
    @FXML private Rectangle paddle;
    @FXML private Ball ball;
    private Lattice cellLattice;
    private Image cellLatticeImage;
    @FXML private ImageView cellLatticeImageView;
    private int last_simulation_view_height;
    private int last_simulation_view_width;

    private int timeCount;
    private boolean paused;
    private Timer timer;
    @FXML private Slider cctSlider;
    @FXML private Slider MaxProliferationSlider;
    @FXML private Slider MotilitySpeedSlider;
    @FXML private Slider ProbabilityOfDyingSlider;
    @FXML private Slider ProbabilityOfDaughterSlider;



    public Controller() {
        this.paused = false;
        this.timeCount = 0;
    }

    public void initialize() {
        this.createNewCellLattice();
        this.cellLatticeImage = SwingFXUtils.toFXImage(this.cellLattice, null);
        this.cellLatticeImageView.setImage(this.cellLatticeImage);
        this.startTimer();
    }

    /**
     * Creates an ArrayList of all cells
     */
    private void createNewCellLattice(){
        //imageType:3 to save memory and speed up computations
        this.cellLattice = new Lattice(300, 300, 3);
//        Graphics2D graphics = cellLattice.createGraphics();
//        graphics.setPaint ( new Color (0, 248, 0) );
//        graphics.fillRect ( 0, 0, cellLattice.getWidth(), cellLattice.getHeight() );
    }

    /**
     * Updates the cells if the cell lattice is not full
     */
    private void updateCells(){
        if (cellLattice.isFull()){
            this.timer.cancel();
            this.pauseButton.setText("Continue");
            this.paused = true;
        }
        else{
            this.cellLattice.updateCells();
        }
        this.cellLatticeImage = SwingFXUtils.toFXImage(this.cellLattice, null);
        this.cellLatticeImageView.setImage(this.cellLatticeImage);
    }

    /**
     * Updates the time label based on the current timestep (measured in 1/24 days)
     */
    private void updateTimeLabel(){
        this.timeCount++;
        if (timeCount%24==0){
            this.timeLabel.setText(String.format("Day: %d", this.timeCount/24));
        }
    }

    /**
     * Updates the size of the simulation window, the settings box, and the simulation image based on the size of the window.
     */
    private void updateWindowSizes(){
        int current_simulation_view_height = (int) this.simulationView.getHeight();
        int current_simulation_view_width = (int) this.simulationView.getWidth();
        if(this.last_simulation_view_height != current_simulation_view_height || this.last_simulation_view_width != current_simulation_view_width){
            cellLatticeImageView.setFitHeight((0.8)*current_simulation_view_height);
            this.last_simulation_view_height = current_simulation_view_height;
            //width
            this.last_simulation_view_width = current_simulation_view_width;
            cellLatticeImageView.setFitWidth((0.8)*current_simulation_view_width);
            if(cellLatticeImageView.getFitHeight() > cellLatticeImageView.getFitWidth()){
                cellLatticeImageView.setFitHeight(cellLatticeImageView.getFitWidth());
            } else {
                cellLatticeImageView.setFitWidth(cellLatticeImageView.getFitHeight());
            }
            double whitespaceWidth = current_simulation_view_width - cellLatticeImageView.getFitWidth();
            this.window.setLeftAnchor(this.cellLatticeImageView, whitespaceWidth/2);
            this.window.setRightAnchor(this.cellLatticeImageView, whitespaceWidth/2);
            this.simulationView.setTopAnchor(this.settings, cellLatticeImageView.getFitHeight());
        }
    }

    /**
     * Creates a timer to run the simulation
     */
    private void startTimer() {
        this.timer = new java.util.Timer();
        TimerTask timerTask = new TimerTask() {
            public void run() {
                Platform.runLater(new Runnable() {
                    public void run() {
                        updateCells();
                        updateWindowSizes();
                        updateTimeLabel();
                        updateTraitVector();
                    }
                });
            }
        };

        long frameTimeInMilliseconds = (long)(1000.0 / FRAMES_PER_SECOND);
        this.timer.schedule(timerTask, 0, frameTimeInMilliseconds);
    }

    public void updateTraitVector(){
        int generalCct = (int) this.cctSlider.getValue();
        int generalMotilitySpeed = (int) this.MotilitySpeedSlider.getValue();
        double stemProbabilityOfDaughterIsStem = (double) this.ProbabilityOfDaughterSlider.getValue();
        int nonstemMaxProliferation = (int) this.MaxProliferationSlider.getValue();
        double nonstemProbabilityOfDying = (double) this.ProbabilityOfDyingSlider.getValue();
        cellLattice.updateTraitVector(generalCct, generalMotilitySpeed, stemProbabilityOfDaughterIsStem, nonstemMaxProliferation, nonstemProbabilityOfDying);
    }



    /**
     * Pauses the simulation when the pause button is clicked.
     * Will reset the simulation if the simulation has finished.
     */
    public void onPauseButton(ActionEvent actionEvent) {
        if (cellLattice.isFull()){
            this.resetSimulation();
        } else {
            this.togglePauseButtonAndTimer();
        }
    }

    /**
     * Resets the simulation when the reset button is clicked
     */
    public void onResetButton(ActionEvent actionEvent) {
        this.resetSimulation();

    }

    /**
     * Sets the timeCount to 0 and generates a new cell lattice
     */
    public void resetSimulation(){
        this.pauseSimulation();
        this.timeCount = 0;
        this.createNewCellLattice();
        this.resumeSimulation();
    }

    /**
     * Pauses the the simulation if running or resumes it if paused
     */
    public void togglePauseButtonAndTimer(){
        if (this.paused) {
            this.resumeSimulation();
        } else {
            this.pauseSimulation();
        }
    }

    /**
     * Pauses the simulation and updates the text of pause button
     */
    public void pauseSimulation(){
        this.paused = true;
        this.pauseButton.setText("Continue");
        this.timer.cancel();
    }

    /**
     * Resumes the simulation and updates the text of pause button
     */
    public void resumeSimulation(){
        this.paused = false;
        this.pauseButton.setText("Pause");
        this.startTimer();
    }
}

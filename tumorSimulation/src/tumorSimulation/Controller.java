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
import javafx.scene.input.MouseEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.layout.AnchorPane;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import java.util.Timer;
import java.awt.Point;
import java.util.TimerTask;
import javafx.embed.swing.SwingFXUtils;


public class Controller implements EventHandler<MouseEvent>{
    final private double FRAMES_PER_SECOND = 20.0;

    @FXML private Button pauseButton;
    @FXML private Button resetButton;
    @FXML private Button instructionsButton;
    @FXML private Label timeLabel;
    @FXML private AnchorPane simulationView;
    @FXML private AnchorPane programWindow;
    @FXML private AnchorPane settings;
    @FXML private ImageView cellLatticeImageView;
    @FXML private Slider cctSlider;
    @FXML private Slider MaxProliferationSlider;
    @FXML private Slider MotilitySpeedSlider;
    @FXML private Slider ProbabilityOfDyingSlider;
    @FXML private Slider ProbabilityOfDaughterSlider;

    @FXML private AnchorPane instructionsView;

    private Lattice cellLattice;
    private Image cellLatticeImage;
    private int simulation_view_height_last_timestep;
    private int simulation_view_width_last_timestep;
    private int timeCount;
    private boolean paused;
    private Timer timer;

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

    private void createNewCellLattice(){
        this.cellLattice = new Lattice(300, 300, 3);
    }

    private void startTimer() {
        this.timer = new java.util.Timer();
        TimerTask timerTask = new TimerTask() {
            public void run() {
                Platform.runLater(new Runnable() {
                    public void run() {
                        updateLattice();
                        updateSimulationGraphics();
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

    private void updateLattice(){
        if (cellLattice.isDone()){
            pauseSimulation();
        }
        else{
            this.cellLattice.updateSimulation();
        }
    }

    private void updateSimulationGraphics(){
        this.cellLatticeImage = SwingFXUtils.toFXImage(this.cellLattice, null);
        this.cellLatticeImageView.setImage(this.cellLatticeImage);
    }

    private void updateTimeLabel(){
        this.timeCount++;
        if (timeCount%24==0){
            this.timeLabel.setText(String.format("Day: %d", this.timeCount/24));
        }
    }

    /**
     * Updates the size of the simulation window, the settings box, and the simulation image based on the size of the program window.
     */
    private void updateWindowSizes(){
        int current_simulation_view_height = (int) this.simulationView.getHeight();
        int current_simulation_view_width = (int) this.simulationView.getWidth();
        if(this.simulation_view_height_last_timestep != current_simulation_view_height || this.simulation_view_width_last_timestep != current_simulation_view_width){
            this.updateImageViewHeightAndWidth(current_simulation_view_height, current_simulation_view_width);
            this.updateImageViewPosition(current_simulation_view_width);
        }
    }

    private void updateImageViewHeightAndWidth(int current_simulation_view_height, int current_simulation_view_width){
        this.cellLatticeImageView.setFitHeight((0.75)*current_simulation_view_height);
        this.simulation_view_height_last_timestep = current_simulation_view_height;
        this.simulation_view_width_last_timestep = current_simulation_view_width;
        this.cellLatticeImageView.setFitWidth((0.75)*current_simulation_view_width);
        if(cellLatticeImageView.getFitHeight() > cellLatticeImageView.getFitWidth()){
            this.cellLatticeImageView.setFitHeight(cellLatticeImageView.getFitWidth());
        } else {
            this.cellLatticeImageView.setFitWidth(cellLatticeImageView.getFitHeight());
        }
    }

    private void updateImageViewPosition(int current_simulation_view_width){
        double whitespaceWidth = current_simulation_view_width - cellLatticeImageView.getFitWidth();
        this.programWindow.setLeftAnchor(this.cellLatticeImageView, whitespaceWidth/2);
        this.programWindow.setRightAnchor(this.cellLatticeImageView, whitespaceWidth/2);
        this.simulationView.setTopAnchor(this.settings, this.cellLatticeImageView.getFitHeight());
    }

    /**
     * Updates the TraitVector for cells in the lattice:
     *         cell cycle time
     *         motility speed
     *         probability that a daughter of a stem cell is also a stem cell
     *         max proliferation of non-stem cells
     *         probability of each non-stem cell dying each time-step
     */
    public void updateTraitVector(){
        int generalCct = 24 - (int) this.cctSlider.getValue() + 1;
        int generalMotilitySpeed = (int) this.MotilitySpeedSlider.getValue();
        double stemProbabilityOfDaughterIsStem = this.ProbabilityOfDaughterSlider.getValue();
        int nonStemMaxProliferation = (int) this.MaxProliferationSlider.getValue();
        double nonStemProbabilityOfDying = this.ProbabilityOfDyingSlider.getValue();
        this.cellLattice.updateCellTraits(generalCct, generalMotilitySpeed, stemProbabilityOfDaughterIsStem,
                nonStemMaxProliferation, nonStemProbabilityOfDying);
    }

    public void onPauseButton(ActionEvent actionEvent) {
        if (this.cellLattice.isDone()){
            this.resetSimulation();
        } else {
            this.togglePauseButtonAndTimer();
        }
    }

    public void onResetSlidersButton(ActionEvent actionEvent) {
        this.cctSlider.setValue(1);
        this.MotilitySpeedSlider.setValue(5);
        this.ProbabilityOfDaughterSlider.setValue(0.1);
        this.MaxProliferationSlider.setValue(10);
        this.ProbabilityOfDyingSlider.setValue(0.01);
    }

    public void onResetButton(ActionEvent actionEvent) {
        this.resetSimulation();
    }

    public void onInstructionsButton(ActionEvent actionEvent) {
        if (this.paused) {
            this.resumeSimulation();
            this.instructionsButton.setText("Instructions");
        } else {
            this.pauseSimulation();
            this.instructionsButton.setText("Return to simulation");
        }
        this.simulationView.setVisible(!(this.simulationView.isVisible()));
        this.instructionsView.setVisible(!(this.instructionsView.isVisible()));
        this.pauseButton.setVisible(!(this.pauseButton.isVisible()));
        this.resetButton.setVisible(!(this.resetButton.isVisible()));
        this.timeLabel.setVisible(!(this.timeLabel.isVisible()));

    }

    @Override
    public void handle(MouseEvent mouseEvent)
    {
        double mouseClickX = mouseEvent.getX();
        double mouseClickY = mouseEvent.getY();
        double imageViewWidth = this.cellLatticeImageView.getFitHeight();
        double imageViewHeight = this.cellLatticeImageView.getFitHeight();
        double aboveBound = 60;
        double belowBound = aboveBound + imageViewHeight ;
        double leftBound = (this.simulationView.getWidth() - imageViewWidth)/2;
        double rightBound = leftBound + imageViewWidth;

        if(mouseClickX > leftBound && mouseClickX < rightBound
                && mouseClickY > aboveBound && mouseClickY < belowBound){

            int x = (int) ((mouseClickX - leftBound) * (300/imageViewWidth));
            int y = (int) ((mouseClickY - aboveBound) * (300/imageViewHeight));
            this.cellLattice.addStemCellFromClick(new Point(x, y));
            System.out.println("X: " + String.valueOf(x));
            System.out.println("Y: " + String.valueOf(y));
        }
//        System.out.println("MOUSE X: " + String.valueOf(mouseClickX));
//        System.out.println("MOUSE Y: " + String.valueOf(mouseClickY));
        System.out.println("aboveBound" + String.valueOf(aboveBound));
//        System.out.println("belowBound" + String.valueOf(belowBound));
        System.out.println("leftBound" + String.valueOf(leftBound));
//        System.out.println("rightBound" + String.valueOf(rightBound));
        mouseEvent.consume();
    }

    public void resetSimulation(){
        this.pauseSimulation();
        this.timeCount = 0;
        this.createNewCellLattice();
        this.resumeSimulation();
    }

    public void togglePauseButtonAndTimer(){
        if (this.paused) {
            this.resumeSimulation();
        } else {
            this.pauseSimulation();
        }
    }

    public void pauseSimulation(){
        this.paused = true;
        this.pauseButton.setText("Continue");
        this.timer.cancel();
    }

    public void resumeSimulation(){
        this.paused = false;
        this.pauseButton.setText("Pause");
        this.startTimer();
    }
}

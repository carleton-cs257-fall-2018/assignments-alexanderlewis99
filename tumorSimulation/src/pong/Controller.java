/**

@author Alec Wang
@author Bat-Orgil Batjargal
*/


package pong;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.shape.Rectangle;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Dictionary;
import java.util.Timer;
import java.util.TimerTask;
import java.awt.Point;
import java.util.HashMap;
import java.util.Map;


public class Controller implements EventHandler<KeyEvent> {
    final private double FRAMES_PER_SECOND = 20.0;

    @FXML private Button pauseButton;
    @FXML private Label scoreLabel;
    @FXML private AnchorPane gameBoard;
    @FXML private Rectangle paddle;
    @FXML private Ball ball;
    private ArrayList<ArrayList> cellArray = new ArrayList<ArrayList>();




    private int score;
    private boolean paused;
    private Timer timer;

    public Controller() {
        this.paused = false;
        this.score = 0;
    }

    public void initialize() {
        this.createCellArray();
        this.startTimer();
    }

    /**
     * Creates an ArrayList of all cells
     */
    private void createCellArray(){
        for (double i = 0; i < 5; i++){
            ArrayList<Cell> innerCellArray = new ArrayList<Cell>();
            for (double j = 0; j < 5; j++){
                innerCellArray.add(new Cell());
            }
            this.cellArray.add(innerCellArray);
        }

        ArrayList middle_array = this.cellArray.get(3);

        Cell middle_cell = new Cell();
        middle_cell.setCellType("stem");
        middle_array.set(3, middle_cell);
        this.cellArray.set(3, middle_array);
        //ArrayList<Point> avalaible_coords = new ArrayList<Point>();
        //avalaible_coords = this.getAvailableCoordinates(new Point(0, 4), this.cellArray);


        /*
        Foreach cell:
            tell it live: it returns its behavior for that timestep
            If it divides, add the neighbor to a list of cells to become stem cells or
                            add the neighbor to a list of cells to become non-stem cells or
            If it divides, dictionary the cell and its neighbor  it will become
        */

    }

    /**
     * Iterates through the cellArray, receives the behavior of each cell, and acts upon it.
     */
    private void updateCells(){
        for(int y = 0; y < this.cellArray.size(); y++){
            ArrayList<Cell> row = this.cellArray.get(y);
            for(int x = 0; x < row.size(); x++) {
                Cell cell = row.get(x);
                Point cell_coords = new Point(x, y);
                if (cell.getCellType() == "stem" || cell.getCellType() == "non-stem"){
                    Map<String, Boolean> behavior = cell.live();
                    if(behavior.get("Divide")){
                        divideCell(cell_coords);
                    }
                    if(behavior.get("Migrate")){
                        migrateCell(cell_coords);
                    }
                    if(behavior.get("Die")){
                        cell.setCellType("dead");
                    }
                }
            }
        }
    }

    /** Divides a cell by finding an empty neighbor to become a daughter cell
     * @param cell_coords - the coordinates of the cell to divide
     * @return the coordinates of the new daughter cell
     */
    private Point divideCell(Point cell_coords){
        return new Point(0,0);
    }

    /** Divides a cell by finding an empty neighbor for the cell to become
     * @param cell_coords - the coordinates of the cell to migrate
     * @return the new coordinates of the cell
     */
    private Point migrateCell(Point cell_coords){
        return new Point(0,0);

    }

    /** Gets coordinates of available (empty/dead) adjacent squares to a given cell
     * @param cell_coords the coordinates of the cell to find available squares adjacent to
     * @param cellArray the ArrayList of all cells
     * @return coordinates of available adjacent squares
     */
    private ArrayList<Point> getAvailableCoordinates(Point cell_coords, ArrayList<ArrayList> cellArray){
        ArrayList<Point> all_eight_neighbors = this.getPotentialNeighborsCoords(cell_coords);
        int numRows = cellArray.size();
        int numColumns = cellArray.get(0).size();
        ArrayList<Point> neighbors = this.removeNeighborsOutOfBounds(all_eight_neighbors, numRows, numColumns);
        ArrayList<Point> available_squares = this.removeLivingCells(neighbors, cellArray);
        return available_squares;
    }

    /** Removes coordinates of stem or non-stem cell
     * @param neighbors - ArrayList of neighbor coordinates in bounds of lattice
     * @param cellArray - ArrayList of all cells
     * @return neighbors - an ArrayList of coordinates of empty/dead neighbors
     */
    private ArrayList<Point> removeLivingCells(ArrayList<Point> neighbors, ArrayList<ArrayList> cellArray){
        for (Point neighbor_coords: neighbors){
            int row_number = (int) neighbor_coords.getY();
            int col_number = (int) neighbor_coords.getX();
            ArrayList<Cell> cellArrayRow = cellArray.get(row_number);
            Cell cell = cellArrayRow.get(col_number);
            if (cell.getCellType().equals("stem") || cell.getCellType().equals("non-stem")){
                neighbors.remove(neighbor_coords);
            }
        }
        return neighbors;
    }

    /** Generate possible 8 neighbors coordinates
     * @param cell_coords - coordinates of the dividing/migrating cell
     * @return an ArrayList of all adjacent, including ones outside the bounds of the lattice
     */

    private ArrayList<Point> getPotentialNeighborsCoords(Point cell_coords){
        int x = (int) cell_coords.getX();
        int y = (int) cell_coords.getY();
        ArrayList<Point> all_eight_neighbors = new ArrayList<Point>();
        for (int i = -1; i <= 1; i++){
            for (int j = -1; j <= 1; j++){
                if (!(i == 0 && j == 0)){
                    Point point = new Point(x + i, y + j);
                    all_eight_neighbors.add(point);
                }
            }
        }
        return all_eight_neighbors;
    }

    /** Removes generated imposible coordinates
     * @param neighbors - an ArrayList of Points
     * @param numRows - number of rows in grid of cells
     * @param numColumns - number of columns in grid of cells
     * @return an ArrayList of Points
     */
    private ArrayList<Point> removeNeighborsOutOfBounds(ArrayList<Point> neighbors, int numRows, int numColumns){
        System.out.println("i" + String.valueOf(neighbors.size()));
        ArrayList<Point> neighbors_to_remove = new ArrayList<Point>();
        for (Point coordinate: neighbors) {
            int x = (int) coordinate.getX();
            int y = (int) coordinate.getY();
            if (x < 0 || x >= numColumns || y < 0 || y >= numRows){
                neighbors_to_remove.add(coordinate);
            }
        }
        for (Point neighbor_out_of_bounds: neighbors_to_remove){
            neighbors.remove(neighbor_out_of_bounds);
        }
        return neighbors;
    }

    private void startTimer() {
        this.timer = new java.util.Timer();
        TimerTask timerTask = new TimerTask() {
            public void run() {
                Platform.runLater(new Runnable() {
                    public void run() {
                        updateAnimation();
                        //updateCells();
                    }
                });
            }
        };

        long frameTimeInMilliseconds = (long)(1000.0 / FRAMES_PER_SECOND);
        this.timer.schedule(timerTask, 0, frameTimeInMilliseconds);
    }

    /**
     * Old method from Pong
     */
    private void updateAnimation() {
        double ballCenterX = this.ball.getCenterX() + this.ball.getLayoutX();
        double ballCenterY = this.ball.getCenterY() + this.ball.getLayoutY();
        double ballRadius = this.ball.getRadius();
        double paddleTop = this.paddle.getY() + this.paddle.getLayoutY();
        double paddleLeft = this.paddle.getX() + this.paddle.getLayoutX();
        double paddleRight = paddleLeft + this.paddle.getWidth();

        // Bounce off paddle. NOTE: THIS IS A BAD BOUNCING ALGORITHM. The ball can badly
        // overshoot the paddle and still "bounce" off it. See if you can come up with
        // something better.
        if (ballCenterX >= paddleLeft && ballCenterX < paddleRight && this.ball.getVelocityY() > 0) {
            double ballBottom = ballCenterY + ballRadius;
            if (ballBottom >= paddleTop) {
                this.ball.setVelocityY(-this.ball.getVelocityY());
                this.score++;
                this.scoreLabel.setText(String.format("Bounces: %d", this.score));
            }
        }

        // Bounce off walls
        double ballVelocityX = this.ball.getVelocityX();
        double ballVelocityY = this.ball.getVelocityY();
        if (ballCenterX + ballRadius >= this.gameBoard.getWidth() && ballVelocityX > 0) {
            this.ball.setVelocityX(-ballVelocityX);
        } else if (ballCenterX - ballRadius < 0 && ballVelocityX < 0) {
            this.ball.setVelocityX(-ballVelocityX);
        } else if (ballCenterY + ballRadius >= this.gameBoard.getHeight() && ballVelocityY > 0) {
            this.ball.setVelocityY(-ballVelocityY);
        } else if (ballCenterY - ballRadius < 0 && ballVelocityY < 0) {
            this.ball.setVelocityY(-ballVelocityY);
        }

        // Move the sprite.
        this.ball.step();
    }

    /**
     * Old method from pong
     * @param keyEvent
     */
    @Override
    public void handle(KeyEvent keyEvent) {
        KeyCode code = keyEvent.getCode();
        double paddlePosition = this.paddle.getLayoutX();
        double stepSize = 15.0;
        if (code == KeyCode.LEFT || code == KeyCode.A) {
            // move paddle left
            if (paddlePosition > stepSize) {
                this.paddle.setLayoutX(this.paddle.getLayoutX() - stepSize);
            } else {
                this.paddle.setLayoutX(0);
            }
            keyEvent.consume();
        } else if (code == KeyCode.RIGHT || code == KeyCode.D) {
            // move paddle right
            if (paddlePosition + this.paddle.getWidth() + stepSize < this.gameBoard.getWidth()) {
                this.paddle.setLayoutX(this.paddle.getLayoutX() + stepSize);
            } else {
                this.paddle.setLayoutX(this.gameBoard.getWidth() - this.paddle.getWidth());
            }
            keyEvent.consume();
        }
    }

    /**
     * Old method from pong that toggles the pause button
     */
    public void onPauseButton(ActionEvent actionEvent) {
        if (this.paused) {
            this.pauseButton.setText("Pause");
            this.startTimer();
        } else {
            this.pauseButton.setText("Continue");
            this.timer.cancel();
        }
        this.paused = !this.paused;
    }
}

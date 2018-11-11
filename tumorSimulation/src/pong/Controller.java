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

    public void createCellArray(){
        for (double i = 0; i < 5; i++){
            ArrayList<Cell> innerCellArray = new ArrayList<Cell>();
            for (double j = 0; j < 5; j++){
                innerCellArray.add(new Cell());
            }
            this.cellArray.add(innerCellArray);
        }

        ArrayList middle_array = this.cellArray.get(3);

        Cell middle_cell = new Cell();
        middle_cell.updateCellType("stem");
        middle_array.set(3, middle_cell);
        cellArray.set(3, middle_array);
    }

    public ArrayList<Point> getNeighbors(Point cell_coords){
        int x = (int) cell_coords.getX();
        int y = (int) cell_coords.getY();
        int numRows = cellArray.size();
        int numColumns = cellArray.get(0).size();
        ArrayList<Point> possible_neighbors = new ArrayList<Point>();
        for (int i = -1; i <= 1; i++){
            for (int j = -1; j <= 1; j++){
                if (j != i){
                    possible_neighbors.add(new Point(x + i, j + i));
                }
            }
        }
        for (int i = 0; i <= possible_neighbors.size(); i++) {
            Point coordinates = possible_neighbors.get(i);
            if (coordinates.getX() < 0 || coordinates.getX() > numColumns
                        || coordinates.getY() < 0 || coordinates.getY() > numRows){
                possible_neighbors.remove(coordinates);
            }
        }
        return possible_neighbors;
    }

    public ArrayList<Point> getEmptyNeighbors(Point cell_coords, ArrayList<ArrayList> cellArray){
        ArrayList<Point> neighbors = this.getNeighbors(cell_coords);
        for (int i = 0; i <= neighbors.size(); i++){
            Point neighbor_coords = neighbors.get(i);
            ArrayList<Cell> cellArrayRow = cellArray.get((int) neighbor_coords.getY());
            Cell cell = cellArrayRow.get((int) neighbor_coords.getX());
            if (!(cell.getCellType().equals("empty") || cell.getCellType().equals("dead"))){
                neighbors.remove(neighbor_coords);
            }
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
                    }
                });
            }
        };

        long frameTimeInMilliseconds = (long)(1000.0 / FRAMES_PER_SECOND);
        this.timer.schedule(timerTask, 0, frameTimeInMilliseconds);
    }

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

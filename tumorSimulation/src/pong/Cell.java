/**
 * Ball.java
 * Jeff Ondich, 10/29/14.
 *
 * A sample subclass of Sprite for CS257.
 */

package pong;
import javafx.fxml.FXML;
import javafx.scene.shape.Rectangle;
import java.util.Random;

import javax.lang.model.type.NullType;

public class Cell extends Rectangle {
    private final double timestep = 1/24;
    private String cellType;
    private int cct; //cell cycle time (affects the rate which a cell divides)
    private int max_proliferation;    //max times the cell can divide before dying
    private double motility_speed; //migration potential (affects the rate at which a cell migrates)
    private double probability_of_dying;    //rate of spontaneous death (probability each timestep it spontaneously dies)
    private double profilerates_stem; //the probability that a new daughter cell is also a stem cell (for stem cells only)
    private double probability_of_dividing;
    private double probability_of_migrating;

    public Cell() {
        this("empty");
    }

    public Cell(String assigned_cellType) {
        this.cellType = assigned_cellType;
        this.updateCellType(this.cellType);
    }

    public void updateCellType(String cellType) {
        switch (cellType) {
            case "stem":
                this.setCellToStem();
            case "non-stem":
                this.setCellToNonStem();
            case "dead":
                this.setCellToDead();
        }
    }

    public void live() {
        if (!(this.cellType == "dead" || this.cellType == "empty")) {
            this.divideIfAble();
            this.migrateIfAble();
            this.dieIfNecessary();
        }
    }

    public String getCellType() {
        return this.cellType;
    }

    private void setCellToStem() {
        this.cct = 24;
        this.max_proliferation = -1; //proliferates infinitely
        this.probability_of_dying = 0; //immortal
        this.motility_speed = 5;
        this.profilerates_stem = 0.1;
        this.setFill(javafx.scene.paint.Color.DARKRED);
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    private void setCellToNonStem() {
        this.cct = 24; //hours
        this.max_proliferation = 10;
        this.motility_speed = 5;
        this.probability_of_dying = 0.01;
        this.profilerates_stem = 0;
        this.setFill(javafx.scene.paint.Color.RED);
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    private void setCellToDead() {
        this.cct = -1;
        this.max_proliferation = -1;
        this.motility_speed = -1;
        this.probability_of_dying = 0;
        this.profilerates_stem = -1;
        this.setFill(javafx.scene.paint.Color.BLACK);
        this.probability_of_dividing = 0;
        this.probability_of_migrating = 0;

    }

    private void updateProbabilityOfDividing() {
        this.probability_of_dividing = (double)(24/this.cct) * this.timestep;
    }

    private void updateProbabilityOfMigrating() {
        this.updateProbabilityOfDividing();
        this.probability_of_migrating = (1 - this.probability_of_dividing) * this.motility_speed  * this.timestep;
    }

    private void divideIfAble(){
        Random rand = new Random();
        if (rand.nextDouble() < this.probability_of_dividing){
            this.divide();
        }
    }

    private void migrateIfAble(){
        Random rand = new Random();
        if (rand.nextDouble() < this.probability_of_migrating){
            this.migrate();
        }
    }

    private void dieIfNecessary(){
        Random rand = new Random(); // don't we need a
        if (rand.nextDouble() < this.probability_of_dying){
            this.die();
        }
    }

    private void divide() {


    }

    private void migrate() {
    }

    private void die(){
    }

}


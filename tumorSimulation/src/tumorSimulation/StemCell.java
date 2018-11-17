/**
 * StemCell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a stem cell
 */

package tumorSimulation;

public class StemCell extends AliveCell {

    public StemCell(){
        this.setCellType("stem");
        this.setCct(24);
        this.setMaxProliferation(-1); //proliferates infinitely
        this.setProbabilityOfDying(0); //immortal
        this.setMotilitySpeed(5);
        this.setProbabilityOfDaughterStemCell(0.1);
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    /**
     * Stem cells have a 0% chance of dying
     * @return boolean - whether the cell should die
     */
    //@Override
    private boolean dieIfUnlucky(){
        return false;
    }
}
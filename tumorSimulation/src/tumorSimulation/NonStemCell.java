/**
 * NonStemCell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a non-stem cell
 */

package tumorSimulation;

public class NonStemCell extends AliveCell {

    public NonStemCell(){
        this.setCellType("non-stem");
        this.setCct(24);
        this.setMaxProliferation(10); //proliferates infinitely
        this.setMotilitySpeed(5);
        this.setProbabilityOfDying(0.01); //immortal
        this.setProbabilityOfDaughterStemCell(0);
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    /** Non-stem cells have a {0%} chance of creating a non-stem cell
     * @return the cell-type of the daughter (either stem or non-stem)
     */
    @Override
    public String getCellTypeOfNewDaughter(){
        return("non-stem");
    }

}
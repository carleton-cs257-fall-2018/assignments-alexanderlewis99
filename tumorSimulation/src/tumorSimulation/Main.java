/**
 * Main.java
 * Alec Wang and Bat-Orgil Batjargal, 11 Nov 2018
 *
 * The main program for a simulation of the growth of a tumor from a single
 * stem cell. The primary goal of this program is to demonstrate how one small
 * cell following a set of simple rules can grow at an exponential rate and
 * give rise to an enormous growth of many cells.
 */

package tumorSimulation;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class  Main extends Application {
    @Override
    public void start(Stage primaryStage) throws Exception{
        primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
            @Override
            public void handle(WindowEvent t) {
                Platform.exit();
                System.exit(0);
            }
        });
        FXMLLoader loader = new FXMLLoader(getClass().getResource("tumorSimulation.fxml"));
        Parent root = (Parent)loader.load();
        Controller controller = loader.getController();
        root.setOnMouseClicked(controller);
        primaryStage.setTitle("Tumor Simulation");
        Scene scene = new Scene(root, 700, 500);
        primaryStage.setScene(scene);
        primaryStage.show();
        root.requestFocus();
    }

    public static void main(String[] args) {
        launch(args);
    }
}

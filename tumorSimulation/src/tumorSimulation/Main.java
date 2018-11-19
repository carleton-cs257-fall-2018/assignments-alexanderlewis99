/**
 * Main.java
 * Jeff Ondich, 19 Nov 2014
 *
 * The main program for a tiny demo pong-like program in JavaFX. The goal of
 * this program is to illustrate two techniques interacting: (1) Timer-based
 * animation, and (2) keystroke handling. As a sidelight, this demo also
 * introduces AnchorPane to keep the gameboard tied to the window's boundaries,
 * and to keep the paddle tied to the bottom of the gameboard.
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

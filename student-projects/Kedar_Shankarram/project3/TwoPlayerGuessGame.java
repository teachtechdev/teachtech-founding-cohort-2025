import java.util.Scanner;

public class TwoPlayerGuessGame {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int secretNumber;
        int guess;
        int currentPlayer = 1;
        boolean gameWon = false;
        int maxTries = 8;
        int triesUsed = 0;

        System.out.println("Welcome to the 2-Player Number Guessing Game!");
        System.out.print("Player 1, please enter a secret number (1 to 100): ");
        secretNumber = scanner.nextInt();

        // Clear screen simulation
        for (int i = 0; i < 50; i++) System.out.println();

        System.out.println("Let the game begin! You have " + maxTries + " total guesses to find the number.");

        while (!gameWon && triesUsed < maxTries) {
            System.out.print("Player " + currentPlayer + ", enter your guess: ");
            guess = scanner.nextInt();
            triesUsed++;

            if (guess == secretNumber) {
                System.out.println("Congratulations Player " + currentPlayer + "! You guessed the correct number in " + triesUsed + " tries!");
                gameWon = true;
            } else if (guess < secretNumber) {
                System.out.println("Too low!");
            } else {
                System.out.println("Too high!");
            }

            // Switch players if game is not won
            if (!gameWon) {
                currentPlayer = (currentPlayer == 1) ? 2 : 1;
                System.out.println("Guesses remaining: " + (maxTries - triesUsed));
            }
        }

        if (!gameWon) {
            System.out.println("No more guesses left! The correct number was: " + secretNumber);
            System.out.println("Better luck next time!");
        }

        scanner.close();
    }
}

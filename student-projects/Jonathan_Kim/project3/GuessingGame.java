import java.util.Scanner;
public class GuessingGame {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String playAgain;

        do {
            System.out.println("Guessing Game");
            System.out.print("Enter a number between 1 and 10 (P1): ");
            int number = input.nextInt();
            System.out.print("Guess number (P2): ");
            int guess = input.nextInt();

            if (guess == number) {
                System.out.println("Correct. Player 2 is the winner.");
            } else {
                System.out.println("Incorrect. Player 1 is the winner. The number was " + number);
            }

            System.out.print("Play again? (yes/no): ");
            input.nextLine();
            playAgain = input.nextLine();
        } while (playAgain.equalsIgnoreCase("yes"));

    }
}

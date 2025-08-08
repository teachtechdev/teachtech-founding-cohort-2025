// File: BinaryBattleTimed.java
package BinaryBattle;

import java.util.Random;
import java.util.Scanner;

public class BinaryBattleTimed {
    private static final int WIN_POINTS = 5;

    private Scanner scanner;
    private Random rand;
    private int[] points;  // points[0] = Player 1’s score, points[1] = Player 2’s score

    /** Starts the game. */
    public void startGame() {
        scanner = new Scanner(System.in);
        rand     = new Random();
        points   = new int[]{0, 0};

        System.out.println("=== Welcome to Binary Battle (first to "
                + WIN_POINTS + " points wins) ===\n");

        while (points[0] < WIN_POINTS && points[1] < WIN_POINTS) {
            // Player 1’s independent puzzle
            Puzzle puzzle1 = genPuzzle();
            System.out.println("Player 1, HIT ENTER to get your puzzle and start!");
            long time1 = playTimedTurn(1, puzzle1);

            // Player 2’s independent puzzle
            Puzzle puzzle2 = genPuzzle();
            System.out.println("\nPlayer 2, HIT ENTER to get your puzzle and start!");
            long time2 = playTimedTurn(2, puzzle2);

            // compare times & award a point
            if      (time1 < time2) { points[0]++; System.out.println("→ Player 1 wins the round!"); }
            else if (time2 < time1) { points[1]++; System.out.println("→ Player 2 wins the round!"); }
            else                    { System.out.println("→ Tie—no points awarded."); }

            // display current score
            System.out.printf("Score: P1=%d   P2=%d%n%n", points[0], points[1]);
        }

        // announce overall champion
        if (points[0] == WIN_POINTS) System.out.println("🎉 Player 1 is the champion! 🎉");
        else                          System.out.println("🎉 Player 2 is the champion! 🎉");

        scanner.close();
    }

    /**
     * Waits for ENTER, shows the puzzle, times the player’s correct answer,
     * and returns elapsed time in milliseconds.
     */
    private long playTimedTurn(int player, Puzzle puzzle) {
        scanner.nextLine();  // wait for ENTER
        System.out.println("Puzzle: " + puzzle.getPrompt());

        long start = System.nanoTime();
        while (true) {
            System.out.print("Your answer: ");
            String answer = scanner.nextLine().trim();
            if (puzzle.isCorrect(answer)) {
                break;
            }
            System.out.println("Nope—try again!");
        }
        long end = System.nanoTime();

        long elapsedMs = (end - start) / 1_000_000;
        System.out.printf("Player %d time: %d ms%n", player, elapsedMs);
        return elapsedMs;
    }

    /**
     * Randomly generates either:
     *  - Decimal → 8-bit binary
     *  - 8-bit binary → Decimal
     */
    private Puzzle genPuzzle() {
        int value   = rand.nextInt(256);
        boolean d2b = rand.nextBoolean();

        // always build the 8-bit version internally
        String binStr = String.format("%8s", Integer.toBinaryString(value))
                .replace(' ', '0');

        String prompt;
        if (d2b) {
            prompt = "Convert decimal " + value + " to 8-bit binary";
        } else {
            prompt = "Convert binary " + binStr + " to decimal";
        }

        return new Puzzle(prompt, value, d2b);
    }

    /**
     * Inner class holding one round’s prompt, the numeric value behind it,
     * and the mode (true = dec→bin, false = bin→dec).
     */
    private static class Puzzle {
        private final String prompt;
        private final int    value;
        private final boolean decToBin;

        public Puzzle(String prompt, int value, boolean decToBin) {
            this.prompt   = prompt;
            this.value    = value;
            this.decToBin = decToBin;
        }

        public String getPrompt() {
            return prompt;
        }

        public boolean isCorrect(String userAnswer) {
            if (decToBin) {
                try {
                    int parsed = Integer.parseInt(userAnswer, 2);
                    return parsed == value;
                } catch (NumberFormatException e) {
                    return false;
                }
            } else {
                try {
                    int parsed = Integer.parseInt(userAnswer);
                    return parsed == value;
                } catch (NumberFormatException e) {
                    return false;
                }
            }
        }
    }
}

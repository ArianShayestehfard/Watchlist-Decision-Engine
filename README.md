<h1 align="center">🎲 Snake and Ladder Game

<p align="center">
  A desktop Snake and Ladder game built with Java and JavaFX, developed as the final project for the Advanced Programming course.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Java-007396?logo=java&logoColor=white" alt="Java">
  <img src="https://img.shields.io/badge/JavaFX-007396?logo=java&logoColor=white" alt="JavaFX">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

---

## 🎯 Overview

**Mar Va Pele** is a classic Snake and Ladder board game, played between the user (**YOU**) and the computer on a 10×10 board (100 tiles).

Rolling the dice moves your piece forward tile by tile. Landing on the bottom of a ladder sends you climbing up; landing on the head of a snake sends you sliding down. The first player to reach tile 100 wins.

---

## 🖼️ Screenshot

<p align="center">
  <img src="screenshots/snake-ladder-game-start.png" alt="Game board with snakes, ladders, and both player pieces on tile 1" width="500">
</p>

---

## ✨ Features

### 🎲 Turn-Based Gameplay

Roll the dice by clicking the on-screen button. Turns alternate automatically between **YOU** and the **COMPUTER**, which rolls on its own after a short pause.

### 🪜 Snakes & Ladders

Eight snake/ladder connections are drawn directly on the board as colored lines — yellow for snakes (moving down), light yellow for ladders (moving up) — so the board layout is visible before you even roll.

### 🎬 Animated Movement

Pieces move step by step across tiles using `PauseTransition`, rather than jumping instantly to the destination, including the extra jump when landing on a snake or ladder.

### 🏆 Win Detection

The game automatically detects when a player reaches tile 100, displays the result in the title bar, and disables further dice rolls.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| **Java** | Core game logic and state |
| **JavaFX** | UI rendering, board layout, animations |

---

## 📁 Project Structure

```text
Snake-Ladder-Game/
│
├── marVaPeleApplication.java   → JavaFX Application entry point, board & game loop
├── marVaPeleController.java    → Player state (name, color, position, board piece)
│
├── Dice/
│   ├── Num1.PNG
│   ├── Num2.PNG
│   ├── Num3.PNG
│   ├── Num4.PNG
│   ├── Num5.PNG
│   └── Num6.PNG
│
├── screenshots/
│   └── snake-ladder-game-start.png
│
└── README.md
```

---

## 🚀 Running the Project

> ⚠️ This repository currently contains raw `.java` source files with no build configuration (no Maven/Gradle project yet — see Roadmap below). To run it, set it up manually:

1. Install a JDK (11+) and download the [JavaFX SDK](https://openjfx.io/) matching your JDK version.
2. Open the project folder in an IDE that supports JavaFX (e.g. IntelliJ IDEA).
3. Add the JavaFX SDK `lib` folder as a library, and set these VM options:
   ```text
   --module-path /path/to/javafx-sdk/lib --add-modules javafx.controls,javafx.graphics
   ```
4. Run `marVaPeleApplication.java` — it contains the `main` method.

---

## 📌 Current Limitations

* No build tool (Maven/Gradle) — dependencies and compilation are manual.
* No automated tests.
* Fixed 2-player mode only (YOU vs. COMPUTER).

---

## 🗺️ Roadmap

* [ ] Add a `pom.xml` (Maven) or `build.gradle` for one-command builds
* [ ] Add unit tests for movement and snake/ladder logic
* [ ] Support more than 2 players
* [ ] Add sound effects for dice rolls and wins

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

<p align="center">
  <b>Arian Shayestehfard</b>
  <br>
  Final project for the Advanced Programming course
  <br><br>
  <a href="https://github.com/ArianShayestehfard">
    <img src="https://img.shields.io/badge/GitHub-ArianShayestehfard-181717?logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

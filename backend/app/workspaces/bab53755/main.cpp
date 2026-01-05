#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <chrono>

using namespace std;

// Définition des constantes
const int WIDTH = 20;
const int HEIGHT = 20;

// Structure pour représenter les coordonnées
struct Coordinate {
    int x;
    int y;
};

// Fonction pour générer des coordonnées aléatoires
Coordinate generateFood(const vector<Coordinate>& snake) {
    Coordinate food;
    bool validFood = false;
    while (!validFood) {
        food.x = rand() % WIDTH;
        food.y = rand() % HEIGHT;

        // Vérifier si la nourriture n'est pas sur le serpent
        validFood = true;
        for (const auto& segment : snake) {
            if (segment.x == food.x && segment.y == food.y) {
                validFood = false;
                break;
            }
        }
    }
    return food;
}

// Fonction pour afficher le jeu
void draw(const vector<Coordinate>& snake, const Coordinate& food) {
    system("clear"); // Effacer l'écran
    for (int i = 0; i < HEIGHT; ++i) {
        for (int j = 0; j < WIDTH; ++j) {
            if (i == food.y && j == food.x) {
                cout << "F"; // Afficher la nourriture
            } else {
                bool isSnakeSegment = false;
                for (const auto& segment : snake) {
                    if (segment.x == j && segment.y == i) {
                        cout << "O"; // Afficher le serpent
                        isSnakeSegment = true;
                        break;
                    }
                }
                if (!isSnakeSegment) {
                    cout << "."; // Afficher l'espace vide
                }
            }
        }
        cout << endl;
    }
}

int main() {
    // Initialisation du générateur de nombres aléatoires
    srand(time(0));

    // Initialisation du serpent
    vector<Coordinate> snake = {{WIDTH / 2, HEIGHT / 2}};

    // Initialisation de la nourriture
    Coordinate food = generateFood(snake);

    // Direction initiale du serpent
    int dx = 1, dy = 0;

    // Boucle de jeu
    while (true) {
        // Affichage du jeu
        draw(snake, food);

        // Contrôle du serpent (exemple simple : direction constante)
        // On pourrait ajouter ici une gestion de l'entrée utilisateur

        // Déplacement du serpent
        Coordinate newHead = {snake.front().x + dx, snake.front().y + dy};

        // Gestion des collisions avec les bords
        if (newHead.x < 0) newHead.x = WIDTH - 1;
        if (newHead.x >= WIDTH) newHead.x = 0;
        if (newHead.y < 0) newHead.y = HEIGHT - 1;
        if (newHead.y >= HEIGHT) newHead.y = 0;

        // Gestion de la collision avec la nourriture
        if (newHead.x == food.x && newHead.y == food.y) {
            snake.insert(snake.begin(), newHead);
            food = generateFood(snake);
        } else {
            snake.insert(snake.begin(), newHead);
            snake.pop_back();
        }

        // Gestion de la collision avec lui-même
        for (size_t i = 1; i < snake.size(); ++i) {
            if (snake[i].x == newHead.x && snake[i].y == newHead.y) {
                cout << "Game Over!" << endl;
                return 0;
            }
        }

        // Pause pour contrôler la vitesse du jeu
        this_thread::sleep_for(chrono::milliseconds(100));
    }

    return 0;
}

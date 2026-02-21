#include <iostream>
#include <chrono>
#include "cambio.h"

int main() {
    int num_games = 10000;
    int turns_per_game = 40;

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_games; i++) {
        Cambio c;
        for (int t = 0; t < turns_per_game; t++) {
            c.step();
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    double seconds = std::chrono::duration<double>(end - start).count();

    std::cout << "C++ total time: " << seconds << "s" << std::endl;
    std::cout << "Ops/sec: " << int(num_games * turns_per_game / seconds) << std::endl;

    return 0;
}

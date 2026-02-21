#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "player.h"
#include "cambio.h"

namespace py = pybind11;

PYBIND11_MODULE(cambio_cpp, m) {
    py::class_<Player>(m, "Player")
        .def(py::init<const std::vector<int>&, const std::string&>())
        .def("get_inventory", &Player::get_inventory)
        .def("set_inventory", &Player::set_inventory)
        .def("get_in_hand", &Player::get_in_hand)
        .def("set_in_hand", &Player::set_in_hand)
        .def("swap_hand_with_inventory", &Player::swap_hand_with_inventory)
        .def("get_name", &Player::get_name)
        .def("get_score", &Player::get_score)
        .def("get_card_score", &Player::get_card_score)
        .def("get_risk_tolerance", &Player::get_risk_tolerance)
        .def("set_risk_tolerance", &Player::set_risk_tolerance)
        .def("decide_swap_index", &Player::decide_swap_index)
        .def_readonly_static("RED_KING_DIAMOND", &Player::RED_KING_DIAMOND)
        .def_readonly_static("RED_KING_HEART", &Player::RED_KING_HEART);

    py::class_<Cambio>(m, "Cambio")
        .def(py::init<>())
        .def("get_deck", &Cambio::get_deck)
        .def("get_player", &Cambio::get_player)
        .def("get_discard_pile", &Cambio::get_discard_pile)
        .def("get_turn_count", &Cambio::get_turn_count)
        .def("get_game_over", &Cambio::get_game_over)
        .def("get_winner", &Cambio::get_winner)
        .def("convert_card", &Cambio::convert_card)
        .def("get_card_score", &Cambio::get_card_score)
        .def("discard", &Cambio::discard)
        .def("discard_card_from_hand", &Cambio::discard_card_from_hand)
        .def("player_get_card_from_pile", &Cambio::player_get_card_from_pile)
        .def("player_put_card_in_hand_into_deck", &Cambio::player_put_card_in_hand_into_deck)
        .def("step", &Cambio::step)
        .def("turn_deck_to_name", &Cambio::turn_deck_to_name)
        .def("turn_deck_to_score", &Cambio::turn_deck_to_score)
        .def_readonly_static("RED_KING_DIAMOND", &Cambio::RED_KING_DIAMOND)
        .def_readonly_static("RED_KING_HEART", &Cambio::RED_KING_HEART)
        .def_readonly_static("JOKER_1", &Cambio::JOKER_1)
        .def_readonly_static("JOKER_2", &Cambio::JOKER_2)
        .def_readonly_static("DECK_SIZE", &Cambio::DECK_SIZE);
}

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "player.h"

namespace py = pybind11;

PYBIND11_MODULE(player_cpp, m) {
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
}

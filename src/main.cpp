#include <pybind11/pybind11.h>

#include "NaoRobot.h"

namespace py = pybind11;

PYBIND11_MODULE(_nao_bindings, m) {
    m.doc() = "Example NAO lib using libqi";

    py::class_<NaoRobot>(m, "Nao")
        .def(py::init<const std::string&, int, bool>(), py::arg("ip"), py::arg("port")=9559, py::arg("dummy")=false)
		.def_readwrite("speech", &NaoRobot::speech);

	py::class_<Speech>(m, "Speech")
		.def("say", &Speech::say)
		.def("setVolume", &Speech::setVolume)
		.def("getVolume", &Speech::getVolume);
}

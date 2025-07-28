#include <pybind11/pybind11.h>

#include "proxy.h"
#include "robot.h"

namespace py = pybind11;

std::string ping() {
    return "Hello c++!";
}

std::string ping2() {
    return "Hello c++! electric boogaloo";
}


PYBIND11_MODULE(_nao_bindings, m) {
    m.doc() = "Example NAO lib using libqi";

    m.def("ping", &ping);
    m.def("ping2", &ping2);

    py::class_<Robot>(m, "Robot")
        .def(py::init<const std::string&, int>(), py::arg("ip"), py::arg("port") = 9559)
        .def("get_service", &Robot::getService);

    py::class_<Proxy>(m, "Proxy")
        .def(py::init<Robot*, const std::string&>(), py::arg("robot"), py::arg("name"));
}

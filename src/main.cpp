#include <pybind11/pybind11.h>

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
}

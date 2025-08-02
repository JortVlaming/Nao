#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_nao_bindings, m) {
    m.doc() = "Example NAO lib using libqi";
}

#include "py_submodules.h"

//#include "../qed/photon.h"
//#include "../qed/tile.h"

#include "../qed/interactions/interaction.h"
#include "../qed/interactions/pair_ann.h"



namespace qed {

  using std::string;

//--------------------------------------------------
//template<size_t D>
//auto declare_tile(
//    py::module& m,
//    const std::string& pyclass_name) 
//{
//
//  return 
//  py::class_<qed::Tile<D>,
//             pic::Tile<D>, 
//             fields::Tile<D>,
//             corgi::Tile<D>, 
//             std::shared_ptr<qed::Tile<D>>
//             >(m, 
//               pyclass_name.c_str(),
//               py::multiple_inheritance()
//               )
//    .def(py::init<int, int, int>())
//    .def("get_bucket",       &qed::Tile<D>::get_bucket, 
//        py::return_value_policy::reference)
//    .def("push_back",       &qed::Tile<D>::push_back);
//}

/// trampoline class for Interactions 
class PyInteraction : public Interaction
{
public:


  using Interaction::Interaction;


  // trampoline for each  virtual function
 
  using tuple_pair = std::tuple<double, double>; // following macro does not accept commas so we define this

  tuple_pair get_minmax_ene( string t1, string t2 ) override { 
    PYBIND11_OVERLOAD_PURE(
        tuple_pair, // return type
        Interaction,                // parent class
        get_minmax_ene,             // name of function in C++
        t1, // arguments
        t2  
        );
  }

  double comp_cross_section( 
    string t1, double ux1, double uy1, double uz1,
    string t2, double ux2, double uy2, double uz2) override {
    PYBIND11_OVERLOAD_PURE(
        double,                     // return type
        Interaction,                // parent class
        comp_cross_section,         // name of function in C++
        t1, ux1, uy1, uz1, t2, ux2, uy2, uz2
        );
  }

  //std::tuple<
  //  string, double, double, double,
  //  string, double, double, double>
  //    interact(
  //      string t1, double ux1, double uy1, double uz1,
  //      string t2, double ux2, double uy2, double uz2) override {
  //  PYBIND11_OVERLOAD_PURE(
  //      std::tuple<string, double, double, double, string, double, double, double>, // return type
  //      Interaction,                // parent class
  //      interact,                   // name of function in C++
  //      string, // arguments
  //      double, double, double,
  //      string,
  //      double, double, double
  //      );
  //  }

  void interact(
        string& t1, double& ux1, double& uy1, double& uz1,
        string& t2, double& ux2, double& uy2, double& uz2) override {
    PYBIND11_OVERLOAD_PURE(
        void,                       // return type
        Interaction,                // parent class
        interact,                   // name of function in C++
        t1, ux1, uy1, uz1, t2, ux2, uy2, uz2
        );
    }

};


//--------------------------------------------------

// python bindings for radiation classes & functions
void bind_qed(py::module& m_sub)
{

  //py::class_<qed::PhotonContainer, pic::ParticleContainer<3>>(m_sub, "PhotonContainer")
  //  .def(py::init<>())
  //  .def("add_particle",  (void (qed::PhotonContainer::*)
  //        ( std::vector<float_p>, std::vector<float_p>, float_p, float_p ) ) 
  //          &qed::PhotonContainer::add_particle)
  //  .def("ene", [](qed::PhotonContainer& s) {return s.eneArr;}, py::return_value_policy::reference)
  //  // FIXME: use base class definition via getter/setter members to avoid this redefinition
  //  .def("loc",          [](qed::PhotonContainer& s, size_t idim) 
  //      {
  //        return s.loc(idim); 
  //      }, py::return_value_policy::reference)
  //  .def("vel",          [](qed::PhotonContainer& s, size_t idim) 
  //      {
  //        return s.vel(idim); 
  //      }, py::return_value_policy::reference);


  // 2D bindings
  //py::module m_2d = m_sub.def_submodule("twoD", "2D specializations");
  //auto t2 = qed::declare_tile<2>(m_2d, "Tile");



  py::class_< qed::Interaction, PyInteraction > qedinter(m_sub, "Interaction");
  qedinter
    //.def(py::init<string&, string& >())
    .def(py::init<string, string>())
    //.def("get_ene",      &qed::Interaction::get_ene);
    .def("get_minmax_ene",      &qed::Interaction::get_minmax_ene)
    .def("comp_cross_section",  &qed::Interaction::comp_cross_section)
    //.def("interact",            &qed::Interaction::interact);
    .def("interact", [](qed::Interaction &self, 
          std::string t1, double ux1, double uy1, double uz1,
          std::string t2, double ux2, double uy2, double uz2) 
        {
          self.interact(t1, ux1, uy1, uz1,  t2, ux2, uy2, uz2); 
          return std::make_tuple(t1, ux1, uy1, uz1,  t2, ux2, uy2, uz2);
        });

  // Pair annihilation 
  py::class_<qed::PairAnn>(m_sub, "PairAnn", qedinter)
    //.def(py::init<string&, string& >());
    .def(py::init<string, string>());



}




} // ns qed

// Copyright 2018 Global Phasing Ltd.
//
// Monomer library - (Refmac) restraints dictionary,
// which is made of monomers (chemical components), links and modifications.

#ifndef GEMMI_MONLIB_HPP_
#define GEMMI_MONLIB_HPP_

#include <cassert>
#include <cctype>  // for tolower
#include <map>
#include <string>
#include <vector>
#include "cifdoc.hpp"
#include "elem.hpp"  // for Element
#include "numb.hpp"  // for as_number
#include "util.hpp"  // for fail
#include "model.hpp" // for Residue, Atom
#include "chemcomp.hpp" // for ChemComp
#include "resinfo.hpp" // for ChemComp

namespace gemmi {

struct ChemLink {
  enum class Group {
    // _chem_link.group_comp_N is one of:
    // "peptide", "pyranose", "DNA/RNA" or null (we ignore "polymer")
    Peptide, Pyranose, DnaRna, Null
  };
  struct Side {
    std::string comp;
    std::string mod;
    Group group;
  };
  std::string id;
  std::string name;
  Side side1;
  Side side2;
  Restraints rt;

  static Group read_group(const std::string& str) {
    if (str.size() >= 4) {
      const char* cstr = str.c_str();
      if ((str[0] == '\'' || str[0] == '"') && str.size() >= 6)
        ++cstr;
      switch (ialpha4_id(cstr)) {
        case ialpha4_id("pept"): return Group::Peptide;
        case ialpha4_id("pyra"): return Group::Pyranose;
        case ialpha4_id("dna/"): return Group::DnaRna;
      }
    }
    return Group::Null;
  }

  static const char* group_str(Group g) {
    switch (g) {
      case Group::Peptide: return "peptide";
      case Group::Pyranose: return "pyranose";
      case Group::DnaRna: return "DNA/RNA";
      case Group::Null: return ".";
    }
    unreachable();
  }
};

struct ChemMod {
  struct AtomMod {
    int func;
    std::string old_id;
    std::string new_id;
    Element el;
    float charge;
    std::string chem_type;
  };

  std::string id;
  std::string name;
  std::string comp_id;
  std::string group_id;
  std::vector<AtomMod> atom_mods;
  Restraints rt;

  void apply_to(ChemComp& cc) const;
};


inline Restraints read_link_restraints(const cif::Block& block_) {
  auto read_aid = [](cif::Table::Row& row, int n) {
    return Restraints::AtomId{cif::as_int(row[n]), row.str(n+1)};
  };
  Restraints rt;
  cif::Block& block = const_cast<cif::Block&>(block_);
  for (auto row : block.find("_chem_link_bond.",
                             {"atom_1_comp_id", "atom_id_1",
                              "atom_2_comp_id", "atom_id_2",
                              "type",
                              "value_dist", "value_dist_esd"}))
    rt.bonds.push_back({read_aid(row, 0), read_aid(row, 2),
                        bond_type_from_string(row[4]), false,
                        cif::as_number(row[5]), cif::as_number(row[6])});
  for (auto row : block.find("_chem_link_angle.",
                             {"atom_1_comp_id", "atom_id_1",
                              "atom_2_comp_id", "atom_id_2",
                              "atom_3_comp_id", "atom_id_3",
                              "value_angle", "value_angle_esd"}))
    rt.angles.push_back({read_aid(row, 0), read_aid(row, 2), read_aid(row, 4),
                         cif::as_number(row[6]), cif::as_number(row[7])});
  for (auto row : block.find("_chem_link_tor.",
                             {"id",
                              "atom_1_comp_id", "atom_id_1",
                              "atom_2_comp_id", "atom_id_2",
                              "atom_3_comp_id", "atom_id_3",
                              "atom_4_comp_id", "atom_id_4",
                              "value_angle", "value_angle_esd",
                              "period"}))
    rt.torsions.push_back({row.str(0),
                           read_aid(row, 1), read_aid(row, 3),
                           read_aid(row, 5), read_aid(row, 7),
                           cif::as_number(row[9]), cif::as_number(row[10]),
                           cif::as_int(row[11])});
  for (auto row : block.find("_chem_link_chir.",
                             {"atom_centre_comp_id", "atom_id_centre",
                              "atom_1_comp_id", "atom_id_1",
                              "atom_2_comp_id", "atom_id_2",
                              "atom_3_comp_id", "atom_id_3",
                              "volume_sign"}))
    if (row[4][0] != 'c') // ignore crossN
      rt.chirs.push_back({read_aid(row, 0), read_aid(row, 2),
                          read_aid(row, 4), read_aid(row, 6),
                          chirality_from_string(row[8])});
  for (auto row : block.find("_chem_link_plane.",
                             {"plane_id", "atom_comp_id", "atom_id",
                              "dist_esd"})) {
    Restraints::Plane& plane = rt.get_or_add_plane(row.str(0));
    if (plane.esd == 0.0)
      plane.esd = cif::as_number(row[3]);
    plane.ids.push_back(read_aid(row, 1));
  }
  return rt;
}

inline ResidueInfo::Kind chemcomp_group_to_kind(const std::string& group) {
  if (group.size() >= 3) {
    const char* str = group.c_str();
    if (group.size() > 4 && (*str == '"' || *str == '\''))
      ++str;
    switch (ialpha4_id(str)) {
      case ialpha4_id("non-"): return ResidueInfo::ELS;
      case ialpha4_id("pept"): return ResidueInfo::AA;
      case ialpha4_id("dna"): return ResidueInfo::DNA;
      case ialpha4_id("rna"): return ResidueInfo::RNA;
      case ialpha4_id("pyra"): return ResidueInfo::PYR;
    }
  }
  return ResidueInfo::UNKNOWN;
}

template<typename T>
void insert_comp_list(cif::Document& doc, T& ri_map) {
  if (cif::Block* list_block = doc.find_block("comp_list")) {
    for (auto row : list_block->find("_chem_comp.",
                                {"id", "group", "?number_atoms_nh"})) {
      ResidueInfo ri;
      ri.kind = chemcomp_group_to_kind(row[1]);
      ri.one_letter_code = ' ';
      ri.hydrogen_count = row.has2(2) ? cif::as_int(row[2]) : 0;
      ri_map.emplace(row.str(0), ri);
    }
  }
}

inline void insert_chemlinks(cif::Document& doc,
                             std::map<std::string,ChemLink>& links) {
  if (const cif::Block* list_block = doc.find_block("link_list")) {
    for (auto row : const_cast<cif::Block*>(list_block)->find("_chem_link.",
                                   {"id", "name",
                                    "comp_id_1", "mod_id_1", "group_comp_1",
                                    "comp_id_2", "mod_id_2", "group_comp_2"})) {
      ChemLink link;
      link.id = row.str(0);
      link.name = row.str(1);
      link.side1.comp = row.str(2);
      link.side1.mod = row.str(3);
      link.side1.group = ChemLink::read_group(row[4]);
      link.side2.comp = row.str(5);
      link.side2.mod = row.str(6);
      link.side2.group = ChemLink::read_group(row[7]);
      const cif::Block* block = doc.find_block("link_" + link.id);
      if (!block)
        fail("inconsisted data_link_list");
      link.rt = read_link_restraints(*block);
      links.emplace(link.id, link);
    }
  }
}

// Helper function. str is one of "add", "delete", "change".
inline int chem_mod_type(const std::string& str) {
  char c = str[0] | 0x20;
  if (c != 'a' && c != 'd' && c != 'c')
    fail("Unexpected value of _chem_mod_*.function: " + str);
  return c;
}

inline Restraints read_restraint_modifications(const cif::Block& block_) {
  Restraints rt;
  cif::Block& block = const_cast<cif::Block&>(block_);
  for (auto row : block.find("_chem_mod_bond.",
                             {"function", "atom_id_1", "atom_id_2",
                              "new_type",
                              "new_value_dist", "new_value_dist_esd"}))
    rt.bonds.push_back({{chem_mod_type(row[0]), row.str(1)}, {1, row.str(2)},
                        bond_type_from_string(row[3]), false,
                        cif::as_number(row[4]), cif::as_number(row[5])});
  for (auto row : block.find("_chem_mod_angle.",
                             {"function", "atom_id_1",
                              "atom_id_2", "atom_id_3",
                              "new_value_angle", "new_value_angle_esd"}))
    rt.angles.push_back({{chem_mod_type(row[0]), row.str(1)},
                         {1, row.str(2)}, {1, row.str(3)},
                         cif::as_number(row[4]), cif::as_number(row[5])});
  for (auto row : block.find("_chem_mod_tor.",
                              {"function", "id", "atom_id_1",
                               "atom_id_2", "atom_id_3", "atom_id_4",
                               "new_value_angle", "new_value_angle_esd",
                               "new_period"}))
    rt.torsions.push_back({row.str(1), {chem_mod_type(row[0]), row.str(2)},
                           {1, row.str(3)}, {1, row.str(4)}, {1, row.str(5)},
                           cif::as_number(row[6]), cif::as_number(row[7]),
                           cif::as_int(row[8])});
  for (auto row : block.find("_chem_mod_chir.",
                             {"function", "atom_id_centre", "atom_id_1",
                              "atom_id_2", "atom_id_3",
                              "new_volume_sign"}))
    rt.chirs.push_back({{1, row.str(1)}, {chem_mod_type(row[0]), row.str(2)},
                        {1, row.str(3)}, {1, row.str(4)},
                        chirality_from_string(row[5])});
  for (auto row : block.find("_chem_mod_plane_atom.",
                             {"function", "plane_id", "atom_id" ,
                              "new_dist_esd"})) {
    Restraints::Plane& plane = rt.get_or_add_plane(row.str(1));
    if (plane.esd == 0.0)
      plane.esd = cif::as_number(row[3]);
    plane.ids.push_back({chem_mod_type(row[0]), row.str(2)});
  }
  return rt;
}

inline void insert_chemmods(cif::Document& doc,
                            std::map<std::string, ChemMod>& mods) {
  if (const cif::Block* list_block = doc.find_block("mod_list")) {
    for (auto row : const_cast<cif::Block*>(list_block)->find("_chem_mod.",
                                   {"id", "name", "comp_id", "group_id"})) {
      ChemMod mod;
      mod.id = row.str(0);
      mod.name = row.str(1);
      mod.comp_id = row.str(2);
      mod.group_id = row.str(3);
      const cif::Block* block = doc.find_block("mod_" + mod.id);
      if (!block)
        fail("inconsisted data_mod_list");
      for (auto ra : const_cast<cif::Block*>(block)->find("_chem_mod_atom.",
                                  {"function", "atom_id", "new_atom_id",
                                   "new_type_symbol", "new_type_energy",
                                   "?new_charge", "?new_partial_charge"}))
        mod.atom_mods.push_back({chem_mod_type(ra[0]), ra.str(1), ra.str(2),
                                 Element(ra.str(3)),
                                 (float) cif::as_number(ra.one_of(5, 6)),
                                 ra.str(4)});
      mod.rt = read_restraint_modifications(*block);
      mods.emplace(mod.id, mod);
    }
  }
}

namespace impl {
template <typename T>
T& add_or_set(std::vector<T>& items, typename std::vector<T>::iterator it,
              const T& x) {
  if (it == items.end()) {
    items.push_back(x);
    return items.back();
  }
  *it = x;
  return *it;
}
} // namespace impl

inline void ChemMod::apply_to(ChemComp& chemcomp) const {
  // _chem_mod_atom
  for (const AtomMod& mod : atom_mods) {
    auto it = chemcomp.find_atom(mod.old_id);
    switch (mod.func) {
      case 'a':
        if (chemcomp.find_atom(mod.new_id) == chemcomp.atoms.end())
          chemcomp.atoms.push_back({mod.new_id, mod.el,
                                    std::isnan(mod.charge) ? mod.charge : 0,
                                    mod.chem_type});
        break;
      case 'd':
        if (it != chemcomp.atoms.end()) {
          chemcomp.atoms.erase(it);
          // delete restraints containing mod.old_id
          const std::string& old = mod.old_id;
          vector_remove_if(chemcomp.rt.bonds, [&](const Restraints::Bond& b) {
              return b.id1 == old || b.id2 == old;
          });
          vector_remove_if(chemcomp.rt.angles, [&](const Restraints::Angle& a) {
              return a.id1 == old || a.id2 == old || a.id3 == old;
          });
          vector_remove_if(chemcomp.rt.torsions,
              [&](const Restraints::Torsion& t) {
                return t.id1 == old || t.id2 == old || t.id3 == old ||
                       t.id4 == old;
          });
          vector_remove_if(chemcomp.rt.chirs,
              [&](const Restraints::Chirality& c) {
                return c.id_ctr == old || c.id1 == old || c.id2 == old ||
                       c.id3 == old;
          });
          for (Restraints::Plane& plane : chemcomp.rt.planes)
            vector_remove_if(plane.ids, [&](const Restraints::AtomId& a) {
                return a.atom == old;
            });
        }
        break;
      case 'c':
        if (it != chemcomp.atoms.end()) {
          if (!mod.new_id.empty())
            it->id = mod.new_id;
          if (mod.el != El::X)
            it->el = mod.el;
          if (!std::isnan(mod.charge))
            it->charge = mod.charge;
          if (!mod.chem_type.empty())
            it->chem_type = mod.chem_type;
        }
        break;
    }
  }

  // _chem_mod_bond
  for (const Restraints::Bond& mod : rt.bonds) {
    auto it = chemcomp.rt.find_bond(mod.id1.atom, mod.id2.atom);
    switch (mod.id1.comp) {
      case 'a':
        impl::add_or_set(chemcomp.rt.bonds, it, mod).id1.comp = 1;
        break;
      case 'd':
        if (it != chemcomp.rt.bonds.end())
          chemcomp.rt.bonds.erase(it);
        break;
      case 'c':
        if (it != chemcomp.rt.bonds.end()) {
          if (mod.type != BondType::Unspec)
            it->type = mod.type;
          if (!std::isnan(mod.value))
            it->value = mod.value;
          if (!std::isnan(mod.esd))
            it->esd = mod.esd;
        }
        break;
    }
  }

  // _chem_mod_angle
  for (const Restraints::Angle& mod : rt.angles) {
    auto it = chemcomp.rt.find_angle(mod.id1.atom, mod.id2.atom, mod.id3.atom);
    switch (mod.id1.comp) {
      case 'a':
        impl::add_or_set(chemcomp.rt.angles, it, mod).id1.comp = 1;
        break;
      case 'd':
        if (it != chemcomp.rt.angles.end())
          chemcomp.rt.angles.erase(it);
        break;
      case 'c':
        if (it != chemcomp.rt.angles.end()) {
          if (!std::isnan(mod.value))
            it->value = mod.value;
          if (!std::isnan(mod.esd))
            it->esd = mod.esd;
        }
        break;
    }
  }

  // _chem_mod_tor
  for (const Restraints::Torsion& mod : rt.torsions) {
    auto it = chemcomp.rt.find_torsion(mod.id1.atom, mod.id2.atom,
                                       mod.id3.atom, mod.id4.atom);
    switch (mod.id1.comp) {
      case 'a':
        impl::add_or_set(chemcomp.rt.torsions, it, mod).id1.comp = 1;
        break;
      case 'd':
        if (it != chemcomp.rt.torsions.end())
          chemcomp.rt.torsions.erase(it);
        break;
      case 'c':
        if (it != chemcomp.rt.torsions.end()) {
          if (!mod.label.empty())
            it->label = mod.label;
          if (!std::isnan(mod.value))
            it->value = mod.value;
          if (!std::isnan(mod.esd))
            it->esd = mod.esd;
          if (mod.period != -1)
            it->period = mod.period;
        }
        break;
    }
  }

  // _chem_mod_chir
  for (const Restraints::Chirality& mod : rt.chirs) {
    auto it = chemcomp.rt.find_chir(mod.id_ctr.atom, mod.id1.atom,
                                    mod.id2.atom, mod.id3.atom);
    switch (mod.id1.comp) {
      case 'a':
        impl::add_or_set(chemcomp.rt.chirs, it, mod).id1.comp = 1;
        break;
      case 'd':
        if (it != chemcomp.rt.chirs.end())
          chemcomp.rt.chirs.erase(it);
        break;
      case 'c':
        if (it != chemcomp.rt.chirs.end())
          it->chir = mod.chir;
        break;
    }
  }

  // _chem_mod_plane_atom
  for (const Restraints::Plane& mod : rt.planes)
    for (const Restraints::AtomId& atom_id : mod.ids) {
      if (atom_id.comp == 'a') {
        Restraints::Plane& plane = chemcomp.rt.get_or_add_plane(mod.label);
        if (plane.esd == 0.0 && !std::isnan(mod.esd))
          plane.esd = mod.esd;
        auto it = std::find(plane.ids.begin(), plane.ids.end(), atom_id.atom);
        if (it == plane.ids.end())
          plane.ids.push_back({1, atom_id.atom});
      } else if (atom_id.comp == 'd') {
        auto it = chemcomp.rt.get_plane(mod.label);
        if (it != chemcomp.rt.planes.end()) {
          auto item = std::find(it->ids.begin(), it->ids.end(), atom_id.atom);
          if (item != it->ids.end())
            it->ids.erase(item);
        }
      }
    }
}


struct MonLib {
  cif::Document mon_lib_list;
  std::map<std::string, ChemComp> monomers;
  std::map<std::string, ChemLink> links;
  std::map<std::string, ChemMod> modifications;
  std::map<std::string, ResidueInfo> residue_infos;

  const ChemLink* find_link(const std::string& link_id) const {
    auto link = links.find(link_id);
    return link != links.end() ? &link->second : nullptr;
  }
  const ChemMod* find_mod(const std::string& name) const {
    auto modif = modifications.find(name);
    return modif != modifications.end() ? &modif->second : nullptr;
  }
  const ChemLink* match_link(
      const std::string& comp1, const std::string& atom1,
      const std::string& comp2, const std::string& atom2) const {
    for (auto& ml : links) {
      const ChemLink& link = ml.second;
      if (link.rt.bonds.empty())
        continue;
      const Restraints::Bond& bond = link.rt.bonds[0];
      if (link.side1.comp == comp1 && link.side2.comp == comp2 &&
          bond.id1.atom == atom1 && bond.id2.atom == atom2)
        return &link;
    }
    return nullptr;
  }

  void ensure_unique_link_name(std::string& name) const {
    size_t orig_len = name.size();
    for (int n = 1; find_link(name) != nullptr; ++n)
      name.replace(orig_len, name.size(), std::to_string(n));
  }
};

typedef cif::Document (*read_cif_func)(const std::string&);

inline MonLib read_monomer_cif(const std::string& path,
                               read_cif_func read_cif) {
  MonLib monlib;
  monlib.mon_lib_list = (*read_cif)(path);
  for (cif::Block& block : monlib.mon_lib_list.blocks)
    if (block.find_values("_chem_comp_atom.atom_id")) {
      ChemComp cc = make_chemcomp_from_block(block);
      std::string name = cc.name;
      monlib.monomers.emplace(name, std::move(cc));
    }
  insert_chemlinks(monlib.mon_lib_list, monlib.links);
  insert_chemmods(monlib.mon_lib_list, monlib.modifications);
  insert_comp_list(monlib.mon_lib_list, monlib.residue_infos);
  return monlib;
}

inline MonLib read_monomer_lib(std::string monomer_dir,
                               const std::vector<std::string>& resnames,
                               read_cif_func read_cif) {
  if (monomer_dir.empty())
    fail("read_monomer_lib: monomer_dir not specified.");
  if (monomer_dir.back() != '/' && monomer_dir.back() != '\\')
    monomer_dir += '/';
  MonLib monlib = read_monomer_cif(monomer_dir + "list/mon_lib_list.cif",
                                   read_cif);
  std::string error;
  for (const std::string& name : resnames) {
    std::string path = monomer_dir;
    path += std::tolower(name[0]);
    path += '/';
    path += name + ".cif";
    try {
      cif::Document doc = (*read_cif)(path);
      auto cc = make_chemcomp_from_cif(name, doc);
      monlib.monomers.emplace(name, cc);
    } catch(std::runtime_error& err) {
      error += "The monomer " + name + " could not be read: ";
      error += err.what();
      error += ".\n";
    }
  }
  if (!error.empty())
    fail(error + "Please create definitions for missing monomers.");
  return monlib;
}

} // namespace gemmi
#endif
// vim:sw=2:ts=2:et

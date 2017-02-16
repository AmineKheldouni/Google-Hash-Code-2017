//
// Created by amine on 14/02/17.
//

#ifndef QUALIFROUND_Slice_H
#define QUALIFROUND_Slice_H

#include "inputs.h"

class Slice {
    std::vector<int> volume;  // (r1,c1,r2,c2)
    int nb_T = 0;
    int nb_M = 0;
public :
    Slice();
    Slice(const vector<int> &init_v, const vector<char> &pizza, const int nb_cols);
    const vector<int> &getVolume() const;

    void setVolume(const vector<int> &volume);
    bool is_valid(const int &l, const int &h) const;
    bool in_pizza(const int &nb_rows, const int &nb_cols) const;
    void get_bigger(const vector<char> &pizza, const int nb_rows, const int nb_cols, const int &l, const int &h);
    void get_valid(const vector<char> &pizza, const int nb_rows, const int nb_cols, const int &l, const int &h);
    void show_slice(const vector<char> &pizza, const int nb_cols) const;
    virtual ~Slice();

};


class Pizza {
    vector<Slice> *list_slices;
    vector<char> pizza;
    int l, h;
    int nb_rows, nb_cols;
public :
    Pizza(const vector<char> &pizza, const int &l, const int &h, const int &nb_rows
    , const int &nb_cols);


    const vector<Slice> &getList_slices() const;

    void setList_slices(const vector<Slice> &list_slices);

    const vector<char> &getPizza() const;

    int getL() const;

    int getH() const;

    int getNb_rows() const;

    int getNb_cols() const;

    void decomposition();
    void show_decomposition() const;
    bool covered(const int &i, const int &j) const ;
    bool covered2() const;
    virtual ~Pizza();
};

#endif //QUALIFROUND_Slice_H

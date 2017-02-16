//
// Created by amine on 14/02/17.
//

#include "Piece.h"



Slice::Slice() {
    vector<int> v (4, 0);
    volume = v;
    nb_T = 0;
    nb_M = 0;
}

Slice::Slice(const vector<int> &init_v, const vector<char> &pizza, const int nb_cols) {
    volume = init_v;
    for (int i=volume[0]; i<volume[2];i++){
        for (int j=volume[1]; j<volume[3];j++) {
            if (pizza[j+nb_cols*i] == 'T') {
                nb_T += 1;
            }
            else {
                nb_M += 1;
            }
        }
    }
}

const vector<int> &Slice::getVolume() const {
    return volume;
}


void Slice::setVolume(const vector<int> &volume) {
    Slice::volume = volume;
}


bool Slice::is_valid(const int &l, const int &h) const{
    if ((nb_M < l || nb_T < l)) {
        return false;
    }
    else if (nb_M > h || nb_T > h){
        return false;
    }
    return true;
}

bool Slice::in_pizza(const int &nb_rows, const int &nb_cols) const {
    if (volume[0]>=0 && volume[2] < nb_rows){
        if (volume[1]>=0 && volume[3] < nb_cols)
            return true;
    }
    return false;
}

void Slice::get_bigger(const vector<char> &pizza, const int nb_rows, const int nb_cols, const int &l, const int &h) {
    vector<int> vect_bigger1 = volume;
    vector<int> vect_bigger2 = volume;
    vect_bigger2[2] ++;
    vect_bigger1[3] ++;
    Slice S1 = Slice(vect_bigger1, pizza, nb_cols);
    Slice S2 = Slice(vect_bigger2, pizza, nb_cols);
    if (S1.is_valid(l, h)) {
        *this = S1;
        get_bigger(pizza, nb_rows, nb_cols, l, h);
    }
    if (S2.is_valid(l, h)) {
        *this = S2;
        get_bigger(pizza, nb_rows, nb_cols, l, h);
    }
}

void Slice::get_valid(const vector<char> &pizza, const int nb_rows, const int nb_cols, const int &l, const int &h) {
    vector<int> vect_bigger1 = volume;
    vector<int> vect_bigger2 = volume;
    vect_bigger1[2] ++;
    vect_bigger2[3] ++;
    Slice S1 = Slice(vect_bigger1, pizza, nb_cols);
    Slice S2 = Slice(vect_bigger2, pizza, nb_cols);
    if (!S1.is_valid(l, h) && !S2.is_valid(l, h)) {
        S1.get_valid(pizza, nb_rows, nb_cols, l, h);
        S2.get_valid(pizza, nb_rows, nb_cols, l, h);
    }
    if (S1.is_valid(l ,h)) {
        *this = S1;
    }
    else *this = S2;
}
void Slice::show_slice(const vector<char> &pizza, const int nb_cols) const {
    string pizza_row = "";
    for(int i=volume[0]; i<volume[2]; i++) {
        for(int j=volume[1]; j<volume[3]; j++) {
            pizza_row += pizza[j+i*nb_cols];
        }
        cout << pizza_row << endl;
        pizza_row = "";
    }
}

Slice::~Slice() {

}

Pizza::Pizza(const vector<char> &pizza, const int &l, const int &h, const int &nb_rows, const int &nb_cols) {
    list_slices = new vector<Slice>(1);
    Pizza::pizza = pizza;
    Pizza::l = l;
    Pizza::h = h;
    Pizza::nb_cols = nb_cols;
    Pizza::nb_rows = nb_rows;
}

Pizza::~Pizza() {

}

const vector<Slice> &Pizza::getList_slices() const {
    return *list_slices;
}

void Pizza::setList_slices(const vector<Slice> &vect_slices) {
    (*list_slices) = vect_slices;
}

bool Pizza::covered(const int &i, const int &j) const {
    vector<int> v;
    for(auto it=list_slices->begin(); it != list_slices->end(); ++it) {
        v = it->getVolume();
        if (i>= v[0] && i < v[2] && j>= v[1] && j < v[3])
            return true;
    }
    return false;
}

bool Pizza::covered2() const {
    for(int i=0; i<nb_rows; i++) {
        for(int j=0; j<nb_cols; j++) {
            covered(i, j);
        }
    }
}

void Pizza::decomposition() {
    vector<int> vect0 = {0, 0, 1, 1};
    Slice S = Slice(vect0, pizza, nb_cols);
    list_slices->push_back(S);
    while (! covered2()) {
        Slice S_tmp = list_slices->back();
        list_slices->pop_back();
        S_tmp.get_valid(pizza, nb_rows, nb_cols, l, h);
        S_tmp.get_bigger(pizza, nb_rows, nb_cols, l, h);
        vector<int> vector_tmp = S_tmp.getVolume();
        list_slices->push_back(S_tmp);
        vector<int> new_vol = {vector_tmp[0], vector_tmp[3], vector_tmp[0]+1, vector_tmp[3]+1};
        Slice next_S = Slice(new_vol, pizza, nb_cols);
        list_slices->push_back(next_S);
    }
}

void Pizza::show_decomposition() const {
    for(auto it = list_slices->begin(); it != list_slices->end(); ++it) {
        it->show_slice(pizza, nb_cols);
    }
}

const vector<char> &Pizza::getPizza() const {
    return pizza;
}

int Pizza::getL() const {
    return l;
}

int Pizza::getH() const {
    return h;
}

int Pizza::getNb_rows() const {
    return nb_rows;
}

int Pizza::getNb_cols() const {
    return nb_cols;
}

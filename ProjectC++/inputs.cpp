//
// Created by amine on 14/02/17.
//

#include "inputs.h"

vector <char> read_inputs(int &n, int &m, int &l, int &h, const string name_file){

    string line;
    ifstream myfile(path+name_file);
// Getting the inputs :
    assert (myfile);
    getline (myfile, line);
    int nb_rows = line[0] - '0';
    int nb_cols = line[2] - '0';
    int min_comp = line[4] - '0';
    int max_comp = line[6] - '0';
    cout << "rows : " << nb_rows << " --- " << " cols : " << nb_cols << endl;
    cout << "min : " << min_comp << " --- "<< " max : " << max_comp << endl;
    vector< char > pizza;
    for(int i=0; i<nb_rows;i++){
        getline(myfile, line);
        for (int j = 0 ; j < nb_cols ; j ++){
            pizza.push_back(line[j]);
        }
    }
    myfile.close();

// Pizza print :
    string pizza_row = "";
    for(int i=0;i<nb_rows;i++){
        for(int j=0;j<nb_cols;j++){
            pizza_row += pizza[j+i*nb_cols];
        }
        pizza_row += " \n";
        cout << pizza_row;
        pizza_row = "";
    }
    n = nb_rows;
    m = nb_cols;
    l = min_comp;
    h = max_comp;

    return pizza;

}
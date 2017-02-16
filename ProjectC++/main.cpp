
#include "Piece.h"

int main() {
    int n, m, l, h;
    vector<char> pizza = read_inputs(n, m, l, h, "example.in");

    cout << "########################" << endl;
    Pizza P = Pizza(pizza, l, h, n, m);
    //P.decomposition();
    //P.show_decomposition();
    vector<int> v_init = {0,0,1,1};
    Slice S = Slice(v_init, P.getPizza(), P.getNb_cols());
    S.get_valid(P.getPizza(), P.getNb_rows(), P.getNb_cols(), P.getL(), P.getH());
    S.get_bigger(P.getPizza(), P.getNb_rows(), P.getNb_cols(), P.getL(), P.getH());
    S.show_slice(P.getPizza(), P.getNb_cols());
    cout << "########################" << endl;
    cout << " Decomposition : " << endl;

    // Write in the output file :
    ofstream myfile2 (path+"example.txt");
    if (myfile2.is_open())
    {
        myfile2 << "This is a line2.\n";
        myfile2 << "This is another line2.\n";
        myfile2.close();
    }

    else cout << "Unable to open file";

    return 0;
}
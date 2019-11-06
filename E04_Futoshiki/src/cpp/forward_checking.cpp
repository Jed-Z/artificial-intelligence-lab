#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;

class Futoshiki {
public:
    int size;
    int con_num;
    vector<vector<int>> puzzle;
    vector<pair<pair<int, int>, pair<int, int>>> constraints;

    Futoshiki(const char* puz_filename, const char* con_filename, int size, int con_num);                 // read puzzle and constraints from file
    bool isSolved();                                                                                      // check whether the puzzle is solved
    vector<vector<set<int>>> makeDomains();                                                               // initialize the domains of each variable
    vector<vector<set<int>>> updateDomains(vector<vector<set<int>>> domains, const pair<int, int>& pos);  // update each domain after assigning a variable
    pair<int, int> mrv(const vector<vector<set<int>>>& domains);                                          // choose a unassigned variable with minimum remaining values
    vector<vector<int>> forwardChecking(const vector<vector<set<int>>>& domains);                         // try to solve the CSP

private:
    // count the total number of values available in the puzzle
    int domainCount(const vector<vector<set<int>>>& domains) {
        int count = 0;
        for(int i = 0; i < size; i++) {
            for(int j = 0; j < size; j++) {
                count += domains[i][j].size();
            }
        }
        return count;
    }
};

/*
    Read the puzzle and constraints from files to numpy matrices,
    and convert the coordinates into 0-indexed (coordinates in the
    file are 1-indexed).
*/
Futoshiki::Futoshiki(const char* puz_filename, const char* con_filename, int size, int con_num)
    : size(size), con_num(con_num), puzzle(size, vector<int>(size, 0)) {
    ifstream puz_file(puz_filename), con_file(con_filename);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            puz_file >> puzzle[i][j];
        }
    }

    for (int i = 0; i < con_num; i++) {
        int x1, y1, x2, y2;
        con_file >> x1 >> y1 >> x2 >> y2;
        constraints.push_back(make_pair(make_pair(x1 - 1, y1 - 1), make_pair(x2 - 1, y2 - 1)));
    }
    puz_file.close();
    con_file.close();
}

/* Check whether all cells in the puzzle is filled. */
bool Futoshiki::isSolved() {
    for (int i = 0; i < puzzle.size(); i++) {
        for (int j = 0; j < puzzle[0].size(); j++) {
            if (puzzle[i][j] == 0) {
                return false;
            }
        }
    }
    return true;
}

vector<vector<set<int>>> Futoshiki::makeDomains() {
    // initialize
    vector<vector<set<int>>> domains(size, vector<set<int>>(size, set<int>()));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] == 0) {
                for (int k = 0; k < size; k++) {
                    domains[i][j].insert(k + 1);
                }
            } else {
                domains[i][j].insert(puzzle[i][j]);
            }
        }
    }

    // remove values that have conflict on rows or columns
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] != 0) {
                for (int i2 = 0; i2 < size; i2++) {
                    if (i2 != i) {
                        domains[i2][j].erase(puzzle[i][j]);
                    }
                }
                for (int j2 = 0; j2 < size; j2++) {
                    if (j2 != j) {
                        domains[i][j2].erase(puzzle[i][j]);
                    }
                }
            }
        }
    }

    // remove values that have conflict with constraints
    int old_domain_count = 0, new_domain_count;
    // repeat until total count of all domains cannot decrease anymore
    do {
        for (int i = 0; i < con_num; i++) {
            pair<int, int> large_pos = constraints[i].first;
            pair<int, int> small_pos = constraints[i].second;
            if (puzzle[large_pos.first][large_pos.second] != 0) {  // large_pos has been assigned
                for (int k = puzzle[large_pos.first][large_pos.second]; k <= size; k++) {
                    domains[small_pos.first][small_pos.second].erase(k);
                }
            }
            else {  // large_pos has not been assigned
                int minimum = *domains[small_pos.first][small_pos.second].begin();
                domains[large_pos.first][large_pos.second].erase(minimum);
            }
            if (puzzle[small_pos.first][small_pos.second] != 0) {
                for (int k = 1; k <= puzzle[small_pos.first][small_pos.second]; k++) {
                    domains[large_pos.first][large_pos.second].erase(k);
                }
            }
            else {
                int minimum = *domains[large_pos.first][large_pos.second].rbegin();
                domains[small_pos.first][small_pos.second].erase(minimum);
            }
        }
        new_domain_count = domainCount(domains);
    } while(old_domain_count == new_domain_count);

    return domains;
}

/*
    In each iteration, we have chosen a pos using MRV, and assign a
    value in its domain to it. After that, we have to update some
    variables' domains by removing some values which has conflict with
    the assignment.
*/
vector<vector<set<int>>> Futoshiki::updateDomains(vector<vector<set<int>>> domains, const pair<int, int>& pos) {
    // check the same column
    for (int i = 0; i < size; i++) {
        if (i == pos.first)
            continue;
        else if (puzzle[i][pos.second] == puzzle[pos.first][pos.second]) {
            return vector<vector<set<int>>>();  // DWO
        } else {
            domains[i][pos.second].erase(puzzle[pos.first][pos.second]);
            if (domains[i][pos.second].size() == 0) {
                return vector<vector<set<int>>>();  // DWO
            }
        }
    }

    // check the same row
    for (int j = 0; j < size; j++) {
        if (j == pos.second)
            continue;
        else if (puzzle[pos.first][j] == puzzle[pos.first][pos.second]) {
            return vector<vector<set<int>>>();  // DWO
        } else {
            domains[pos.first][j].erase(puzzle[pos.first][pos.second]);
            if (domains[pos.first][j].size() == 0) {
                return vector<vector<set<int>>>();  // DWO
            }
        }
    }

    // check the constraints
    for (int i = 0; i < con_num; i++) {
        pair<int, int> large_pos = constraints[i].first;
        pair<int, int> small_pos = constraints[i].second;
        if (pos == large_pos) {
            for (int k = puzzle[pos.first][pos.second]; k <= size; k++) {
                domains[small_pos.first][small_pos.second].erase(k);
                if (puzzle[small_pos.first][small_pos.second] == 0 && domains[small_pos.first][small_pos.second].size() == 0) {
                    return vector<vector<set<int>>>();  // DWO
                }
            }
        } else if (pos == small_pos) {
            for (int k = 1; k <= puzzle[pos.first][pos.second]; k++) {
                domains[large_pos.first][large_pos.second].erase(k);
                if (puzzle[large_pos.first][large_pos.second] == 0 && domains[large_pos.first][large_pos.second].size() == 0) {
                    return vector<vector<set<int>>>();  // DWO
                }
            }
        }
    }
    return domains;
}

/*
    Find the variable with minimum remaining values (MRV),
    and return its position.
*/
pair<int, int> Futoshiki::mrv(const vector<vector<set<int>>>& domains) {
    int min_val = size * size;  // max size of domain
    pair<int, int> min_pos = make_pair(-1, -1);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] == 0 && domains[i][j].size() < min_val) {
                min_val = domains[i][j].size();
                min_pos = make_pair(i, j);
            }
        }
    }
    return min_pos;
}

/* Use forward checking algorithm to solve the CSP problem. */
vector<vector<int>> Futoshiki::forwardChecking(const vector<vector<set<int>>>& domains) {
    if (isSolved()) {
        return puzzle;
    }

    pair<int, int> pos = mrv(domains);

    for (auto pd = domains[pos.first][pos.second].begin(); pd != domains[pos.first][pos.second].end(); pd++) {
        puzzle[pos.first][pos.second] = *pd;
        auto temp_domains = updateDomains(domains, pos);
        if (temp_domains.size() != 0) {  // not DWO
            vector<vector<int>> ret = forwardChecking(temp_domains);
            if (ret.size() != 0) return ret;
        }
    }

    puzzle[pos.first][pos.second] = 0;  // restore the assignment
    return vector<vector<int>>();
}

int main() {
    Futoshiki game("../puzzle.txt", "../constraints.txt", 9, 30);
    auto domains = game.makeDomains();
    vector<vector<int>> result = game.forwardChecking(domains);
    if (result.size() != 0) {
        cout << "Solution found:" << endl;
        for (int i = 0; i < game.size; i++) {
            for (int j = 0; j < game.size; j++) {
                cout << result[i][j] << " ";
            }
            cout << endl;
        }
    } else {
        cout << "[-] No solution!" << endl;
    }
    return 0;
}

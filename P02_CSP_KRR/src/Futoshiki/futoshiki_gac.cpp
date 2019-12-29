#include <algorithm>
#include <fstream>
#include <iostream>
#include <list>
#include <set>
#include <string>
#include <vector>
using namespace std;

typedef vector<vector<int>> PUZZLE;        // 棋盘每个格子的赋值
typedef vector<vector<set<int>>> DOMAINS;  // 棋盘上每个格子的取值域

/* 约束类，用于表示一个约束 */
struct Constraint {
    int type;                                         // type==0为不等式约束，>0为行约束，<0的绝对值为列约束。行列约束的索引均从1开始
    pair<pair<int, int>, pair<int, int>> inequality;  // 不等式约束，first>second，索引从0开始
    Constraint(int type, pair<pair<int, int>, pair<int, int>> inequality = make_pair(make_pair(-1, -1), make_pair(-1, -1)))
        : type(type), inequality(inequality) {}
    bool operator==(const Constraint& y) {  // 重载运算符，主要用于find函数
        return (type == y.type && inequality == y.inequality);
    }
};

class Futoshiki {
   public:
    Futoshiki(const string puz_filename, const string con_filename);
    bool isSolved();  // check whether the puzzle is solved
    void printPuzzle();
    DOMAINS makeDomains(list<Constraint>& gac_queue);         // initialize the domains of each variable
    pair<int, int> chooseUnassigned(const DOMAINS& domains);  // choose a unassigned variable with minimum remaining values

    void pushConstraintIntoQueue(pair<int, int> pos, list<Constraint>& gac_queue);  // 将与变量pos相关的所有约束加入队列
    PUZZLE gac(const DOMAINS& domains, list<Constraint>& gac_queue);                // GAC外层
    DOMAINS gacEnforce(DOMAINS domains, list<Constraint>& gac_queue);               // GAC enforce

   private:
    int size;     // 棋盘边长
    PUZZLE puzzle;
    vector<Constraint> constraints;  // 只储存不等式约束，行列约束是平凡的，无需储存
};

/*
    Read the puzzle and constraints from files to numpy matrices,
    and convert the coordinates into 0-indexed (coordinates in the
    file are 1-indexed).
*/
Futoshiki::Futoshiki(const string puz_filename, const string con_filename)
    : size(0) {
    ifstream puz_file(puz_filename.c_str()), con_file(con_filename.c_str());
    if(!puz_file || !con_file) {
        cerr << "[-] Failed to open file. Check again." << endl;
        exit(-1);
    }
    string temp;
    int con_num = 0;
    while (getline(puz_file, temp)) size++;
    while (getline(con_file, temp)) con_num++;
    puz_file.clear(); puz_file.seekg(0);
    con_file.clear(); con_file.seekg(0);
    puzzle.assign(size, vector<int>(size, 0));

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            puz_file >> puzzle[i][j];
        }
    }
    for (int i = 0; i < con_num; i++) {
        int x1, y1, x2, y2;
        con_file >> x1 >> y1 >> x2 >> y2;
        constraints.push_back(Constraint(0, make_pair(make_pair(x1 - 1, y1 - 1), make_pair(x2 - 1, y2 - 1))));
    }
    puz_file.close();
    con_file.close();
}

/* Check whether all cells in the puzzle are filled. */
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

/* 打印整个棋盘 */
void Futoshiki::printPuzzle() {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            cout << puzzle[i][j] << " ";
        }
        cout << endl;
    }
}

/* 从上到下、从左到右选取第一个未赋值的变量 */
pair<int, int> Futoshiki::chooseUnassigned(const DOMAINS& domains) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] == 0) {
                return make_pair(i, j);
            }
        }
    }
    return pair<int, int>();
}

/* GAC */
PUZZLE Futoshiki::gac(const DOMAINS& domains, list<Constraint>& gac_queue) {
    if (domains.size() == 0) return PUZZLE();
    if (isSolved()) {
        return puzzle;  // 找到解
    }
    pair<int, int> pos = chooseUnassigned(domains);
    for (auto pd = domains[pos.first][pos.second].begin(); pd != domains[pos.first][pos.second].end(); pd++) {
        puzzle[pos.first][pos.second] = *pd;  // 赋值
        auto temp_domains = domains;          // 在temp_domains上修改。（注意，若在原domains上修改会导致迭代器失效）
        temp_domains[pos.first][pos.second].clear();
        temp_domains[pos.first][pos.second].insert(*pd);
        pushConstraintIntoQueue(pos, gac_queue);
        
        temp_domains = gacEnforce(temp_domains, gac_queue);

        if (temp_domains.size() != 0) {  // not DWO
            PUZZLE ret = gac(temp_domains, gac_queue);
            if (ret.size() != 0) return ret;  // 已找到解，直接返回该解
        }
    }
    puzzle[pos.first][pos.second] = 0;  // 恢复未赋值状态
    return PUZZLE();                    // 返回无解
}

/* 把与变量pos相关的不等式约束不重复地加入队列 */
void Futoshiki::pushConstraintIntoQueue(pair<int, int> pos, list<Constraint>& gac_queue) {
    for (int i = 0; i < constraints.size(); i++) {
        if (constraints[i].type != 0) {
            continue;
        }  // 只考虑不等式约束。行列约束稍后单独考虑
        pair<pair<int, int>, pair<int, int>> inequality = constraints[i].inequality;
        if (pos == inequality.first || pos == inequality.second) {                              // 与该变量相关的约束
            if (find(gac_queue.begin(), gac_queue.end(), constraints[i]) == gac_queue.end()) {  // 不重复加入
                gac_queue.push_back(constraints[i]);
            }
        }
    }

    // 把变量的行列约束分别不重复地加入队列，特别注意type表示的行列索引是从1开始的
    Constraint row_constraint(Constraint(pos.first + 1));
    if (find(gac_queue.begin(), gac_queue.end(), row_constraint) == gac_queue.end()) {  // 不重复加入
        gac_queue.push_back(row_constraint);
    }
    Constraint col_constraint(Constraint(-(pos.second + 1)));
    if (find(gac_queue.begin(), gac_queue.end(), col_constraint) == gac_queue.end()) {  // 不重复加入
        gac_queue.push_back(col_constraint);
    }
}

DOMAINS Futoshiki::makeDomains(list<Constraint>& gac_queue) {
    // initialize
    DOMAINS domains(size, vector<set<int>>(size, set<int>()));
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

    // 将所有约束（包括行列约束和不等式约束）加入gac_queue
    for (int ij = 1; ij <= size; ij++) {
        gac_queue.push_back(Constraint(ij));   // 第ij行
        gac_queue.push_back(Constraint(-ij));  // 第ij列，注意列用负数表示
    }
    for (int i = 0; i < constraints.size(); i++) {
        gac_queue.push_back(constraints[i]);
    }
    return gacEnforce(domains, gac_queue);  // 首次执行GAC enforce
}

/* GAC enforce */
DOMAINS Futoshiki::gacEnforce(DOMAINS domains, list<Constraint>& gac_queue) {
    while (!gac_queue.empty()) {
        Constraint constraint = gac_queue.front();
        gac_queue.pop_front();

        // 不等式约束
        if (constraint.type == 0) {
            // 以下采用了针对不等式约束优化过的GAC_Enforce，避免了多层循环，提高效率
            pair<int, int> large_pos = constraint.inequality.first;
            pair<int, int> small_pos = constraint.inequality.second;
            int minimum = *domains[small_pos.first][small_pos.second].begin();
            for (int k = 1; k <= minimum; k++) {
                bool did_erased = domains[large_pos.first][large_pos.second].erase(k);
                if (did_erased) {
                    if (domains[large_pos.first][large_pos.second].size() == 0) return DOMAINS();  // DWO
                    pushConstraintIntoQueue(large_pos, gac_queue);
                }
            }

            int maximum = *domains[large_pos.first][large_pos.second].rbegin();
            for (int k = maximum; k <= size; k++) {
                bool did_erased = domains[small_pos.first][small_pos.second].erase(k);
                if (did_erased) {
                    if (domains[small_pos.first][small_pos.second].size() == 0) return DOMAINS();  // DWO
                    pushConstraintIntoQueue(small_pos, gac_queue);
                }
            }
        }
        // 行约束，以下方法已经过优化以提高效率
        else if (constraint.type > 0) {
            int i = constraint.type - 1;
            for (int j = 0; j < size; j++) {
                if (domains[i][j].size() == 1) {
                    int value = *domains[i][j].begin();
                    for (int j1 = 0; j1 < size; j1++) {
                        if (j1 != j) {
                            bool did_erased = domains[i][j1].erase(value);
                            if (did_erased) {
                                if (domains[i][j1].size() == 0) return DOMAINS();  // DWO
                                pushConstraintIntoQueue(make_pair(i, j1), gac_queue);
                            }
                        }
                    }
                }
            }
        }
        // 列约束
        else {
            int j = -constraint.type - 1;
            for (int i = 0; i < size; i++) {
                if (domains[i][j].size() == 1) {
                    int value = *domains[i][j].begin();
                    for (int i1 = 0; i1 < size; i1++) {
                        if (i1 != i) {
                            bool did_erased = domains[i1][j].erase(value);
                            if (did_erased) {
                                if (domains[i1][j].size() == 0) return DOMAINS();  // DWO
                                pushConstraintIntoQueue(make_pair(i1, j), gac_queue);
                            }
                        }
                    }
                }
            }
        }
    }
    return domains;
}

int main(int argc, char* argv[]) {
    if(argc < 2) {
        cerr << "[-] Usage: ./futoshiki_gac <test_id>" << endl;
        cerr << "test_id is a integer from 0 to 5." << endl;
        return -1;
    }
    Futoshiki game(string("tests/puzzle")+argv[1]+".txt", string("tests/constraints")+argv[1]+".txt");
    list<Constraint> gac_queue;
    auto domains = game.makeDomains(gac_queue);  // 初始化各变量的取值域并首次执行gacEnforce
    PUZZLE result = game.gac(domains, gac_queue);

    if (result.size() != 0) {
        cout << "Solution found:" << endl;
        game.printPuzzle();
    } else {
        cout << "[-] No solution!" << endl;
    }
    return 0;
}
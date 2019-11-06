#include "Othello.h"
#include <iostream>
using namespace std;

/* 初始化棋盘 */
void Othello::create(Othello *board) {
    int i, j;
    board->white_num = 2;
    board->black_num = 2;
    for (i = 0; i < 6; i++) {
        for (j = 0; j < 6; j++) {
            board->cell[i][j].color = SPACE;
            board->cell[i][j].stable = 0;
        }
    }
    board->cell[2][2].color = board->cell[3][3].color = WHITE;
    board->cell[2][3].color = board->cell[3][2].color = BLACK;
}

/* 复制棋盘 */
void Othello::copy(Othello *Fake, const Othello *Source) {
    int i, j;
    Fake->white_num = Source->white_num;
    Fake->black_num = Source->black_num;
    for (i = 0; i < 6; i++) {
        for (j = 0; j < 6; j++) {
            Fake->cell[i][j].color = Source->cell[i][j].color;
            Fake->cell[i][j].stable = Source->cell[i][j].stable;
        }
    }
}

/* 打印棋盘 */
void Othello::show(Othello *board) {
    cout << "\n  ";
    for (int i = 0; i < 6; i++) {
        cout << "   " << i + 1;
    }
    cout << endl
         << "   ┌───┬───┬───┬───┬───┬───┐" << endl;
    for (int i = 0; i < 6; i++) {  // 每一行
        cout << i + 1 << "--│";
        for (int j = 0; j < 6; j++) {  // 每一列
            switch (board->cell[i][j].color) {
                case BLACK:
                    cout << " ○ │";
                    break;
                case WHITE:
                    cout << " ● │";
                    break;
                case SPACE:
                    if (board->cell[i][j].stable) {
                        cout << " + │";  // 允许落子
                    } else {
                        cout << "   │";  // 不允许落子
                    }
                    break;
                default:  // 棋子颜色错误
                    cout << " ■ │";
            }
        }
        if (i != 5) cout << endl
                         << "   ├───┼───┼───┼───┼───┼───┤" << endl;
    }
    cout << "\n   └───┴───┴───┴───┴───┴───┘\n";

    cout << "    白棋(●)个数为:" << board->white_num << '\t' << "黑棋(○)个数为:" << board->black_num << endl
         << endl;
}

/* 计算可以落子的位置数量 */
int Othello::rule(Othello *board, enum Option player) {
    unsigned num = 0;
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (board->cell[i][j].color == SPACE) {  // 遍历整个棋盘上的空cell
                board->cell[i][j].stable = 0;
                for (int x = -1; x <= 1; x++) {
                    for (int y = -1; y <= 1; y++) {
                        // 8个方向
                        if (x != 0 || y != 0) {
                            unsigned num2 = 0;
                            for (int i2 = i + x, j2 = j + y; i2 >= 0 && i2 < 6 && j2 >= 0 && j2 < 6; i2 += x, j2 += y) {
                                // 当前检查的cell是对方的棋子
                                if (board->cell[i2][j2].color == (enum Option) - player) {
                                    num2++;
                                } else if (board->cell[i2][j2].color == player) {
                                    board->cell[i][j].stable += player * num2;
                                    break;
                                } else if (board->cell[i2][j2].color == SPACE) {
                                    break;
                                }
                            }
                        }
                    }
                }

                if (board->cell[i][j].stable) {
                    num++;
                }
            }
        } /* END FOR J */
    }     /* END FOR I */
    return num;
}

/* 落子并修改棋盘 */
bool Othello::action(Othello *board, Do *choice, enum Option player) {
    int i = choice->pos.first, j = choice->pos.second;  // 准备落子的位置

    // 若准备落子的位置上已经有棋子，或者在这个位置落子不能吃掉对方任何棋子的话，说明这个action无效
    if (board->cell[i][j].color != SPACE || board->cell[i][j].stable == 0 || player == SPACE) {
        return false;  // 落子无效
    }

    board->cell[i][j].color = player;
    board->cell[i][j].stable = 0;

    // 更新棋子数量
    if (player == WHITE) {
        board->white_num++;
    } else if (player == BLACK) {
        board->black_num++;
    }

    for (int x = -1; x <= 1; x++) {
        for (int y = -1; y <= 1; y++) {
            // 需要在8个方向上检测落子是否符合规则（能否吃子）
            if (x != 0 || y != 0) {
                unsigned num = 0;
                for (int i2 = i + x, j2 = j + y; i2 >= 0 && i2 <= 5 && j2 >= 0 && j2 <= 5; i2 += x, j2 += y) {
                    if (board->cell[i2][j2].color == (enum Option) - player) {
                        num++;
                    } else if (board->cell[i2][j2].color == player) {
                        board->white_num += (player * WHITE) * num;
                        board->black_num += (player * BLACK) * num;

                        for (i2 -= x, j2 -= y; num > 0; num--, i2 -= x, j2 -= y) {
                            board->cell[i2][j2].color = player;
                            board->cell[i2][j2].stable = 0;
                        }
                        break;
                    } else if (board->cell[i2][j2].color == SPACE) {
                        break;
                    }
                }
            }
        }
    }
    return true;  // 落子有效
}

/* 计算赢棋个数 */
void Othello::stable(Othello *board) {
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (board->cell[i][j].color != SPACE) {
                board->cell[i][j].stable = 1;

                for (int x = -1; x <= 1; x++) {
                    for (int y = -1; y <= 1; y++) {
                        // 4个方向
                        if (x == 0 && y == 0) {
                            x = 2;
                            y = 2;
                        } else {
                            int flag = 2;
                            for (int i2 = i + x, j2 = j + y; i2 >= 0 && i2 <= 5 && j2 >= 0 && j2 <= 5; i2 += x, j2 += y) {
                                if (board->cell[i2][j2].color != board->cell[i][j].color) {
                                    flag--;
                                    break;
                                }
                            }

                            for (int i2 = i - x, j2 = j - y; i2 >= 0 && i2 <= 5 && j2 >= 0 && j2 <= 5; i2 -= x, j2 -= y) {
                                if (board->cell[i2][j2].color != board->cell[i][j].color) {
                                    flag--;
                                    break;
                                }
                            }

                            /* 在某一条线上稳定 */
                            if (flag != 0) {
                                board->cell[i][j].stable++;
                            }
                        }
                    }
                }
            }
        }
    }
}

/* 计算评价函数 */
int Othello::judge(Othello *board, enum Option player) {
    stable(board);
    int value = 0;

    // 对稳定子给予奖励
    // for (int i = 0; i < 6; i++) {
    //     for (int j = 0; j < 6; j++) {
    //         if(board->cell[i][j].color == player) {
    //             value += 10 * board->cell[i][j].stable;  // 是自己就奖励
    //         }
    //         else if(board->cell[i][j].color == (enum Option) - player) {
    //             value -= 10 * board->cell[i][j].stable;  // 是对方就惩罚
    //         }
    //     }
    // }

    double d = 0;
    int my_tiles = 0, opp_tiles = 0, my_front_tiles = 0, opp_front_tiles = 0;

	int X1[] = {-1, -1, 1, 1, 0, -1};
	int Y1[] = {0, 1, 1, 0,  -1, -1};
    int V[6][6] = {
        {2000, -5, 8, 8, -5, 2000},
        {-5, -7, 1, 1, -7, -5},
        {8, 1, -5, -5, 1, 8},
        {8, 1, -5, -5, 1, 8},
        {-5, -7, 1, 1, -7, -5},
        {2000, -5, 8, 8, -5, 2000}};

    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (board->cell[i][j].color == player) {  // 奖励自己
                d += V[i][j];
                my_tiles++;
            } else if (board->cell[i][j].color == (enum Option) - player) {  // 惩罚对方
                d -= V[i][j];
                opp_tiles++;
            }
            // if (board->cell[i][j].color != SPACE) {
            //     for (int k = 0; k < 6; k++) {
            //         int x = i + X1[k];
            //         int y = j + Y1[k];
            //         if (x >= 0 && x < 6 && y >= 0 && y < 6 && board->cell[i][j].color == SPACE) {
            //             if (board->cell[i][j].color == player)
            //                 my_front_tiles++;
            //             else
            //                 opp_front_tiles++;
            //             break;
            //         }
            //     }
            // }
        }
    } /* END FOR */

    double p = 0;
    if (my_tiles > opp_tiles)
        p = (100.0 * my_tiles) / (my_tiles + opp_tiles);
    else if (my_tiles < opp_tiles)
        p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles);
    else
        p = 0;

    double f = 0;
    // if (my_front_tiles > opp_front_tiles)
    //     f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles);
    // else if (my_front_tiles < opp_front_tiles)
    //     f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles);
    // else
    //     f = 0;

    // 行动力
    double m = 0;
	my_tiles = rule(board, player);
	opp_tiles = rule(board, (enum Option) - player);
	if(my_tiles > opp_tiles)
		m = (75.0 * my_tiles)/(my_tiles + opp_tiles);
	else if(my_tiles < opp_tiles)
		m = -(75.0 * opp_tiles)/(my_tiles + opp_tiles);
	else m = 0;

    value += (10 * p) + (78.922 * m) + (74.396 * f);

    return value;  // 该分数对player来说越大（越正）越好
}

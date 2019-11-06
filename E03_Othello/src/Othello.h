#ifndef _OTHELLO_H_
#define _OTHELLO_H_
#include <iostream>
using namespace std;

/* 跨平台 */
#define CLEARSCREEN system("clear");
#define PAUSE                               \
    printf("Press any key to continue..."); \
    fgetc(stdin);                           \
    fgetc(stdin);

//基本元素：棋子，颜色，数字变量

enum Option {
    WHITE = -1,
    SPACE,
    BLACK  // 是否能落子  // 黑子
};

struct Do {
    pair<int, int> pos;
    int score;
};

struct WinNum {
    enum Option color;
    int stable;  // 若在此处落子，可以吃掉对方棋子的数量
};

// 主要功能：棋盘及关于棋子的所有操作，功能
class Othello {
   public:
    WinNum cell[6][6];  // 定义棋盘中有6*6个格子
    int white_num;      // 白棋数目
    int black_num;      // 黑棋数目

    void create(Othello *board);                                  // 初始化棋盘
    void copy(Othello *boardDest, const Othello *boardSource);    // 复制棋盘
    void show(Othello *board);                                    // 打印棋盘
    int rule(Othello *board, enum Option player);                 // 计算可以落子的位置数量
    bool action(Othello *board, Do *choice, enum Option player);  // 落子并修改棋盘
    void stable(Othello *board);                                  // 计算赢棋个数
    int judge(Othello *board, enum Option player);                // 计算评价函数
};

#endif

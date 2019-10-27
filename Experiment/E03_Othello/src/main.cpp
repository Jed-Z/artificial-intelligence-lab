#include <string>
#include "Othello.h"
using namespace std;

const int MAX = 65534;
const int MAX_DEPTH = 10;  //最大搜索深度

/* 最大最小博弈与α-β剪枝 */
Do *minimax(Othello *board, enum Option player, int step, int min, int max, Do *choice) {
    choice->score = -MAX;
    choice->pos.first = -1;
    choice->pos.second = -1;

    int num = board->rule(board, player);  // 找出player可以落子的数量，对应于图像界面里面的‘+’的个数

    // 无处落子
    if (num == 0) {
        // 但对方可以落子，让对方下
        if (board->rule(board, (enum Option) - player) != 0) {
            Othello tempBoard;
            Do nextChoice;
            Do *pNextChoice = &nextChoice;
            board->copy(&tempBoard, board);
            pNextChoice = minimax(&tempBoard, (enum Option) - player, step - 1, -max, -min, pNextChoice);
            choice->score = -pNextChoice->score;
            choice->pos.first = -1;
            choice->pos.second = -1;
            return choice;
        } else {  // 双方都无处落子，游戏结束
            int value = WHITE * (board->white_num) + BLACK * (board->black_num);
            if (player * value > 0) {
                choice->score = MAX - 1;
            } else if (player * value < 0) {
                choice->score = -MAX + 1;
            } else {
                choice->score = 0;
            }
            return choice;
        }
    }

    // 以下都为有处落子的情况

    if (step <= 0)  // 已搜索到最大深度，直接返回得分
    {
        choice->score = board->judge(board, player);  // 评价函数
        return choice;
    }

    // 新建一个Do*类型的数组，其中num即为玩家可落子的数量，用于保存所有可落子的选择
    Do *allChoices = (Do *)malloc(sizeof(Do) * num);

    /****
		下面三个两重for循环其实就是分区域寻找可落子的位置，本函数开头的 `num = board->rule(board, player)` 只返
		回了可落子的数量，并没有返回可落子的位置，因此需要重新遍历整个棋盘去寻找可落子的位置。
		下面三个for循环分别按照最外一圈、最中间的四个位置、靠里的一圈这三个顺序来寻找可落子的位置，如下图所示(数字
		表示寻找的顺序)
		1 1 1 1 1 1
		1 3 3 3 3 1
		1 3 2 2 3 1
		1 3 2 2 3 1
		1 3 3 3 3 1
		1 1 1 1 1 1
	*/
    int k = 0;
    // 最外圈
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (i == 0 || i == 5 || j == 0 || j == 5) {
                /* 可落子的位置需要满足两个条件：1、该位置上没有棋子, 2、如果把棋子放在这个位置上可以吃掉对方的
				   棋子(可以夹住对方的棋子)。stable记录的是可以吃掉对方棋子的数量，所以stable>0符合条件2
				*/
                if (board->cell[i][j].color == SPACE && board->cell[i][j].stable) {
                    allChoices[k].score = -MAX;
                    allChoices[k].pos.first = i;
                    allChoices[k].pos.second = j;
                    k++;
                }
            }
        }
    }

    // 中间四个位置
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if ((i == 2 || i == 3 || j == 2 || j == 3) && (i >= 2 && i <= 3 && j >= 2 && j <= 3)) {
                if (board->cell[i][j].color == SPACE && board->cell[i][j].stable) {
                    allChoices[k].score = -MAX;
                    allChoices[k].pos.first = i;
                    allChoices[k].pos.second = j;
                    k++;
                }
            }
        }
    }

    // 中间圈
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if ((i == 1 || i == 4 || j == 1 || j == 4) && (i >= 1 && i <= 4 && j >= 1 && j <= 4)) {
                if (board->cell[i][j].color == SPACE && board->cell[i][j].stable) {
                    allChoices[k].score = -MAX;
                    allChoices[k].pos.first = i;
                    allChoices[k].pos.second = j;
                    k++;
                }
            }
        }
    }

    // 尝试在之前得到的num个可落子位置进行落子
    for (int k = 0; k < num; k++) {
        Do nextChoice;
        Do *pNextChoice = &nextChoice;
        Do thisChoice = allChoices[k];

        Othello tempBoard;
        board->copy(&tempBoard, board);                                                                // 为了不影响当前棋盘，需要复制一份作为虚拟棋盘
        board->action(&tempBoard, &thisChoice, player);                                                // 在虚拟棋盘上落子
        pNextChoice = minimax(&tempBoard, (enum Option) - player, step - 1, -max, -min, pNextChoice);  // 递归调用α-β剪枝，得到对手的落子评分
        thisChoice.score = -pNextChoice->score;                                                        // 上面得到的是对手得分，因此要取相反数

        if (thisChoice.score > min && thisChoice.score < max) /* 可以预计的更优值 */
        {
            min = thisChoice.score;
            choice->score = thisChoice.score;
            choice->pos.first = thisChoice.pos.first;
            choice->pos.second = thisChoice.pos.second;
        } else if (thisChoice.score >= max) /* 好的超乎预计 */
        {
            choice->score = thisChoice.score;
            choice->pos.first = thisChoice.pos.first;
            choice->pos.second = thisChoice.pos.second;
            break;  // 剪枝
        }
        /* 不如已知最优值 */

        /****
            本代码框架与我们在课上学的略有不同。在这里，无论是黑棋还是白棋，其得分都是相对自己来说的，不是“MAX节点最大化
            分数、MIN节点最小化分数”的形式，而是双方的目标都是最大化自己的分数。其实只需要适当取分数的相反数，即可将这种
            形式转换为我们课上学习的形式。由于上面递归调用中将-max和-min分别传参给了min和max，因此可以将MAX节点和MIN节
            点的剪枝代码合二为一，如下。
        */
        // if (thisChoice.score > min) {
        //     min = thisChoice.score;  // 更新alpha的值
        //     choice->score = thisChoice.score;
        //     choice->pos.first = thisChoice.pos.first;
        //     choice->pos.second = thisChoice.pos.second;
        //     if (max <= min) {
        //         break;  // 剪枝
        //     }
        // }
    }

    free(allChoices);
    return choice;
}

int main() {
    Othello board;
    Othello *pBoard = &board;
    enum Option player, present;
    Do choice;
    Do *pChoice = &choice;
    int num, result = 0;
    // char restart = ' ';

    player = SPACE;
    present = BLACK;
    num = 4;
    // restart = ' ';

    cout << ">>> 人机对战开始：" << endl;

    while (player != WHITE && player != BLACK) {
        cout << ">>> 请选择执黑棋(○),或执白棋(●)：输入1为黑棋，-1为白棋" << endl;
        scanf("%d", &player);
        cout << ">>> 黑棋行动:  \n";

        if (player != WHITE && player != BLACK) {
            cout << "[-] 输入不符合规范，请重新输入\n";
            player = SPACE;  // 重置
        }
    }

    board.create(pBoard);

    /* BEGIN WHILE */
    while (num < 6 * 6) {  // 棋盘上未下满36个棋子
        string player_str = "";
        if (present == BLACK) {
            player_str = "黑棋(○)";
        } else if (present == WHITE) {
            player_str = "白棋(●)";
        }

        if (board.rule(pBoard, present) == 0)  //未下满并且无子可下
        {
            if (board.rule(pBoard, (enum Option) - present) == 0) {
                break;  // 双方都无子可下
            }
            cout << player_str << "GAME OVER! \n";
        } else {
            int i, j;
            board.show(pBoard);  // 【首先】打印棋盘

            if (present == player) {
                while (1) {
                    cout << player_str << "\n >>> 请输入棋子坐标，先行后列：";
                    cin >> i >> j;
                    i--;
                    j--;  // 转换为数组下标
                    pChoice->pos.first = i;
                    pChoice->pos.second = j;

                    if (i < 0 || i > 5 || j < 0 || j > 5 || pBoard->cell[i][j].color != SPACE || pBoard->cell[i][j].stable == 0) {
                        cout << "[-] 此处落子不符合规则，请重新选择！" << endl;
                        board.show(pBoard);
                    } else {
                        break;
                    }
                }
                CLEARSCREEN;
                cout << ">>> 玩家本手棋得分为：" << pChoice->score << endl;
                PAUSE
                cout << ">>> 按任意键继续..." << pChoice->score << endl;
            } else  //AI下棋
            {
                cout << player_str << "..........................";

                pChoice = minimax(pBoard, present, MAX_DEPTH, -MAX, MAX, pChoice);
                i = pChoice->pos.first;
                j = pChoice->pos.second;

                CLEARSCREEN;

                cout << ">>> AI本手棋得分为     " << pChoice->score << endl;
            }

            board.action(pBoard, pChoice, present);
            num++;
            cout << player_str << ">>> AI于" << i + 1 << "," << j + 1 << "落子，该你了！";
        }

        present = (enum Option) - present;  //交换执棋者
    }
    /* END WHILE */

    /* 游戏结束，打印结果 */
    board.show(pBoard);
    if (pBoard->white_num > pBoard->black_num) {
        cout << "\n—————— 白棋(●)胜 ——————" << endl;
    } else if (pBoard->white_num < pBoard->black_num) {
        cout << "\n—————— 黑棋(○)胜 ——————" << endl;
    } else {
        cout << "\n———————— 平局 ————————" << endl;
    }

    return 0;
}

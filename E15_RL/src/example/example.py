import numpy as np

R = np.array([
    [-1, -1, -1, -1, 0, -1] ,
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, 100],
    [-1, 0, -1, -1, 0, 100]
])
Q = np.zeros(R.shape)  # 初始化Q表为全零矩阵

goal_state = 5  # 目标状态
discount = 0.8  # 折扣因子

for episode in range(5000):
    state = np.random.randint(R.shape[0])  # 随机选取初始状态
    while True:  # do-while循环
        action = np.random.choice(np.where(R[state] != -1)[0])  # 随机选取一个可行的动作
        next_state = action  # 本例中，执行的动作与下一状态的表示方法相同
        next_actions = np.where(R[next_state] != -1)[0]
        
        Q[state, action] = R[state, action] + discount * np.max([Q[next_state, next_action] for next_action in next_actions])
        if next_state == goal_state:
            break  # 结束本次迭代
        else:
            state = next_state  # 继续迭代

print('Q =')
print(Q)  # 显示Q表（未做归一化）

###########################################################################

state = 2  # 起始状态
path = [state]  # 路径
while state != goal_state:
    next_state = Q[state].argmax()
    path.append(next_state)
    state = next_state
    
print('path:', path)

import random
import numpy as np
from matplotlib import pyplot as plt


class Player():
    def __init__(self, my_rate):
        # 默认值：15级，1星；胜率为输入值
        self.my_levels = 14
        self.my_stars = 1
        self.my_rate = my_rate


# 以预期胜率创建一个获胜列表,输出比赛列表，并打印实际胜率
def winList(rate, matches):
    win_list = []
    actual_rate = 0
    for i in range(0, matches):
        this_round = random.random()
        if this_round <= rate:
            win_list.append(1)
            actual_rate += 1
        else:
            win_list.append(0)
    actual_rate = actual_rate / matches
    # print('ActualRate:' + str(actual_rate))
    # 打印比赛结果列表
    # print(win_list)
    return win_list, actual_rate


# 等级调节函数
def gameLevel(levels, stars, reset_star, key):
    # 当星数小于0时,需要降级判定
    if stars < 0:
        # 非关键级级时，降级(级别+1)，重置星数量为reset_star
        if key == 0:
            levels += 1
            stars = reset_star
        # 关键级级时，不降级，重置星数量为0
        elif key == 1:
            stars = 0
    # 当星数等于reset_star的值加1时，升级(级别-1)，重置星数量为1
    elif stars == reset_star + 1:
        levels -= 1
        stars = 1
    # 当星数等于reset_star的值加2时，升级(级别-1)，重置星数量为2
    elif stars == reset_star + 2:
        levels -= 1
        stars = 2
    # 返回最新stars,levels
    return stars, levels


# 创建一个遍历获胜列表的函数，查看升到几级几星
def gameResult(levels, stars, rate, matches):
    # print('StartLevels:{} StartStars:{}'.format(levels,stars))
    game_result = winList(rate, matches)
    win_list = game_result[0]
    actual_rate = game_result[1]
    # win_list = [1,1,1,1,1,1,1]
    # round_n为当前局数
    round_n = 0
    # 开始遍历
    for i in win_list:
        # 简易规则：胜利+1星；失败-1星
        # 增加规则：连胜+2星
        # 局数+1
        round_n += 1
        if i == 1:
            # 从第三局开始
            if round_n >= 3:
                # 当前两局都获胜时加两星（且level大于5时，即5级以下）
                if win_list[round_n - 2] == 1 and win_list[round_n - 3] == 1 and levels > 5:
                    stars += 2
                else:
                    stars += 1
            else:
                stars += 1
        elif i == 0:
            stars -= 1

        # 判断是否为关键级（可以被5除尽的是关键级）
        if levels % 5 == 0:
            key = 1
        else:
            key = 0

        # 找到reset_star
        reset_star = 6 - (int(levels / 5) - key)
        round_result = gameLevel(levels, stars, reset_star, key)
        stars = round_result[0]
        levels = round_result[1]

        # 0级时（传说级），不升不降，重置星数量为1
        if levels == 0:
            stars = 1
            levels = 0

        # 输出每回合结果
        # print('RoundResult:{} Levels:{} Stars:{}'.format(i,levels,stars))
    final_stars = "*" * stars
    # print('ActualRate:{} FinalLevels:{} FinalStars:{}'.format(actual_rate,levels,final_stars))
    return stars, levels


# 统计函数
def countGame(g_times, final_list):
    # 打印平均值
    print('平均等级：' + str(np.mean(final_list)))
    print('各等级次数：' + str(np.bincount(final_list)))
    np_list = np.array(final_list)
    plt.hist(np_list, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    plt.title('{} tests'.format(g_times))
    plt.show()


if __name__ == '__main__':
    player = Player(0.55)
    player.my_levels = 10
    my_finals = []
    g_times = 50000
    for i in range(0, g_times):
        my_match = 200
        my_games = gameResult(player.my_levels, player.my_stars, player.my_rate, my_match)
        my_finals.append(my_games[1])
    # 打印每次100局比赛的最终结果
    # print(my_finals)
    countGame(g_times, my_finals)
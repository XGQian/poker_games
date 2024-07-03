"""
BlackJack_21点游戏 -

Author: XGQ
Version: 0.1
Date: 2024/6/29
"""
import poker
# 定义玩家类
class Player(poker.Player):
    """玩家"""
    def what_face(self):
        # 计算玩家手牌的总点数（考虑A可能作为1或者11）
        li = []
        for i in self.cards:
            if i.face > 10:
                # J, Q, K 都当作10点
                li.append(10)
            elif i.face == 1:
                # A 暂时当作11点
                li.append(11)
            else:
                # 2-10按照实际点数计算
                li.append(i.face)

        result = sum(li)

        # 如果总点数大于等于21，并且包含A（当作11点），尝试将A改为1点，并重新计算
        while result >= 21 and (11 in li):
            li.remove(11)
            li.append(1)
            result = sum(li)

            # 返回玩家手牌的总点数
        return result


# 初始化
# 创建一个扑克对象
poker = poker.Poker()
# 对扑克进行洗牌
poker.shuffle()
# 创建一个名为“我”的玩家对象
gamer = Player('我')
# 创建一个名为“庄家”的玩家对象
master = Player('庄家')


# 开局
def game_start():
    # 打印游戏开始的标题
    print(' BlackJack - 21点游戏 '.center(40,'='))

# 为玩家发牌
def deal_start(player, is_hidden=False):
    """为玩家发牌，并打印发牌信息"""
    # 摸一张明牌
    card1 = poker.deal()
    player.get_one(card1,is_hidden)
    # 摸一张牌，根据is_hidden参数决定是否为暗牌
    card2 = poker.deal()
    player.get_one(card2,is_hidden)

# 计算并打印玩家和庄家的得分
def score_data(gamer: Player, master: Player, is_over: bool):
    # 计算玩家和庄家的得分（这里只是一个简单的示例，实际规则可能更复杂）
    gamer_score = (21 - abs(gamer.cards_face - 21)) * 100 // 21
    master_score = (21 - abs(master.cards_face - 21)) * 100 // 21
    if not is_over:
        # 判断谁赢了这一局
        if gamer_score > master_score:
            print('玩家赢！')
        elif gamer_score == master_score:
            print('平局！')
        else:
            print('庄家赢！')
    print('\n游戏数据：')
    print(f'{f"玩家 {gamer.cards}":<21} 点数：{gamer.cards_face} 得分：{gamer_score}')
    print(f'{f"庄家 {master.cards}":<21} 点数：{master.cards_face} 得分：{master_score}')


# 开局发牌
game_start()
deal_start(master, is_hidden=True)  # 为庄家发牌，庄家第一张牌为暗牌
deal_start(gamer, is_hidden=False)  # 为玩家发牌，玩家两张牌都为明牌
print()

# 玩家回合
print(' 玩家回合 '.center(40,'='))
gamer.show_cards()  # 显示玩家手牌

# 玩家开始摸牌或停牌
while True:
    gamer.cards_face = gamer.what_face()  # 计算玩家手牌的总点数
    master.cards_face = master.what_face()  # 计算庄家手牌的总点数（此处假设庄家的牌也可见，但通常不是）

    if gamer.cards_face > 21:
        # 如果玩家点数超过21，则玩家输
        print('\n玩家点数超过21，玩家输！', gamer.cards, '点数：', gamer.cards_face, )
        score_data(gamer, master, True)  # 传入is_over=True表示游戏结束
        break

        # 询问玩家是否继续摸牌
    is_ok = input('输入1继续 摸牌 ，输入2或其他 停牌 : ')
    if is_ok == '1':
        gamer_card = poker.deal()
        gamer.get_one(gamer_card)
        print(f'{gamer.name}获得一张{gamer_card}')
        gamer.show_cards()  # 更新后显示玩家手牌
    else:
        # 玩家选择停牌，进入庄家回合
        # 庄家回合
        print()
        print(' 庄家回合 '.center(40,'='))

        # 庄家回合的循环，根据庄家的点数来决定是否继续摸牌
        while True:
            # 计算庄家的手牌总点数
            master.cards_face = master.what_face()

            # 如果庄家的点数小于17，则必须继续摸牌
            if master.cards_face < 17:
                # 摸一张牌
                master_card = poker.deal()
                master.get_one(master_card)
                print(f'{master.name}获得一张{master_card}')
                # 如果庄家的点数大于或等于17，则停止摸牌
            else:
                break

                # 结算
        print()

        # 检查庄家的点数是否超过21
        if master.cards_face > 21:
            # 如果庄家点数超过21，则玩家赢
            print('\n庄家点数超过21，玩家赢！', master.cards, '庄家点数：', master.cards_face)
            score_data(gamer, master, True)  # 游戏结束，传入is_over=True
            break

            # 如果庄家点数没有超过21，则进行正常的得分计算
        score_data(gamer, master, False)  # 游戏未结束，传入is_over=False

        # 因为庄家回合结束后，整个游戏流程也结束了，所以这里再次加入break来确保跳出循环
        break

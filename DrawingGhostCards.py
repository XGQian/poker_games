"""
抽鬼牌 - DrawingGhostCards

Author: XGQ
Version: 0.1
Date: 2024/7/1
"""
import poker
import random

# 定义玩家类
class Player(poker.Player):
    def get_one(self, card, is_hidden = False):
        """摸牌"""
        # 玩家摸到一张牌，将其加入手牌列表
        self.cards.append(card)
        if is_hidden:
            if card.face != 14:
                print(f'{self.name}：获得一张牌')
            else:
                print(f'{self.name}：获得一张{card}')
        else:
            print(f'{self.name}：获得一张{card}')
# 玩家回合
def get_deal(master, gamer, ):
    print(f' {gamer.name}回合开始 '.center(40,'='))
    gamer.show_cards()
    master.show_cards(True)
    while True:
        num = input(f'请抽{master.name}的牌,输入第几张牌：')
        if num.isdigit() and int(num) -1 in range(len(master.cards)):
            break
        print('输入格式错误！！！')
    num = int(num)
    card = master.cards[num - 1]
    master.deal(card)
    gamer.get_one(card)
    # 丢牌
    while True:
        gamer.show_cards()
        try:
            n, m = input('请丢牌，输入第几张和第几张(如1 2)\n输入 0 0 则跳过出牌：').split()
        except:
            print('输入格式错误!!!')
            continue
        if n.isdigit() and m.isdigit():
            n, m = map(int, (n, m))
            if n != m:
                card1 = gamer.cards[n - 1]
                card2 = gamer.cards[m - 1]
                if card1.face == card2.face:
                    gamer.deal(card1)
                    gamer.deal(card2)
                    if len(gamer.cards) == 0:
                        print('you win')
                        return True, gamer, True
                    if len(gamer.cards) == 1 and gamer.cards[0].face == 14:
                        print('you lost')
                        return True, gamer, False
            elif n == 0 and m == 0:
                print(f'{gamer.name}跳过出牌')
                break
            elif n == m:
                print('无法出同一张牌')
        else:
            print(f'{gamer.name}跳过出牌')
            break
    print(f' {gamer.name}回合结束 '.center(40,'='))
    return False, 0

def deal_PC(pc2, master, ):
    # 庄家回合
    print(f' {master.name}回合开始 '.center(40,'='))
    pc2.show_cards(True)
    num = random.randint(1, len(pc2.cards))
    card = pc2.cards[num - 1]
    pc2.deal(card)
    master.get_one(card, True)
    pc2.show_cards(True)
    # if len(master.cards) == 0:
    #     print('winer')
    #     return True, master, True
    # if len(master.cards) == 1 and master.cards[0].face == 14:
    #     print('lost')
    #     return True, master, False
    # 丢牌
    while True:
        master.show_cards(True)
        counts = {}
        for x in [c.face for c in master.cards]:
            counts[x] = counts.get(x, 0) + 1
        key1 = ''
        for i in counts.items():
            if i[1] > 1:
                key1 = i[0]
                break
        if key1:
            n = [c.face for c in master.cards].index(key1)
            card1 = master.cards[n]
            master.deal(card1)
            n = [c.face for c in master.cards].index(key1)
            card1 = master.cards[n]
            master.deal(card1)
            if len(master.cards) == 0:
                print('winer')
                return True, master, True
            if len(master.cards) == 1 and master.cards[0].face == 14:
                print('lost')
                return True, master, False
        else:
            break
    pc2.show_cards(True)
    master.shuffle()
    master.show_cards(True)
    print(f' {master.name}回合结束 '.center(40,'='))
    return False, 0

# 初始化
# 创建一个扑克对象
poker = poker.Poker(1, (2, 1, 11), 1)
# 对扑克进行洗牌
poker.shuffle()
# 创建一个名为“我”的玩家对象
gamer = Player('我')
# 创建一个名为“庄家”的玩家对象
master = Player('庄家')
pc2 = Player('PC')
print(poker.cards)

# 初始发牌
init_card = 7
for i in range(init_card):
    card1 = poker.deal()
    gamer.get_one(card1)
    card2 = poker.deal()
    master.get_one(card2, True)
    card3 = poker.deal()
    pc2.get_one(card3, True)
gamer.show_cards()
master.shuffle()
master.show_cards(True)
pc2.shuffle()
pc2.show_cards(True)
print(' 抽鬼牌 - 游戏开始 '.center(40,'='))

while True:
    result = get_deal(master,gamer)
    if result[0]:
        print(result[1].name, ' win! ' if result[2] else 'lost')
        break
    result = deal_PC(pc2,master)
    if result[0]:
        print(result[1].name, ' win! ' if result[2] else 'lost')
        break
    result = deal_PC(gamer,pc2)
    if result[0]:
        print(result[1].name, ' win! ' if result[2] else 'lost')
        break
gamer.show_cards()
master.show_cards()
pc2.show_cards()

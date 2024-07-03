"""
poker - 

Author: XGQ
Version: 0.1
Date: 2024/7/1
"""
import random
from enum import Enum
# 定义花色枚举
class Suite(Enum):
    """花色(枚举)"""
    # 定义四种花色，分别是黑桃、红心、梅花、方块
    SPADE, HEART, CLUB, DIAMOND, mJOKER, JOKER = range(6)
# 定义牌类
class Card:
    """牌"""
    def __init__(self, suite, face):
        # 初始化牌的花色和点数
        self.suite = suite
        self.face = face
    def __repr__(self):
        # 定义一个字符串表示牌的花色和点数
        suites = '♠♥♣♦🤡😈'  # 花色字符串，分别对应黑桃、红心、梅花、方块
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'joker', 'joker']  # 点数字符串
        # 返回牌的花色和点数，格式为“花色+点数”
        return f'{suites[self.suite.value]}{faces[self.face]}'
# 定义扑克类
class Poker:
    """扑克"""
    def __init__(self, joker = 0, card_num = (4,1,14), poker_num = 1):
        # 初始化一副扑克牌，包含四种花色和13种点数（从A到K）
        self.joker = joker
        self.card_num = card_num
        self.poker_num = poker_num

        self.cards = [
            Card(suite, face)
            for suite in [i for i in Suite][:self.card_num[0]]  # 遍历花色枚举
            for face in range(self.card_num[1], self.card_num[2])  # 遍历点数，从1（A）到13（K）
        ]
        for i in range(self.joker):
            self.cards.append(
                Card([i for i in Suite][4+i], 14+i)
            )
        self.cards = self.cards * poker_num

    def shuffle(self):
        """洗牌"""
        # 洗牌前，将current重置为0，表示还没有发过牌
        self.current = 0
        # 使用random模块的shuffle函数打乱扑克牌顺序
        random.shuffle(self.cards)
    def deal(self):
        """发牌"""
        # 发出当前索引的牌，并更新索引
        card = self.cards[self.current]
        self.current += 1
        return card
    @property
    def has_next(self):
        """还有没有牌可以发"""
        # 判断是否还有未发的牌
        return self.current < len(self.cards)

# 定义玩家类
class Player:
    """玩家"""
    def __init__(self, name):
        # 初始化玩家的名字和手牌列表
        self.name = name
        self.cards = []
    def get_one(self, card, is_hidden = False):
        """摸牌"""
        # 玩家摸到一张牌，将其加入手牌列表
        self.cards.append(card)
        if is_hidden:
            print(f'{self.name}：获得一张牌')
        else:
            print(f'{self.name}：获得一张{card}')
    def show_cards(self, is_hidden = False):
        # 显示玩家当前的手牌
        if is_hidden:
            print(f'{self.name}现在的手牌是: '+' ▮ '*len(self.cards))
        else:
            print(f'{self.name}现在的手牌是: {self.cards}')
    def shuffle(self):
        """洗牌"""
        # 使用random模块的shuffle函数打乱扑克牌顺序
        random.shuffle(self.cards)
        print(f'{self.name}洗了自己的手牌')
    def deal(self, card):
        """出牌"""
        if card in self.cards:
            self.cards.remove(card)
            print(f'{self.name}失去了一张牌: {card}')


if __name__ == '__main__':
    p = Poker(2, (4,1,14), 2)
    print(p.cards)

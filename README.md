# poker_games
python实现扑克游戏 : 抽鬼牌 和 21点 - Python Implementation of Poker Games : Drawing Ghost Cards and Blackjack

## poker模块
首先，定义一个扑克模块，后面的包括以后的扑克牌游戏，都可以调用这个模块
这个模块可以实现：

* 卡牌、扑克牌组
* 发牌、洗牌
* 玩家摸牌、出牌
等一些扑克游戏共性的类和方法

### 定义卡牌的类
**属性**：
* 花色 - 黑桃、红心、梅花、方块 外加两个特殊的鬼牌 
  * 使用Enum将 花色 定义为枚举类型 6种花色与0到5 一一对应
  * 在牌类Card中将所有花色定义成字符串 '♠♥♣♦🤡😈' 
* 面值 - ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'joker', 'joker']

牌类Card 通过__repr__方法使打印返回的是花色值索引的字符 和 面值 索引的字符 如 '♠3'、'🤡joker'
```python
import random
from enum import Enum
# 定义花色枚举
class Suite(Enum):
    """花色(枚举)"""
    # 定义四种花色，分别是黑桃、红心、梅花、方块，外加两种鬼牌
    SPADE, HEART, CLUB, DIAMOND, JOKER, mJOKER = range(6)
# 定义牌类
class Card:
    """牌"""
    def __init__(self, suite, face):
        # 初始化牌的花色和点数
        self.suite = suite
        self.face = face
    def __repr__(self):
        # 定义一个字符串表示牌的花色和点数
        suites = '♠♥♣♦🤡😈'  # 花色字符串，分别对应黑桃、红心、梅花、方块、大鬼、小鬼
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'joker', 'joker']  # 点数字符串
        # 返回牌的花色和点数，格式为“花色+点数”
        return f'{suites[self.suite.value]}{faces[self.face]}'
```
### 定义扑克的类
**属性**：
* 扑克牌组 - 可定义鬼牌数量、花色种类，面值范围，牌组数量

**方法**：
* 洗牌 - 随机打乱牌组
* 发牌 - 返回牌组索引的一张牌
```python
# 定义扑克类
class Poker:
    """扑克"""
    def __init__(self, joker = 0, card_num = (4,1,14), poker_num = 1):
        self.joker = joker    # 鬼牌数量 0，1，2
        self.card_num = card_num  # (花色数量, 面值开始, 面值结束, 牌组数量)
        self.poker_num = poker_num # 牌组数量
        # 初始化一副扑克牌，默认四种花色和13种点数（从A到K）
        self.cards = [
            Card(suite, face)
            for suite in [i for i in Suite][:self.card_num[0]]  # 遍历花色枚举
            for face in range(self.card_num[1], self.card_num[2])  # 遍历点数，从1（A）到13（K）
        ]
        # 在扑克牌组中加入鬼牌，默认是0
        for i in range(self.joker):
            self.cards.append(
                Card([i for i in Suite][4+i], 14+i)
            )
        # 牌组数量，默认1组牌
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
```
### 定义玩家类
**属性**：
* 名字 - 用名字属性来区分玩家
* 手牌 - 一个列表，存储玩家手牌

**方法**：
* 摸牌 - 先通过牌组类的发牌方法获取一张牌，再将这这牌加入玩家手牌
* 洗牌 - 随机打乱手牌
* 出牌 - 先判断这张牌是否在手牌中，在就移除，不在则不做任何操作

如还需计算点数等方法，可以在具体的游戏程序中继承玩家类，再写计算点数的方法
```python
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
        # is_hidden为True，则表示该牌为暗牌
        if is_hidden:
            print(f'{self.name}：获得一张牌')
        else:
            print(f'{self.name}：获得一张{card}')
    def show_cards(self, is_hidden = False):
        # 显示玩家当前的手牌
        # is_hidden为True，则表示该牌为暗牌
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
```
可以打印检查一下，poker模块是否可以正常工作
```python
if __name__ == '__main__':
    # 第一个参数 鬼牌数量
    # 第二个参数 - 元组 (花色数量, 面值开始, 面值结束, 牌组数量)
    # 如 两种花色 A-K的，外加一个鬼牌的牌组
    p = Poker(1, (2,1,14), 1)
    print(p.cards)
```
运行结果如下：
![](https://img2024.cnblogs.com/blog/3476191/202407/3476191-20240702140940119-1814375421.png)

## 抽鬼牌
**玩法**：
* 先根据玩家数量调整扑克牌组数量 - 要确保所有玩家的手牌加起来除了鬼牌都是成对出现 （如 3个人 可以两种花色 面值1-10 外加一张鬼牌，共21张，每人7张牌）
* 开局 - 每个玩家分到一份牌
* 玩家A回合
    * 从玩家B手牌中抽取一张牌，放到自己的手牌中
    * 玩家A可选择自己手牌中两个面值相同的牌打出，出牌次数无限制，也可选择跳过出牌
* 玩家B回合
    * 从玩家C手牌中抽取一张牌，放到自己的手牌中
    * 玩家B可选择自己手牌中两个面值相同的牌打出，出牌次数无限制，也可选择跳过出牌
* 玩家C回合
    * 从玩家A手牌中抽取一张牌，放到自己的手牌中
    * 玩家C可选择自己手牌中两个面值相同的牌打出，出牌次数无限制，也可选择跳过出牌
* 游戏结束条件
  * 当某位玩家出牌后，剩余手牌为空，则该玩家获胜，游戏结束
  * 当某位玩家出牌后，仅剩余一张鬼牌，则该玩家失败，游戏结束

若poker模块中的玩家类无法满足需求，可定义子类继承原玩家类，抽鬼牌需要重写原玩家类的摸牌方法，摸到鬼牌必须显示
```python
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
```
### 初始化
先根据玩家数量调整扑克牌组数量 - 要确保所有玩家的手牌加起来除了鬼牌都是成对出现 （如 3个人 可以两种花色 面值1-10 外加一张鬼牌，共21张，每人7张牌）
```python
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
```
### 定义抽牌与出牌阶段的规则

```python
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
    pc2.show_cards()
    num = random.randint(1, len(pc2.cards))
    card = pc2.cards[num - 1]
    pc2.deal(card)
    master.get_one(card, True)
    pc2.show_cards()
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
            print(f'{master.name}回合结束')
            break
    pc2.show_cards(True)
    master.shuffle()
    master.show_cards(True)
    print(f' {master.name}回合结束 '.center(40,'='))
    return False, 0
```
### 游戏进行
通过while True使游戏不断进行
轮流进行不同玩家的抽牌与出牌，直到某玩家出牌后触发结束条件
```python
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
```
运行结果如下：
![](https://img2024.cnblogs.com/blog/3476191/202407/3476191-20240702152956084-976575918.png)

![](https://img2024.cnblogs.com/blog/3476191/202407/3476191-20240702152910795-448140746.png)




## BlackJack - 21点游戏 
**玩法**：
* 定义 一副 4花色 A-K 无鬼牌 的扑克
* 开局给玩家和庄家各分2张牌，一张明牌，一张暗牌
* 点数说明：
  * 2 - 10 点数就是它们的面值
  * J Q K 点数都是10
  * A默认面值为11，若手牌有A 且 总点数大于等于21，则A面值变为1
* 玩家回合：
  * 玩家选择摸牌或停牌
  * 若选li择摸牌，则给玩家发一张牌
    * 若此时玩家总点数大于21，则玩家输，
    * 若不大于21，则可继续选择摸牌或停牌
  * 若选择停牌，则玩家回合结束，进入庄家回合
* 庄家回合：
  * 庄家选择摸牌或停牌
  * 注：若庄家手牌总点数小于17，则庄家必须摸牌，直到大于等于17
    * 若此时庄家总点数大于21，则庄家输，
    * 若不大于21，则可继续选择摸牌或停牌
  * 若选择停牌，则庄家回合结束，进入结算
* 结算
  * 计算玩家与庄家手牌总点数
  * 总点数离21越近，分数越高
  * 分数一样，平局，否则分数高者赢

若poker模块中的玩家类无法满足需求，可定义子类继承原玩家类，21点需要再写一个计算点数的方法
```python
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
```
### 初始化
* 定义 一副 4花色 A-K 无鬼牌 的扑克
* 开局给玩家和庄家各分2张牌，一张明牌，一张暗牌
```python
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

# 开局发牌
game_start()
deal_start(master, is_hidden=True)  # 为庄家发牌，庄家第一张牌为暗牌
deal_start(gamer, is_hidden=False)  # 为玩家发牌，玩家两张牌都为明牌
print()
```
### 游戏进行
* 玩家回合
* 庄家回合
* 结算
```python
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
```
运行结果如下：
![](https://img2024.cnblogs.com/blog/3476191/202407/3476191-20240702153138731-1407567508.png)
![](https://img2024.cnblogs.com/blog/3476191/202407/3476191-20240702153148649-94252808.png)

import tkinter as tk
from tkinter import messagebox
import numpy as np

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        # 游戏状态变量
        self.board_size = 15
        self.cell_size = 40
        self.record_black = []  # 黑棋落子记录
        self.record_white = []  # 白棋落子记录
        self.rec = []  # 所有已落子位置记录
        self.game_started = False

        # 创建开始界面
        self.create_start_screen()

    def create_start_screen(self):
        # 清空窗口
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建标题
        title_label = tk.Label(self.root, text="五子棋游戏", font=("SimHei", 36))
        title_label.pack(pady=100)

        # 创建开始按钮
        start_btn = tk.Button(self.root, text="开始游戏", font=("SimHei", 24), width=10, height=2, command=self.start_game)
        start_btn.pack(pady=20)

        # 创建退出按钮
        quit_btn = tk.Button(self.root, text="退出游戏", font=("SimHei", 24), width=10, height=2, command=self.root.quit)
        quit_btn.pack(pady=20)

        # 创建游戏说明
        instructions = [
            "游戏规则:",
            "1. 黑方使用鼠标左键落子",
            "2. 白方使用鼠标右键落子",
            "3. 先形成五子连珠者获胜",
            "4. 落子后不可更改"
        ]

        for text in instructions:
            label = tk.Label(self.root, text=text, font=("SimHei", 12))
            label.pack(pady=5)

    def start_game(self):
        self.game_started = True
        # 清空窗口
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建游戏画布
        self.canvas = tk.Canvas(self.root, width=self.board_size*self.cell_size, height=self.board_size*self.cell_size,
                               bg="#DEB887")
        self.canvas.pack(pady=20)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.callback1)  # 左键-黑棋
        self.canvas.bind("<Button-3>", self.callback2)  # 右键-白棋

        # 创建返回按钮
        back_btn = tk.Button(self.root, text="返回主菜单", font=("SimHei", 12), command=self.create_start_screen)
        back_btn.pack(pady=10)

        # 绘制棋盘
        self.draw_board()

    def draw_board(self):
        # 绘制横线
        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size//2, self.cell_size//2 + i*self.cell_size,
                                   (self.board_size-1)*self.cell_size + self.cell_size//2, self.cell_size//2 + i*self.cell_size)
        # 绘制竖线
        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size//2 + i*self.cell_size, self.cell_size//2,
                                   self.cell_size//2 + i*self.cell_size, (self.board_size-1)*self.cell_size + self.cell_size//2)
        # 绘制天元和星位
        star_points = [(3,3), (3,11), (7,7), (11,3), (11,11)]
        for (x,y) in star_points:
            self.canvas.create_oval(self.cell_size//2 + x*self.cell_size - 3, self.cell_size//2 + y*self.cell_size - 3,
                                   self.cell_size//2 + x*self.cell_size + 3, self.cell_size//2 + y*self.cell_size + 3,
                                   fill="black")

    def get_position(self, x, y):
        # 将鼠标坐标转换为棋盘坐标
        col = round((x - self.cell_size//2) / self.cell_size)
        row = round((y - self.cell_size//2) / self.cell_size)
        # 检查是否在棋盘范围内
        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            return row, col
        return None

    def callback1(self, event):
        # 黑棋落子(左键)
        if not self.game_started:
            return

        pos = self.get_position(event.x, event.y)
        if pos is None:
            return

        row, col = pos
        # 计算棋子编号 (从上到下，从左到右)
        stone_id = row * self.board_size + col

        # 检查是否已经有棋子
        if stone_id in self.rec:
            return

        # 记录落子
        self.record_black.append(stone_id)
        self.rec.append(stone_id)

        # 绘制黑子
        self.draw_stone(row, col, "black")

        # 判断是否获胜
        if self.check_win(row, col, "black"):
            messagebox.showinfo("游戏结束", "黑方获胜！")
            self.game_started = False
            self.create_start_screen()

    def callback2(self, event):
        # 白棋落子(右键)
        if not self.game_started:
            return

        pos = self.get_position(event.x, event.y)
        if pos is None:
            return

        row, col = pos
        # 计算棋子编号
        stone_id = row * self.board_size + col

        # 检查是否已经有棋子
        if stone_id in self.rec:
            return

        # 记录落子
        self.record_white.append(stone_id)
        self.rec.append(stone_id)

        # 绘制白子
        self.draw_stone(row, col, "white")

        # 判断是否获胜
        if self.check_win(row, col, "white"):
            messagebox.showinfo("游戏结束", "白方获胜！")
            self.game_started = False
            self.create_start_screen()

    def draw_stone(self, row, col, color):
        # 绘制棋子
        x = self.cell_size//2 + col * self.cell_size
        y = self.cell_size//2 + row * self.cell_size
        self.canvas.create_oval(x - self.cell_size//2 + 2, y - self.cell_size//2 + 2,
                               x + self.cell_size//2 - 2, y + self.cell_size//2 - 2,
                               fill=color, outline="black")

    def check_win(self, row, col, color):
        # 获取当前玩家的所有落子
        stones = self.record_black if color == "black" else self.record_white
        # 将棋子编号转换为坐标
        stone_positions = set()
        for stone_id in stones:
            r = stone_id // self.board_size
            c = stone_id % self.board_size
            stone_positions.add((r, c))

        # 检查四个方向: 水平、垂直、两个对角线
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1  # 当前位置已有一个棋子
            # 正方向检查
            for i in range(1, 5):
                nr, nc = row + dr*i, col + dc*i
                if (nr, nc) in stone_positions:
                    count += 1
                else:
                    break
            # 反方向检查
            for i in range(1, 5):
                nr, nc = row - dr*i, col - dc*i
                if (nr, nc) in stone_positions:
                    count += 1
                else:
                    break
            # 判断是否五子连珠
            if count >= 5:
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass

@dataclass
class Config:
    """配置类，用于存储A*算法的参数"""
    animation_interval: int = 300  # 动画间隔（毫秒）
    allow_diagonal: bool = True    # 是否允许对角线移动
    grid_alpha: float = 0.3       # 网格线透明度

class AStar:
    def __init__(self, grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int], config: Optional[Config] = None):
        """
        初始化A*寻路器
        
        Args:
            grid: 地图数据，0表示可通过，1表示障碍
            start: 起点坐标 (row, col)
            goal: 终点坐标 (row, col)
            config: 配置参数
        """
        self.grid = grid
        self.start = start
        self.goal = goal
        self.config = config or Config()
        self.rows, self.cols = len(grid), len(grid[0])
        
        # 基本方向：上、下、左、右
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 对角线方向
        if self.config.allow_diagonal:
            self.directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
        
        # 搜索过程记录
        self.visited: Set[Tuple[int, int]] = set()
        self.path_trace: List[Tuple[int, int]] = []
        self.final_path: List[Tuple[int, int]] = []
        
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """计算两点间的启发式距离"""
        dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
        if self.config.allow_diagonal:
            return max(dx, dy)  # 切比雪夫距离
        return dx + dy  # 曼哈顿距离

    def get_path_cost(self, current: Tuple[int, int], neighbor: Tuple[int, int]) -> float:
        """计算相邻节点间的移动代价"""
        dx, dy = abs(current[0] - neighbor[0]), abs(current[1] - neighbor[1])
        return 1.4142 if dx + dy == 2 else 1.0  # 对角线移动代价为√2

    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """检查位置是否有效且可通过"""
        row, col = pos
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        return self.grid[row][col] != 1

    def find_path(self) -> bool:
        """执行A*寻路算法"""
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(self.start, self.goal), 0, self.start))
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {self.start: 0}

        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            self.visited.add(current)
            self.path_trace.append(current)

            if current == self.goal:
                self._reconstruct_path(came_from)
                return True

            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if not self.is_valid_position(neighbor):
                    continue

                tentative_g = current_g + self.get_path_cost(current, neighbor)
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, self.goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

        return False

    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
        """重建最终路径"""
        current = self.goal
        while current in came_from:
            self.final_path.append(current)
            current = came_from[current]
        self.final_path.append(self.start)
        self.final_path.reverse()

    def visualize(self) -> None:
        """可视化搜索过程和最终路径"""
        fig, ax = plt.subplots(figsize=(8, 6))
        mat = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        img = ax.imshow(mat, cmap='Pastel1', vmin=0, vmax=5)

        # 添加网格线
        ax.grid(True, alpha=self.config.grid_alpha)
        ax.set_xticks(range(self.cols))
        ax.set_yticks(range(self.rows))

        def update(frame):
            if frame < len(self.path_trace):
                x, y = self.path_trace[frame]
                mat[x][y] = 2  # 搜索过程（蓝色）
            elif frame < len(self.path_trace) + len(self.final_path):
                x, y = self.final_path[frame - len(self.path_trace)]
                mat[x][y] = 4  # 最终路径（红色）

            # 更新特殊点和障碍物
            mat[self.start[0]][self.start[1]] = 3  # 起点（绿色）
            mat[self.goal[0]][self.goal[1]] = 5    # 终点（黑色）
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.grid[i][j] == 1:
                        mat[i][j] = 1  # 障碍物（灰色）

            img.set_data(mat)
            return [img]

        ani = animation.FuncAnimation(
            fig, update,
            frames=len(self.path_trace) + len(self.final_path),
            interval=self.config.animation_interval,
            repeat=False
        )

        plt.title("A* Pathfinding Visualization")
        plt.show()

# 示例用法
if __name__ == "__main__":
    # 地图定义：0是空地，1是障碍
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
    ]

    # 创建A*算法实例并配置参数
    config = Config(
        animation_interval=300,
        allow_diagonal=True,
        grid_alpha=0.3
    )
    
    astar = AStar(grid, start=(0, 0), goal=(2, 5), config=config)
    
    # 执行寻路算法
    if astar.find_path():
        # 可视化结果
        astar.visualize()
    else:
        print("未找到可行路径！")

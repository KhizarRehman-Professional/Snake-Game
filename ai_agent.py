CELL = 20

class AIAgent:
    """
    Simple rule-based AI agent.
    AI Concept: uses Manhattan distance heuristic to move toward food,
    while avoiding walls and itself.
    """

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

    def get_direction(self, snake, food):
        head = snake.get_head()
        food_pos = food.position
        body_set = set(snake.body)

        # All 4 possible moves: right, left, down, up
        possible = [
            (CELL, 0),
            (-CELL, 0),
            (0, CELL),
            (0, -CELL)
        ]

        # Remove opposite of current direction (can't reverse)
        cx, cy = snake.direction
        opposite = (-cx, -cy)
        possible = [d for d in possible if d != opposite]

        # Filter out moves that hit wall or body
        safe = []
        for d in possible:
            nx = head[0] + d[0]
            ny = head[1] + d[1]
            if (0 <= nx < self.screen_w and
                0 <= ny < self.screen_h and
                (nx, ny) not in body_set):
                safe.append(d)

        if not safe:
            return snake.direction  # no safe move, continue anyway

        # Pick the safe move that gets closest to food (Manhattan distance)
        def dist(d):
            nx = head[0] + d[0]
            ny = head[1] + d[1]
            return abs(nx - food_pos[0]) + abs(ny - food_pos[1])

        return min(safe, key=dist)

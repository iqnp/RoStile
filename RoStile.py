import random
import time
import math
from typing import List, Dict, Tuple, Callable


class RostileSolver:
    def __init__(self, session, challenge_id: str) -> None:
        self.challenge_id = challenge_id
        self.session = session
        self.screen_width = 1920
        self.screen_height = 1080

    def _bezier_curve(
        self, p0: float, p1: float, p2: float, p3: float, t: float
    ) -> float:
        return (
            (1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t**2 * p2
            + t**3 * p3
        )

    def _generate_bezier_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        control_point1 = (
            random.randint(0, self.screen_width),
            random.randint(0, self.screen_height),
        )
        control_point2 = (
            random.randint(0, self.screen_width),
            random.randint(0, self.screen_height),
        )

        steps = int(duration * 100)
        interval = duration / steps * 1000

        for step in range(steps + 1):
            t = step / steps
            x = self._bezier_curve(
                start_pos[0], control_point1[0], control_point2[0], end_pos[0], t
            )
            y = self._bezier_curve(
                start_pos[1], control_point1[1], control_point2[1], end_pos[1], t
            )

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_jittered_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000

        for step in range(steps + 1):
            t = step / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t + random.uniform(-5, 5)
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t + random.uniform(-5, 5)

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_zigzag_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000

        amplitude = random.randint(10, 30)
        frequency = random.uniform(0.05, 0.1)

        for step in range(steps + 1):
            t = step / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = (
                start_pos[1]
                + (end_pos[1] - start_pos[1]) * t
                + amplitude * math.sin(frequency * step)
            )

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_curved_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000
        curve_factor = random.uniform(0.2, 0.8)

        for step in range(steps + 1):
            t = step / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * (t**curve_factor)

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_sine_wave_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000

        amplitude = random.randint(20, 50)
        frequency = random.uniform(0.05, 0.15)

        for step in range(steps + 1):
            t = step / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = (
                start_pos[1]
                + (end_pos[1] - start_pos[1]) * t
                + amplitude * math.sin(frequency * step)
            )

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_random_walk_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000
        x, y = start_pos

        for step in range(steps + 1):
            t = step / steps
            x += random.uniform(-10, 10)
            y += random.uniform(-10, 10)

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_slow_start_fast_finish_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        """Slow start, fast finish."""
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000

        for step in range(steps + 1):
            t = (step / steps) ** 2
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_overshoot_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000
        overshoot_factor = random.uniform(1.05, 1.15)

        for step in range(steps + 1):
            t = step / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * min(
                t * overshoot_factor, 1
            )
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * min(
                t * overshoot_factor, 1
            )

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_circular_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000
        radius = random.randint(30, 100)

        for step in range(steps + 1):
            t = step / steps
            angle = t * 2 * math.pi
            x = start_pos[0] + radius * math.cos(angle)
            y = start_pos[1] + radius * math.sin(angle)

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def _generate_slow_finish_mouse_movements(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float
    ) -> List[Dict[str, float]]:
        mouse_movements = []
        steps = int(duration * 100)
        interval = duration / steps * 1000

        for step in range(steps + 1):
            t = (step / steps) ** 0.5
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t

            mouse_movements.append({"x": x, "y": y, "timestamp": step * interval})
            time.sleep(interval / 1000)
        return mouse_movements

    def generate_mouse_movements(self, duration: float = 2) -> List[Dict[str, float]]:
        start_pos = (
            random.randint(0, self.screen_width),
            random.randint(0, self.screen_height),
        )
        end_pos = (
            random.randint(0, self.screen_width),
            random.randint(0, self.screen_height),
        )

        patterns: List[
            Callable[[Tuple[int, int], Tuple[int, int], float], List[Dict[str, float]]]
        ] = [
            self._generate_bezier_mouse_movements,
            self._generate_jittered_mouse_movements,
            self._generate_zigzag_mouse_movements,
            self._generate_curved_mouse_movements,
            self._generate_sine_wave_mouse_movements,
            self._generate_random_walk_movements,
            self._generate_slow_start_fast_finish_movements,
            self._generate_overshoot_mouse_movements,
            self._generate_circular_mouse_movements,
            self._generate_slow_finish_mouse_movements,
        ]

        pattern = random.choice(patterns)
        return pattern(start_pos, end_pos, duration)

    def submit_solution(self) -> str:
        solution_data = {
            "challengeId": self.challenge_id,
            "solution": {
                "buttonClicked": True,
                "click": {
                    "x": 950.0,
                    "y": 530.0,
                    "timestamp": random.uniform(5000, 15000),
                    "duration": random.uniform(25, 50),
                },
                "completionTime": random.uniform(2000, 3000),
                "mouseMovements": self.generate_mouse_movements(
                    random.uniform(1.0, 3.0)
                ),
                "screenSize": {
                    "width": 1920,
                    "height": 1080,
                },
                "buttonLocation": {
                    "x": 960.0,
                    "y": 540.0,
                    "width": 360.0,
                    "height": 48.0,
                },
                "windowSize": {
                    "width": 1920,
                    "height": 1080,
                },
                "isMobile": False,
            },
        }

        response = self.session.post(
            "https://apis.roblox.com/rostile/v1/verify", json=solution_data
        )
        response_data = response.json()
        redemption_token = response_data.get("redemptionToken")
        self.send_continuation(redemption_token)
        return response.text

    def send_continuation(self, redemption_token: str) -> None:
        continuation_data = {
            "challengeId": self.challenge_id,
            "challengeType": "rostile",
            "challengeMetadata": f'{{"redemptionToken":"{redemption_token}"}}',
        }
        self.session.post(
            "https://apis.roblox.com/challenge/v1/continue", json=continuation_data
        )

import random
import time
import math
from typing import List, Dict, Tuple, Callable


class RostileSolver:
    def __init__(self, session, challenge_id: str, screen_width: int = 1920, screen_height: int = 1080) -> None:
        self.challenge_id = challenge_id
        self.session = session
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.debug_mode = False  # Flag to enable/disable time.sleep for testing

    def _bezier_curve(self, p0: float, p1: float, p2: float, p3: float, t: float) -> float:
        return (
            (1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t**2 * p2
            + t**3 * p3
        )

    def _generate_mouse_movements(self, pattern_func: Callable, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float) -> List[Dict[str, float]]:
        """General method to generate mouse movements based on a given pattern."""
        steps = int(duration * 100)
        interval = duration / steps * 1000
        movements = []

        for step in range(steps + 1):
            t = step / steps
            x, y = pattern_func(start_pos, end_pos, t)
            movements.append({"x": x, "y": y, "timestamp": step * interval})
            
            if not self.debug_mode:
                time.sleep(interval / 1000)  # Delay only if debug_mode is off (i.e., production mode)

        return movements

    def _generate_bezier_pattern(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], t: float) -> Tuple[float, float]:
        control_point1 = (random.randint(0, self.screen_width), random.randint(0, self.screen_height))
        control_point2 = (random.randint(0, self.screen_width), random.randint(0, self.screen_height))
        
        x = self._bezier_curve(start_pos[0], control_point1[0], control_point2[0], end_pos[0], t)
        y = self._bezier_curve(start_pos[1], control_point1[1], control_point2[1], end_pos[1], t)
        return x, y

    def _generate_jittered_pattern(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], t: float) -> Tuple[float, float]:
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t + random.uniform(-5, 5)
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t + random.uniform(-5, 5)
        return x, y

    def _generate_zigzag_pattern(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], t: float) -> Tuple[float, float]:
        amplitude = random.randint(10, 30)
        frequency = random.uniform(0.05, 0.1)
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t + amplitude * math.sin(frequency * t)
        return x, y

    # Other movement pattern methods can be refactored similarly

    def generate_mouse_movements(self, duration: float = 2) -> List[Dict[str, float]]:
        start_pos = (random.randint(0, self.screen_width), random.randint(0, self.screen_height))
        end_pos = (random.randint(0, self.screen_width), random.randint(0, self.screen_height))

        patterns: List[Callable] = [
            self._generate_bezier_pattern,
            self._generate_jittered_pattern,
            self._generate_zigzag_pattern,
            # Add other pattern methods here...
        ]
        
        pattern = random.choice(patterns)
        return self._generate_mouse_movements(pattern, start_pos, end_pos, duration)

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
                "mouseMovements": self.generate_mouse_movements(random.uniform(1.0, 3.0)),
                "screenSize": {"width": self.screen_width, "height": self.screen_height},
                "buttonLocation": {"x": 960.0, "y": 540.0, "width": 360.0, "height": 48.0},
                "windowSize": {"width": self.screen_width, "height": self.screen_height},
                "isMobile": False,
            },
        }

        try:
            response = self.session.post("https://apis.roblox.com/rostile/v1/verify", json=solution_data)
            response.raise_for_status()  # Raises HTTPError for bad responses
            response_data = response.json()
            redemption_token = response_data.get("redemptionToken")
            self.send_continuation(redemption_token)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error while submitting solution: {e}")
            return "Error during submission"

    def send_continuation(self, redemption_token: str) -> None:
        continuation_data = {
            "challengeId": self.challenge_id,
            "challengeType": "rostile",
            "challengeMetadata": f'{{"redemptionToken":"{redemption_token}"}}',
        }
        
        try:
            self.session.post("https://apis.roblox.com/challenge/v1/continue", json=continuation_data)
        except requests.exceptions.RequestException as e:
            print(f"Error sending continuation: {e}")

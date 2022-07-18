from enum import Enum
class Part(Enum):
    Play = 400
    Help = 401
    About = 402
    Exit = 403

class HitState(Enum):
    Hit = 0
    Miss = 1

class PadState(Enum):
    Idle = 100
    Hit = 101
    Miss = 102

class PauseState(Enum):
    Pausing = 200
    NotPausing = 201
    Waiting = 202

class ExitReason(Enum):
    Exit = 300
    Finish = 301
    Restart = 302
    Failed = 303


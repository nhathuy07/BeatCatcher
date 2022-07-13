import enum
class Part(enum.Enum):
    Play = 400
    Help = 401
    About = 402
    Exit = 403

class HitState(enum.Enum):
    Hit = 0
    Miss = 1

class PadState(enum.Enum):
    Idle = 100
    Hit = 101
    Miss = 102

class PauseState(enum.Enum):
    Pausing = 200
    NotPausing = 201
    Waiting = 202

class ExitReason(enum.Enum):
    Exit = 300
    Finish = 301
    Restart = 302

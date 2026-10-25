from __future__ import annotations

from collections import deque
from statistics import mean, pstdev

from .liveness import LivenessSignals, classify


LEFT_EYE = (33, 133, 159, 145)
RIGHT_EYE = (362, 263, 386, 374)


def _point(points, index):
    p = points[index]
    return float(p[0]), float(p[1])


def _eye_ratio(points, ids):
    left, right, upper, lower = [_point(points, i) for i in ids]
    horizontal = abs(right[0] - left[0]) or 1e-6
    vertical = abs(lower[1] - upper[1])
    return vertical / horizontal


def face_features(points):
    if len(points) < 455:
        raise ValueError('MediaPipe FaceMesh landmarks are required')
    left_eye = _eye_ratio(points, LEFT_EYE)
    right_eye = _eye_ratio(points, RIGHT_EYE)
    eye_open = (left_eye + right_eye) / 2
    cheek_left = _point(points, 234)
    cheek_right = _point(points, 454)
    nose = _point(points, 1)
    width = abs(cheek_right[0] - cheek_left[0]) or 1e-6
    centre = (cheek_left[0] + cheek_right[0]) / 2
    nose_offset = (nose[0] - centre) / width
    return {'eye_ratio': eye_open, 'face_width': width, 'nose_offset': nose_offset}


class LiveLivenessSession:
    def __init__(self, challenge='BLINK_TWICE', threshold=.62, max_history=40):
        if challenge not in {'BLINK_TWICE', 'TURN_SIDE'}:
            raise ValueError('unsupported challenge')
        self.challenge = challenge
        self.threshold = threshold
        self.nose = deque(maxlen=max_history)
        self.widths = deque(maxlen=max_history)
        self.eye = deque(maxlen=max_history)
        self.frames = 0
        self.blinks = 0
        self.was_closed = False
        self.decision = None

    def _challenge_score(self):
        if self.challenge == 'BLINK_TWICE':
            return min(1.0, self.blinks / 2)
        movement = (max(self.nose) - min(self.nose)) if len(self.nose) >= 2 else 0
        return min(1.0, movement / .18)

    def _motion_score(self):
        if len(self.nose) < 2:
            return 0.0
        return min(1.0, (max(self.nose) - min(self.nose)) / .20)

    def _depth_consistency(self):
        if len(self.widths) < 3:
            return .75
        avg = mean(self.widths) or 1e-6
        cv = pstdev(self.widths) / avg
        return max(0.0, min(1.0, 1 - cv * 8))

    def process(self, points, texture_score=.7):
        texture_score = float(texture_score)
        if not 0 <= texture_score <= 1:
            raise ValueError('texture_score must be between 0 and 1')
        f = face_features(points)
        self.frames += 1
        self.nose.append(f['nose_offset'])
        self.widths.append(f['face_width'])
        self.eye.append(f['eye_ratio'])

        closed = f['eye_ratio'] < .18
        if closed and not self.was_closed:
            self.blinks += 1
        self.was_closed = closed

        motion = self._motion_score()
        depth = self._depth_consistency()
        challenge_score = self._challenge_score()
        result = classify(LivenessSignals(texture_score, motion, depth, challenge_score), threshold=self.threshold)
        completed = challenge_score >= 1.0
        if completed and self.frames >= 6 and self.decision is None:
            self.decision = result

        return {
            'frames': self.frames,
            'blink_count': self.blinks,
            'eye_ratio': round(f['eye_ratio'], 3),
            'head_offset': round(f['nose_offset'], 3),
            'texture_score': round(texture_score, 3),
            'motion_score': round(motion, 3),
            'depth_consistency': round(depth, 3),
            'challenge': self.challenge,
            'challenge_progress': round(challenge_score, 3),
            'challenge_complete': completed,
            'liveness_score': result['liveness_score'],
            'provisional_label': result['label'],
            'decision': self.decision,
        }

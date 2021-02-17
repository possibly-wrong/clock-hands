from itertools import permutations
import sympy as sym

def hand_positions(hour, minute, second):
    """Return positions in [0, 360) of clock hands."""
    r_60 = sym.Rational(60, 1)
    return (360 * (hour + minute / r_60 + second / (r_60 * r_60)) / 12,
            360 * (minute + second / r_60) / r_60,
            360 * second / r_60)

def hand_angles(hands):
    """Return angles between clock hands."""
    x, y, z = sorted(hands)
    return (y - x, z - y, x - z + 360)

# Define metrics to be minimized.
def max_min(*time):
    """(120 minus) minimum angle between clock hands."""
    return 120 - min(hand_angles(hand_positions(*time)))

def min_max(*time):
    """Max. deviation from 120 deg. of angles between clock hands."""
    return max(abs(a - 120) for a in hand_angles(hand_positions(*time)))

h, m, s = [sym.Symbol(v) for v in 'hms']

def critical_points():
    """Generate possible critical positions of sweeping second hand."""
    yield 0
    for x, y, z in permutations(hand_positions(h, m, s)):
        a, b, c = (y - x, z - y, x - z + 360)
        for lhs, rhs in ((a, b), (a, c), (b, c), (a, 120), (b, 120), (c, 120)):
            yield from sym.solve(lhs - rhs, [s])

def all_times(seconds, metric):
    """Generate all critical times with corresponding metric."""
    for hour in range(12):
        for minute in range(60):
            for expr in seconds:
                second = sym.Add(expr).subs({h: hour, m: minute})
                if 0 <= second < 60:
                    yield (metric(hour, minute, second), hour, minute, second)

if __name__ == '__main__':
    seconds = set(critical_points())
    for sweep in (True, False):
        print('Sweeping:' if sweep else 'Ticking:')
        for metric in (max_min, min_max):
            print('    {}'.format(metric.__name__))
            times = sorted(all_times(seconds if sweep else range(60), metric))
            for value, hour, minute, second in times[:16]:
                print('        {:02}:{:02}:{:02}+{} cost {}'.format(
                    hour, minute, int(second), second - int(second), value))

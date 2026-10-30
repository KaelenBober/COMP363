from xmlrpc.client import TRANSPORT_ERROR

from heap363 import MinHeap363
import random

# Given -- simulation settings. PLACEHOLDER values.
LIFE_THREATENING = 1
SEVERE = 2
NON_LIFE_THREATENING = 3
TIERS = [LIFE_THREATENING, SEVERE, NON_LIFE_THREATENING]

# Share of arrivals with each severity, in the same order as TIERS. Must add up to 1.
TIER_WEIGHTS = [0.10, 0.35, 0.55]

# Treatment length in minutes for each severity: (shortest, longest), inclusive.
TREATMENT_MINUTES = {
    LIFE_THREATENING: (60, 180),
    SEVERE: (30, 90),
    NON_LIFE_THREATENING: (10, 30),
}

ARRIVAL_PROB = 0.25          # chance of one arrival in any given minute (about 15 per hour)
NUM_DOCTORS = 12
SIM_MINUTES = 7 * 24 * 60    # one week
SEED = 363                   # same seed -> same "random" week, so runs can be compared

# Most patients the waiting room can hold at once. PLACEHOLDER.
WAITING_ROOM_CAPACITY = 60






# Given -- experiment with the random module. Change the seed and re-run.
random.seed(SEED)
print("five floats:     ", [round(random.random(), 3) for _ in range(5)])
print("five dice rolls: ", [random.randint(1, 6) for _ in range(5)])
print("one weighted pick:", random.choices(TIERS, weights=TIER_WEIGHTS))

picks = random.choices(TIERS, weights=TIER_WEIGHTS, k=10_000)
print("share of each tier in 10,000 picks:",
      {tier: picks.count(tier) / len(picks) for tier in TIERS})







# TODO -- write the three helpers and simulate().
def random_tier() -> int:
    """Return a random severity from TIERS, chosen according to TIER_WEIGHTS."""
    tier = random.choices(tier, TIER_WEIGHTS, k=1)[0]
    return tier


def arrival_happens(arrival_prob: float) -> bool:
    """Return True with probability arrival_prob."""
    happens = False
    happens == random.random() < arrival_prob
    return happens


def treatment_minutes(tier: int) -> int:
    """Return a random treatment length for tier, within TREATMENT_MINUTES[tier]."""
    low, high = TREATMENT_MINUTES[tier]
    minutes = random.randint(low,high)
    return minutes


def simulate(num_doctors: int, arrival_prob: float, minutes: int,
             capacity: int = WAITING_ROOM_CAPACITY,
             seed: int | None = None) -> dict:
    """Run the ED for `minutes` minutes and return the statistics.

    Each minute: every free doctor calls in the most urgent waiting patient
    from a MinHeap363; then at most one new patient arrives and is added to
    the heap as (severity, arrival_minute), or turned away if the heap
    already holds `capacity` patients; then the statistics are updated.
    """
    random.seed(seed)
    stats = {tier: {"arrived": 0, "seen": 0, "total_wait": 0,
                    "still_waiting": 0, "turned_away": 0}
             for tier in TIERS}
    stats["room"] = {"peak_waiting": 0, "first_full_minute": None,
                     "waiting_sum": 0, "busy_sum": 0}
    # TODO
    return stats
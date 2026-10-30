from turtle import st
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
NUM_DOCTORS = 3
SIM_MINUTES = 7 * 24 * 60    # one week
SEED = 363                   # same seed -> same "random" week, so runs can be compared

# Most patients the waiting room can hold at once. PLACEHOLDER.
WAITING_ROOM_CAPACITY = 60

TIER_NAMES = {LIFE_THREATENING: "life-threatening",
              SEVERE: "severe",
              NON_LIFE_THREATENING: "non-life-threatening"}






# Given -- experiment with the random module. Change the seed and re-run.
random.seed(SEED)
print("five floats:     ", [round(random.random(), 3) for _ in range(5)])
print("five dice rolls: ", [random.randint(1, 6) for _ in range(5)])
print("one weighted pick:", random.choices(TIERS, weights=TIER_WEIGHTS))

picks = random.choices(TIERS, weights=TIER_WEIGHTS, k=10_000)
print("share of each tier in 10,000 picks:",
      {tier: picks.count(tier) / len(picks) for tier in TIERS})







# TODO -- write simulate().
def random_tier() -> int:
    """Return a random severity from TIERS, chosen according to TIER_WEIGHTS."""
    tier = random.choices(TIERS, weights = TIER_WEIGHTS, k=1)[0]
    return tier


def arrival_happens(arrival_prob: float) -> bool:
    """Return True with probability arrival_prob."""
    happens = False
    happens = random.random() < arrival_prob
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
    #waiting room
    waiting = MinHeap363()
    #list of doctors, when they are free
    free_at = [0] * num_doctors

    #treatment
    for minute in range(minutes):
        for doctor in range(num_doctors):
            if free_at[doctor] <= minute and waiting.size() > 0:
                #get patient
                patient_severity, patient_minute = waiting.get()
                #check their wait time 
                wait = minute - patient_minute
                # update that severity's seen and total wait
                stats[patient_severity]["seen"] += 1
                stats[patient_severity]["total_wait"] += wait
                #update when that doctor is free
                free_at[doctor] = minute + treatment_minutes(patient_severity)

        #arrival
        if arrival_happens(arrival_prob):
            tier = random_tier()
            stats[tier]["arrived"] += 1
            if waiting.size() >= capacity:
                stats[tier]["turned_away"] += 1
            else:
                waiting.add((tier, minute))

        #room stats
        in_room = waiting.size()
        # check if people in the waiting room is larger than the previous minutes peak
        if in_room > stats["room"]["peak_waiting"]:
            stats["room"]["peak_waiting"] = in_room
        if stats["room"]["first_full_minute"] is None and in_room >= capacity:
            stats["room"]["first_full_minute"] = minute
        stats["room"]["waiting_sum"] += in_room
        for doctor in range(num_doctors):
            if free_at[doctor] > minute:
                stats["room"]["busy_sum"] += 1
        
    for patient in waiting.storage:
        severity = patient[0]
        stats[severity]["still_waiting"] += 1

    return stats


def average_wait(stats: dict, tier: int) -> float | None:
    """Average wait, in minutes, of the patients of `tier` who were seen."""
    average = None
    if stats[tier]["seen"] > 0:
        average = stats[tier]["total_wait"] / stats[tier]["seen"]
    return average


def print_report(stats: dict) -> None:
    print(f"{'severity':22s} {'arrived':>8s} {'seen':>6s} {'waiting':>8s} {'turned away':>12s} {'avg wait (min)':>15s}")
    for tier in TIERS:
        s = stats[tier]
        avg = average_wait(stats, tier)
        shown = "--" if avg is None else f"{avg:.1f}"
        print(f"{TIER_NAMES[tier]:22s} {s['arrived']:8d} {s['seen']:6d} "
              f"{s['still_waiting']:8d} {s['turned_away']:12d} {shown:>15s}")
    room = stats["room"]
    print(f"waiting room: peak {room['peak_waiting']}, first full at minute {room['first_full_minute']}")


print_report(simulate(NUM_DOCTORS, ARRIVAL_PROB, SIM_MINUTES, seed=SEED))





# Given -- how many doctors does this ED need?
print(f"arrival_prob = {ARRIVAL_PROB}, one week, seed = {SEED}\n")
print(f"{'doctors':>7s}  " + "  ".join(f"{TIER_NAMES[t]:>22s}" for t in TIERS))
for doctors in range(6, 17):
    stats = simulate(doctors, ARRIVAL_PROB, SIM_MINUTES, seed=SEED)
    cells = []
    for tier in TIERS:
        avg = average_wait(stats, tier)
        shown = "--" if avg is None else f"{avg:.0f}"
        cells.append(f"{shown:>10s} min, {stats[tier]['still_waiting']:4d} left, {stats[tier]['turned_away']:4d} out")
    print(f"{doctors:7d}  " + "  ".join(f"{c:>22s}" for c in cells))



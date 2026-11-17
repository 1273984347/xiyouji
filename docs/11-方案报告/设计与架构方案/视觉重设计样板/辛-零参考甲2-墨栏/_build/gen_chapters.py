import math
w = []
for i in range(1, 101):
    x = (
        17.0
        + 6.5 * math.sin(i / 9.0 + 0.7)
        + 13.0 * math.exp(-((i - 27) / 2.6) ** 2)
        + 10.0 * math.exp(-((i - 40) / 3.2) ** 2)
        + 9.0 * math.exp(-((i - 59) / 2.4) ** 2)
        + 8.0 * math.exp(-((i - 87) / 3.0) ** 2)
        + 7.0 * math.exp(-((i - 8) / 2.0) ** 2)
        + 6.5 * math.exp(-((i - 14) / 2.4) ** 2)
        + 6.0 * math.exp(-((i - 49) / 2.2) ** 2)
        + 5.5 * math.exp(-((i - 76) / 2.6) ** 2)
        + 5.0 * math.exp(-((i - 96) / 2.4) ** 2)
        + 4.0 * math.exp(-((i - 19) / 2.0) ** 2)
    )
    w.append(max(6.0, x))
total = 2692
s = sum(w)
raw = [v / s * total for v in w]
vals = [int(v) for v in raw]
diff = total - sum(vals)
order = sorted(range(100), key=lambda i: raw[i] - vals[i], reverse=True)
for k in range(diff):
    vals[order[k % 100]] += 1
assert sum(vals) == total, sum(vals)
peak = max(range(100), key=lambda i: vals[i]) + 1
print("sum =", sum(vals), "peak =", peak, "peak value =", max(vals))
print("min =", min(vals), "max =", max(vals))
print("segments(10):", [sum(vals[i * 10:(i + 1) * 10]) for i in range(10)])
print("[")
for i in range(0, 100, 10):
    print("  " + ",".join(str(v) for v in vals[i:i + 10]) + ("," if i < 90 else ""))
print("]")

def flow_to_speed(flow):
    a = -1.4648375
    b = 93.75
    c = -flow
    disc = b**2 - 4*a*c
    if disc < 0: return None
    s1 = (-b + disc**0.5) / (2*a)
    s2 = (-b - disc**0.5) / (2*a)
    return max(s1, s2) if flow < 1500 else min(s1, s2)


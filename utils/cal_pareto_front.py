import numpy as np


def calculate_pareto_front(results, keys, directions=None):
    """
    Calculate the Pareto front from a list of result dicts.

    Parameters
    ----------
    results : list[dict]
        List of result dicts, each containing values for the given keys.
    keys : list[str]
        Metric names to use for Pareto optimization.
    directions : list[str] or None
        Optimization direction for each key: "min" (smaller is better) or
        "max" (larger is better). If None, all keys are treated as "min".

    Returns
    -------
    list[dict]
        The subset of results that lie on the Pareto front.
    """
    n = len(results)
    if n == 0:
        return []
    if n == 1:
        return list(results)

    if directions is None:
        directions = ["min"] * len(keys)

    # Build (n, d) array; flip sign for "max" so all are treated as minimization
    d = len(keys)
    arr = np.empty((n, d), dtype=np.float64)
    for j, key in enumerate(keys):
        col = np.array([r[key] for r in results], dtype=np.float64)
        if directions[j] == "max":
            col = -col
        arr[:, j] = col

    # Vectorized dominance check:
    #   j dominates i  ⇔  all(arr[j] <= arr[i])  AND  any(arr[j] < arr[i])
    #   i is dominated if ∃ j ≠ i such that j dominates i.
    #   (Self-pair i=j fails the strict-inequality check, so self is never
    #   counted as dominating itself — duplicates are handled correctly.)
    le = arr[:, None, :] <= arr[None, :, :]    # (n, n, d) → le[j, i, k]
    lt = arr[:, None, :] < arr[None, :, :]      # (n, n, d) → lt[j, i, k]

    dom = np.all(le, axis=2) & np.any(lt, axis=2)  # (n, n)  dom[j, i]
    dominated = np.any(dom, axis=0)                 # (n,)    True if any j dominates i
    pareto_mask = ~dominated

    return [results[i] for i in range(n) if pareto_mask[i]]


def calculate_pareto_front_indices(results, keys, directions=None):
    """
    Same as calculate_pareto_front but returns indices instead of dicts.
    Useful when you only need the indices for further processing.
    """
    n = len(results)
    if n == 0:
        return np.array([], dtype=np.int64)
    if n == 1:
        return np.array([0], dtype=np.int64)

    if directions is None:
        directions = ["min"] * len(keys)

    d = len(keys)
    arr = np.empty((n, d), dtype=np.float64)
    for j, key in enumerate(keys):
        col = np.array([r[key] for r in results], dtype=np.float64)
        if directions[j] == "max":
            col = -col
        arr[:, j] = col

    le = arr[:, None, :] <= arr[None, :, :]
    lt = arr[:, None, :] < arr[None, :, :]

    dom = np.all(le, axis=2) & np.any(lt, axis=2)
    dominated = np.any(dom, axis=0)
    pareto_mask = ~dominated

    return np.where(pareto_mask)[0]

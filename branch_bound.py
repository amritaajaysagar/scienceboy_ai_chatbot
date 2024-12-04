import numpy as np
from scipy.optimize import linprog
import copy

def branch_and_bound(c, A_eq, b_eq, bounds, maximize=True):
    if maximize:
        c = -np.array(c)  # Negate for maximization

    best_solution = None
    best_value = -np.inf if maximize else np.inf
    node_queue = [{'A_eq': A_eq, 'b_eq': b_eq, 'bounds': bounds}]
    branches = []  # To store details of each branch
    node_count = 0  # To track branch numbers

    while node_queue:
        current_node = node_queue.pop(0)
        A_eq = current_node['A_eq']
        b_eq = current_node['b_eq']
        bounds = current_node['bounds']

        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if not res.success:
            branches.append({
                'node': node_count,
                'status': 'Infeasible',
                'bounds': bounds
            })
            node_count += 1
            continue

        x_relaxed = res.x
        z_relaxed = -res.fun if maximize else res.fun

        branches.append({
            'node': node_count,
            'x': x_relaxed.tolist(),
            'objective': z_relaxed,
            'bounds': bounds
        })
        node_count += 1

        if np.all(np.abs(x_relaxed - np.round(x_relaxed)) < 1e-6):
            if (maximize and z_relaxed > best_value) or (not maximize and z_relaxed < best_value):
                best_solution = x_relaxed
                best_value = z_relaxed
            continue

        fractional_index = np.argmax(np.abs(x_relaxed - np.round(x_relaxed)))
        lower_bound = np.floor(x_relaxed[fractional_index])
        upper_bound = np.ceil(x_relaxed[fractional_index])

        lower_bounds = copy.deepcopy(bounds)
        lower_bounds[fractional_index] = (bounds[fractional_index][0], lower_bound)

        upper_bounds = copy.deepcopy(bounds)
        upper_bounds[fractional_index] = (upper_bound, bounds[fractional_index][1])

        node_queue.append({'A_eq': A_eq, 'b_eq': b_eq, 'bounds': lower_bounds})
        node_queue.append({'A_eq': A_eq, 'b_eq': b_eq, 'bounds': upper_bounds})

    if best_solution is not None:
        return {
            'solution': np.round(best_solution).astype(int).tolist(),
            'objective_value': best_value,
            'branches': branches  # Include branch details in the output
        }
    else:
        return {
            'status': 'Infeasible',
            'branches': branches  # Include branch details even if infeasible
        }

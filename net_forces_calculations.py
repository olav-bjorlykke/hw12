import numpy as np

velocitys = [0.0, 0.13, 0.25, 0.37, 0.5, 0.63, 0.75]
Cd = 1
alpha = 0
v = 1.75
h = 1.55
t = 2.42 * 10**(-3)
w = 25.5 * 10**(-3)
rho = 1025
mg = 9.6/2 * 9.81

def calculate_fixed_net_forces(velocitys):
    global  Cd, v, h, t, w, rho
    forces_given_velocitys = []
    for U in velocitys:
        Fd = (rho * v * h * Cd * U**2) * (t/w)
        forces_given_velocitys.append(2 * Fd)
    return forces_given_velocitys
def calculate_alpha_u_pair(U, alpha):
    global Cd, v, h, t, w, rho, mg
    sin_alpha = (
            (
            0.5 * rho * v * h * (t / w) * Cd * (U ** 2) *
            ((np.cos(alpha) ** 3 + 1) + (np.cos(alpha) ** 2) * np.sin(alpha))
            ) / (2 * mg)
    )

    alpha_estimate = np.arcsin(sin_alpha)

    return alpha_estimate
def estimate_alpha(U):
    alpha_guess = 1.42  #Starts by assuming an angle of almost 90 degrees to avoid runtime errors
    estimated_alpha = calculate_alpha_u_pair(U, alpha_guess)
    threshold = 0.005
    while np.abs(alpha_guess - estimated_alpha) > threshold:
        alpha_guess = estimated_alpha
        estimated_alpha = calculate_alpha_u_pair(U, alpha_guess)

    return alpha_guess
def estimate_alphas(velocitys):
    return [estimate_alpha(U) for U in velocitys]
def calculate_hinged_net_drag_force(U, alpha):
    global Cd, v, h, t, w, rho
    Fd = 0.5 * rho * v * h * U**2 * (t / w) * (np.cos(alpha)**3 + 1)
    return Fd
def calculate_hinged_net_forces(velocitys):
    alphas = estimate_alphas(velocitys)
    forces = []
    for velocity, alpha in zip(velocitys, alphas):
        Fd = 2 * calculate_hinged_net_drag_force(velocity, alpha)
        forces.append(Fd)

    return forces
def calculate_volumes(velocitys):
    return np.cos(estimate_alphas(velocitys))



if __name__ == '__main__':
    #c
    print(calculate_fixed_net_forces(velocitys))
    print(calculate_hinged_net_forces(velocitys))
    #d and e
    print(calculate_volumes(velocitys))







import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


def perform_linear_regression(points):
    if len(points) < 2:
        return None

    points_array = np.array(points)
    x_vals = points_array[:, 0]
    y_vals = points_array[:, 1]

    slope, intercept, r_value, p_value, std_err = linregress(x_vals, y_vals)
    r_squared = r_value**2

    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "std_err": std_err,
        "x_vals": x_vals,
        "y_vals": y_vals,
    }


def generate_calibration_plot(x_vals, y_vals, slope, intercept):
    fig, ax = plt.subplots()
    ax.scatter(x_vals, y_vals, label="Pontos de Calibração")

    line_x = np.linspace(min(x_vals) * 0.9, max(x_vals) * 1.1, 100)
    line_y = slope * line_x + intercept

    ax.plot(line_x, line_y, label="Linha de Regressão", color="red")
    ax.set_xlabel("Concentração (X)")
    ax.set_ylabel("Sinal (Y)")
    ax.set_title("Curva de Calibração")
    ax.legend()
    ax.grid(True)

    return fig


def calculate_recovery(slope, intercept, s_inicial, recovery_points):
    if slope == 0:
        return []

    results_data = []
    c_inicial = (s_inicial - intercept) / slope

    for point in recovery_points:
        c_padrao = point["c_padrao"]
        s_final = point["s_final"]

        c_final = (s_final - intercept) / slope
        c_recuperado = c_final - c_inicial
        recuperacao = (c_recuperado / c_padrao) * 100

        results_data.append(
            {
                "C. Padrão Adicionado": c_padrao,
                "Sinal Final": s_final,
                "C. Recuperado": c_recuperado,
                "Recuperação (%)": recuperacao,
            }
        )

    return results_data


def calcular_recuperacao_padrao(slope, intercept, s_inicial, recovery_points):
    results_data = []

    if slope != 0:
        c_inicial = (s_inicial - intercept) / slope
    else:
        return []

    for point in recovery_points:
        c_padrao = point["c_padrao"]
        s_final = point["s_final"]

        c_final_medida = (s_final - intercept) / slope

        c_recuperado = c_final_medida - c_inicial

        if c_padrao > 0:
            recuperacao_percentual = (c_recuperado / c_padrao) * 100
        else:
            recuperacao_percentual = 0

        results_data.append(
            {
                "C. Padrão Adicionado": c_padrao,
                "Sinal Final": s_final,
                "C. Recuperado": c_recuperado,
                "Recuperação (%)": recuperacao_percentual,
            }
        )

    return results_data

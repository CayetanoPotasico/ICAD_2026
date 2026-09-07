import numpy as np
import pandas as pd

def generate_surface_code_dataset(num_samples=50000, p_x=0.01, p_z=0.01, q_measure=0.0):
    """
    Genera el dataset vectorizado.
    p_x: Probabilidad de Bit-Flip
    p_z: Probabilidad de Phase-Flip
    q_measure: Probabilidad de error en la medida del síndrome (Ruido Fenomenológico)
    """
    # Errores Físicos
    e_x = np.random.binomial(1, p_x, (num_samples, 25))
    e_z = np.random.binomial(1, p_z, (num_samples, 25))
    
    # Topología (Matrices H_z y H_x)
    z_plaquettes = [[0, 1], [2, 3], [1, 2, 6, 7], [3, 4, 8, 9], [5, 6, 10, 11], [7, 8, 12, 13], [11, 12, 16, 17], [13, 14, 18, 19], [15, 16, 20, 21], [17, 18, 22, 23], [21, 22], [23, 24]]
    H_z = np.zeros((12, 25), dtype=int)
    for i, qubits in enumerate(z_plaquettes): H_z[i, qubits] = 1
        
    x_stars = [[5, 10], [15, 20], [0, 1, 5, 6], [2, 3, 7, 8], [6, 7, 11, 12], [8, 9, 13, 14], [10, 11, 15, 16], [12, 13, 17, 18], [16, 17, 21, 22], [18, 19, 23, 24], [4, 9], [14, 19]]
    H_x = np.zeros((12, 25), dtype=int)
    for i, qubits in enumerate(x_stars): H_x[i, qubits] = 1

    # Cálculo del Síndrome
    S_z = np.dot(e_x, H_z.T) % 2  
    S_x = np.dot(e_z, H_x.T) % 2  
    
    # Canal Ruidoso (Fenomenológico) - Shannon
    if q_measure > 0:
        noise_sz = np.random.binomial(1, q_measure, S_z.shape)
        noise_sx = np.random.binomial(1, q_measure, S_x.shape)
        S_z = (S_z + noise_sz) % 2
        S_x = (S_x + noise_sx) % 2
    
    # Etiquetas Lógicas (Ground Truth real, independiente del ruido de medida)
    logical_z = np.sum(e_z[:, 0:5], axis=1) % 2
    logical_x = np.sum(e_x[:, [0, 5, 10, 15, 20]], axis=1) % 2
    
    logical_error = np.zeros(num_samples, dtype=int)
    logical_error[(logical_x == 1) & (logical_z == 0)] = 1
    logical_error[(logical_x == 0) & (logical_z == 1)] = 2
    logical_error[(logical_x == 1) & (logical_z == 1)] = 3
    
    # Adaptación para Matlab
    dataset = np.hstack((S_x, S_z, logical_error.reshape(-1, 1)))
    cols = [f'Flag_X_{i}' for i in range(12)] + [f'Flag_Z_{i}' for i in range(12)] + ['Logical_Error']

    # Creación del DataFrame
    df_fast = pd.DataFrame(dataset, columns=cols)

    print(f"Dimensiones del Dataset: {df_fast.shape}")
    print("\nDistribución [%] de las clases a predecir (0=OK, 1=Bit-Flip, 2=Phase-Flip, 3=Bit-Flip+Phase-Flip):")
    print(df_fast['Logical_Error'].value_counts(normalize=True) * 100)

    return df_fast

# EJECUCIÓN 1: Escenario Biased (Clases Desbalanceadas, Medidas Perfectas)
df_biased = generate_surface_code_dataset(num_samples=50000, p_x=0.01, p_z=0.05, q_measure=0.0)
df_biased.to_csv('dataset_1_biased.csv', index=False)

# EJECUCIÓN 2: Escenario Canal Ruidoso (Biased + 2% Errores de Medida)
df_noisy = generate_surface_code_dataset(num_samples=50000, p_x=0.01, p_z=0.05, q_measure=0.02)
df_noisy.to_csv('dataset_2_noisy.csv', index=False)

print("Datasets generados!")
import numpy as np
import matplotlib.pyplot as plt

def analyze_fourier_array(data_array, max_harmonic=20, include_zero_order=False):
    signals = data_array[:-1, :]
    num_signals = signals.shape[0]
    num_samples = signals.shape[1]
    n = data_array.shape[0]

    start_idx = 0 if include_zero_order else 1
    num_columns = max_harmonic + 1 if include_zero_order else max_harmonic
    
    result = np.zeros((n, num_columns))
    
    for i in range(num_signals):
        signal = signals[i, :]
        fft_values = np.fft.fft(signal)
        
        amplitudes = np.abs(fft_values) * 2 / num_samples
        amplitudes[0] = amplitudes[0] / 2
        
        result[i, :] = amplitudes[start_idx : max_harmonic + 1]
        
    result[-1, :] = np.arange(start_idx, max_harmonic + 1)
    
    return result

if __name__ == "__main__":
    # 1. Tạo dữ liệu đầu vào
    num_samples = 1000
    theta = np.linspace(0, 2*np.pi, num_samples, endpoint=False)

    # Tín hiệu giả lập có thành phần DC
    signal1 = 0.5 + 1.0 * np.sin(theta) + 0.3 * np.sin(3 * theta) + 0.1 * np.sin(5 * theta)
    signal2 = 0.2 + 1.2 * np.sin(theta) + 0.6 * np.sin(3 * theta) + 0.2 * np.sin(7 * theta)

    data_input = np.vstack((signal1, signal2, theta))

    # 2. Thực hiện phân tích (Bỏ qua bậc 0)
    max_harmonic = 10
    fourier_output = analyze_fourier_array(data_input, max_harmonic, include_zero_order=False)

    harmonics = fourier_output[-1, :]
    amplitudes1 = fourier_output[0, :]
    amplitudes2 = fourier_output[1, :]

    # 3. Vẽ đồ thị
    theta_deg = np.degrees(theta)
    plt.figure(figsize=(12, 10))

    # --- Waveform ---
    plt.subplot(2, 1, 1)
    plt.plot(theta_deg, signal1, label='Signal 1 (DC=0.5)', color='royalblue')
    plt.plot(theta_deg, signal2, label='Signal 2 (DC=0.2)', color='darkorange', linestyle='--')
    plt.title('Original Signals (Spatial Domain)')
    plt.xlabel('Angle (Degrees)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 360)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper right')

    # --- Harmonics ---
    plt.subplot(2, 1, 2)
    plt.bar(harmonics - 0.2, amplitudes1, width=0.4, label='Signal 1', color='royalblue')
    plt.bar(harmonics + 0.2, amplitudes2, width=0.4, label='Signal 2', color='darkorange', alpha=0.8)

    plt.title(f'Harmonic Spectrum (include_zero_order=False)')
    plt.xlabel('Harmonic Order')
    plt.ylabel('Amplitude')
    plt.xticks(harmonics)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    plt.tight_layout()
    plt.show()

    print(f"Matrix Shape: {fourier_output.shape}")
    print(f"Harmonic orders: {fourier_output[-1, :]}")
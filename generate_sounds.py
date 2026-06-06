
import wave
import struct
import math
import os

def generate_tone(filename, frequency, duration, type='sine'):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)

    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)

        for i in range(num_samples):
            t = float(i) / sample_rate
            if type == 'sine':
                value = math.sin(2.0 * math.pi * frequency * t)
            elif type == 'noise':
                import random
                value = random.uniform(-1, 1)
            elif type == 'saw':
                value = 2.0 * (t * frequency - math.floor(0.5 + t * frequency))

            # Simple envelope to avoid clicks
            envelope = 1.0
            if i < 1000: envelope = i / 1000.0
            if i > num_samples - 1000: envelope = (num_samples - i) / 1000.0

            sample = int(value * 32767 * envelope * 0.5)
            f.writeframes(struct.pack('<h', sample))

os.makedirs('assets/sounds', exist_ok=True)

# Sizzling (Noise)
generate_tone('assets/sounds/cook.wav', 440, 1.0, 'noise')
# Chopping (Short burst)
generate_tone('assets/sounds/cut.wav', 100, 0.1, 'saw')
# Fire (Low noise)
generate_tone('assets/sounds/fire.wav', 50, 2.0, 'noise')
# Interact
generate_tone('assets/sounds/interact.wav', 880, 0.1, 'sine')
# Success
generate_tone('assets/sounds/success.wav', 440, 0.5, 'sine')
# Fail
generate_tone('assets/sounds/fail.wav', 220, 0.5, 'saw')

print("Sounds generated.")

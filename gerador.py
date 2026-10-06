"""Gera tons de teste para conferir as barras de frequência do decibelímetro."""

import io
import math
import sys
import wave
from array import array

import winsound


SAMPLE_RATE = 48_000
DURATION_SECONDS = 5
AMPLITUDE = 0.3
BAND_CENTERS = (
    5.5,
    55,
    550,
    1500,
    3000,
    6000,
    9000,
    11000,
    13000,
    15000,
    17000,
    19000,
    21000,
    23000,
)


def parse_frequency(text: str) -> float:
    """Converte uma frequência digitada com ponto ou vírgula decimal."""
    frequency = float(text.strip().replace(",", "."))
    if not math.isfinite(frequency) or frequency <= 0:
        raise ValueError("A frequência deve ser um número maior que zero.")
    if frequency >= SAMPLE_RATE / 2:
        raise ValueError(
            f"A frequência deve ser menor que {SAMPLE_RATE / 2:g} Hz "
            "(limite de Nyquist do sinal gerado)."
        )
    return frequency


def make_tone(frequency: float) -> bytes:
    """Cria um WAV PCM mono de cinco segundos para reprodução no Windows."""
    sample_count = SAMPLE_RATE * DURATION_SECONDS
    samples = array(
        "h",
        (
            round(
                AMPLITUDE
                * 32767
                * math.sin(2 * math.pi * frequency * index / SAMPLE_RATE)
            )
            for index in range(sample_count)
        ),
    )
    if sys.byteorder != "little":
        samples.byteswap()

    audio = io.BytesIO()
    with wave.open(audio, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(samples.itemsize)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(samples.tobytes())
    return audio.getvalue()


def main() -> None:
    print("Gerador de tons para teste das barras do decibelímetro")
    print("Digite uma frequência em Hz (ponto ou vírgula decimal; sem escrever Hz).")
    print("Cada tom toca por 5 segundos. Pressione Enter sem digitar para sair.")
    print("Centros das 14 faixas (Hz): " + ", ".join(f"{value:g}" for value in BAND_CENTERS))
    print("Use volume moderado e não aproxime o alto-falante do microfone.")

    while True:
        try:
            text = input("\nFrequência: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if not text:
            break

        try:
            frequency = parse_frequency(text)
        except ValueError as error:
            print(f"Frequência inválida: {error}")
            continue

        print(f"Tocando {frequency:g} Hz por {DURATION_SECONDS} segundos...")
        winsound.PlaySound(make_tone(frequency), winsound.SND_MEMORY)
        print("Tom concluído.")


if __name__ == "__main__":
    main()

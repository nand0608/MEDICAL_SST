import json
import re
import pyaudio
from vosk import Model, KaldiRecognizer


MODEL_PATH = "model/vosk-model-small-en-us-0.15"
GRAMMAR_PATH = "grammar/medical_grammar.json"


def load_grammar():
    with open(GRAMMAR_PATH, "r") as f:
        return json.load(f)["phrases"]


def normalize_numbers(text: str) -> str:
    tokens = text.split()
    result = []
    i = 0

    while i < len(tokens):
        
        if (
            i + 1 < len(tokens)
            and tokens[i].isdigit()
            and tokens[i + 1] == "100"
        ):
            result.append(str(int(tokens[i]) * 100))
            i += 2
            continue

       
        if (
            i + 1 < len(tokens)
            and tokens[i].isdigit()
            and tokens[i + 1] in {"1000", "100000"}
        ):
            result.append(str(int(tokens[i]) * int(tokens[i + 1])))
            i += 2
            continue

        result.append(tokens[i])
        i += 1

    return " ".join(result)


def medical_replacements(text: str) -> str:
    text = text.lower()

    replacements = {
        # ---- FOOD ----
        r"\bbefore food\b": "BF",
        r"\bafter food\b": "AF",
        r"\bwith food\b": "WF",
        r"\bon empty stomach\b": "ES",

        # ---- FREQUENCY ----
        r"\bonce daily\b": "OD",
        r"\bone time a day\b": "OD",
        r"\btwice daily\b": "BD",
        r"\btwo times a day\b": "BD",
        r"\bthrice daily\b": "TDS",
        r"\bthree times a day\b": "TDS",
        r"\bfour times a day\b": "QID",

        # ---- TIMING ----
        r"\bin the morning\b": "morning",
        r"\bat night\b": "night",
        r"\bbefore bedtime\b": "HS",

        # ---- DOSAGE FORM ----
        r"\btablet\b": "tab",
        r"\bcapsule\b": "cap",
        r"\bsyrup\b": "syp",
        r"\binjection\b": "inj",
        r"\bdrops\b": "gtt",

        # ---- UNITS ----
        r"\bmilligram\b": "mg",
        r"\bmilligrams\b": "mg",
        r"\bmilliliter\b": "ml",
        r"\bmilliliters\b": "ml",
        r"\bunits\b": "IU",

        # ---- SPECIAL ----
        r"\bas needed\b": "SOS",
        r"\bif required\b": "PRN"
    }

    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    # ---- WORD → DIGIT ----
    word_to_digit = {
        "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8",
        "nine": "9", "ten": "10",
        "hundred": "100",
        "thousand": "1000"
    }

    for word, digit in word_to_digit.items():
        text = re.sub(rf"\b{word}\b", digit, text)

    
    text = normalize_numbers(text)

    text = re.sub(r"\s+", " ", text).strip()
    return text.capitalize()

def main():
    model = Model(MODEL_PATH)
    grammar = load_grammar()

    recognizer = KaldiRecognizer(
        model,
        16000,
        json.dumps(grammar)
    )
    recognizer.SetWords(True)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000
    )

    stream.start_stream()
    print("🎙️ Speak prescription now (Ctrl+C to stop)\n")

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                res = json.loads(recognizer.Result())
                text = res.get("text", "")
                if text:
                    final_text = medical_replacements(text)
                    print("🩺 Prescription:", final_text)

    except KeyboardInterrupt:
        print("\n🛑 Stopped")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    main()

import os

def load_transcripts(directory: str):
    transcripts = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            path = os.path.join(directory, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    transcripts.append(f.read())
            except Exception as e:
                print(f"Skipping {file}: {e}")
    return transcripts

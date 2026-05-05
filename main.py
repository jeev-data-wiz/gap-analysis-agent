import typer
import json
from utils.file_loader import load_transcripts
from agents.requirements_agent import extract_requirements
from agents.solution_agent import extract_solutions
from agents.gap_agent import analyze_gaps

app = typer.Typer()

@app.command()
def run(
    business: str,
    engineering: str,
    output: str
):
    business_data = load_transcripts(business)
    engineering_data = load_transcripts(engineering)

    requirements = extract_requirements(business_data)
    solutions = extract_solutions(engineering_data)
    gaps = analyze_gaps(requirements, solutions)

    with open(output, "w") as f:
        json.dump(gaps, f, indent=2)

    print("Report generated:", output)

if __name__ == "__main__":
    app()

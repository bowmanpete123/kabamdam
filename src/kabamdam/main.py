import os
import re
from pathlib import Path
import typer
from kabamdam.parser import RoadmapParser
from kabamdam.svg_generator import SVGGenerator

app = typer.Typer(help="KABAMDAM: Visualise project status as code.")


def get_relative_path(from_path: Path, to_path: Path) -> str:
    """Calculates relative path from a README file to an asset."""
    # Ensure absolute for calculation
    abs_from = from_path.resolve()
    abs_to = to_path.resolve()

    # Path.relative_to needs one to be a parent of another, or use os.path.relpath
    rel = os.path.relpath(abs_to, abs_from.parent)
    return rel


def update_readme(
    readme_path: Path, svg_path: Path, roadmap_path: Path, timesheet_path: Path
):
    """Injects SVG and links into README between markers."""
    if not readme_path.exists():
        return

    content = readme_path.read_text()
    start_marker = "<!-- KABAMDAM:START -->"
    end_marker = "<!-- KABAMDAM:END -->"

    if start_marker not in content or end_marker not in content:
        if start_marker in content or end_marker in content:
            typer.echo(
                f"Error: Incomplete KABAMDAM markers in {readme_path}.", err=True
            )
            raise typer.Exit(code=1)
        typer.echo(
            f"Warning: Markers {start_marker} and {end_marker} not found in {readme_path}. No update performed."
        )
        return

    # Calculate relative paths for the README injection
    rel_svg = get_relative_path(readme_path, svg_path)
    rel_roadmap = get_relative_path(readme_path, roadmap_path)
    rel_timesheet = get_relative_path(readme_path, timesheet_path)

    new_block = (
        f"{start_marker}\n"
        f"![Status Heatmap]({rel_svg})\n\n"
        f"[Roadmap]({rel_roadmap}) | [Timesheets]({rel_timesheet})\n"
        f"{end_marker}"
    )

    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
    new_content = re.sub(pattern, new_block, content, flags=re.DOTALL)

    readme_path.write_text(new_content)
    typer.echo(f"Successfully updated {readme_path} with latest roadmap status.")


@app.command()
def main(
    roadmap_file: Path = typer.Option(
        "docs/roadmap/ROADMAP.md", help="Path to ROADMAP.md"
    ),
    timesheet_file: Path = typer.Option("timesheets.md", help="Path to timesheets.md"),
    readme_file: Path = typer.Option("README.md", help="Path to README.md"),
    output_svg: Path = typer.Option(
        "docs/roadmap/status.svg", help="Output path for SVG"
    ),
):
    """Parse roadmap and timesheets, generate SVG, and update README."""

    if not roadmap_file.exists():
        typer.echo(f"Error: Roadmap file '{roadmap_file}' not found.", err=True)
        raise typer.Exit(code=2)

    # 1. Parse Data
    try:
        roadmap_tasks = RoadmapParser().parse_file(roadmap_file)
        # Timesheet parsing is optional for basic SVG but good for detailed logs
        # For now, we mainly use the roadmap for the heatmap
    except Exception as e:
        typer.echo(f"Error parsing roadmap: {e}", err=True)
        raise typer.Exit(code=1)

    # 2. Generate SVG
    try:
        generator = SVGGenerator()
        svg_content = generator.generate(roadmap_tasks)

        # Ensure directory exists
        output_svg.parent.mkdir(parents=True, exist_ok=True)
        output_svg.write_text(svg_content)
    except Exception as e:
        typer.echo(f"Error generating SVG: {e}", err=True)
        raise typer.Exit(code=1)

    # 3. Update README
    update_readme(readme_file, output_svg, roadmap_file, timesheet_file)


if __name__ == "__main__":
    app()

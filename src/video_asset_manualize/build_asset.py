"""
CLI Interface for building training assets.
"""

import json
from pathlib import Path
import typer
from rich.console import Console

from .build_training_asset_pipeline import BuildTrainingAssetPipeline
from .settings import settings

app = typer.Typer(help="VideoAsset Manualize - Convert training videos to structured assets")
console = Console()


@app.command()
def build(
    input_file: Path = typer.Argument(..., help="Path to input training_asset_spec.json"),
    output_dir: Path = typer.Option(settings.EXPORTS_DIR, "--output", "-o", help="Output directory"),
):
    """Build training assets from JSON specification."""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file not found: {input_file}[/red]")
        raise typer.Exit(code=1)
    
    pipeline = BuildTrainingAssetPipeline()
    
    try:
        console.print(f"[cyan]Loading: {input_file}[/cyan]")
        if not pipeline.load_spec(input_file):
            console.print("[yellow]Warning: Validation failed but continuing[/yellow]")
        else:
            console.print("[green]✓ Validation passed[/green]")
        
        console.print(f"[cyan]Generating outputs to: {output_dir}[/cyan]")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        asset_id = pipeline.spec.get("asset_meta", {}).get("asset_id", "asset")
        
        html_file = output_dir / f"{asset_id}_manual.html"
        pipeline.generate_html(html_file)
        console.print(f"[green]✓[/green] Generated HTML: {html_file}")
        
        pdf_file = output_dir / f"{asset_id}_manual.pdf"
        pipeline.generate_pdf(pdf_file)
        console.print(f"[green]✓[/green] Generated PDF: {pdf_file}")
        
        console.print(f"[green bold]\n✓ Build completed successfully![/green bold]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def validate(input_file: Path = typer.Argument(..., help="Path to training_asset_spec.json")):
    """Validate JSON against schema."""
    
    if not input_file.exists():
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        raise typer.Exit(code=1)
    
    pipeline = BuildTrainingAssetPipeline()
    
    try:
        console.print(f"[cyan]Validating: {input_file}[/cyan]")
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        pipeline.validator.validate(data)
        console.print("[green bold]✓ Validation passed![/green bold]")
        
    except Exception as e:
        console.print(f"[red]Validation Error: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

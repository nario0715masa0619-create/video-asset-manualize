"""
VideoAsset Manualize - CLI Build Asset Command
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def validate(
    input_file: str = typer.Argument(..., help="JSON file to validate"),
):
    """Validate a JSON file against schema."""
    from video_asset_manualize.schema_validator import SchemaValidator
    
    validator = SchemaValidator()
    try:
        validator.validate_file(input_file)
        console.print(f"[green]✓ Validation passed: {input_file}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Validation failed: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def build(
    input_file: str = typer.Argument(..., help="training_asset_spec.json file path"),
    output_dir: str = typer.Option("output/exports", help="output directory"),
    format: str = typer.Option("all", help="html, pdf, or all"),
):
    """Build HTML/PDF manuals from training_asset_spec.json."""
    from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline
    
    console.print("[cyan]📋 VideoAsset Manualize - Build Pipeline[/cyan]")
    console.print(f"Input file: {input_file}")
    
    try:
        pipeline = BuildTrainingAssetPipeline()
        results = pipeline.generate_outputs(input_file, output_dir=output_dir, format=format)
        
        result_table = Table(title="Generated Files")
        result_table.add_column("File Type", style="cyan")
        result_table.add_column("Path", style="green")
        
        for file_type, file_path in results.items():
            if file_path:
                result_table.add_row(file_type, str(file_path))
        
        console.print(result_table)
        console.print(f"\n[green]✅ Build completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def extract(
    input_file: str = typer.Argument(..., help="source_evidence.json file path"),
    output_dir: str = typer.Option("output/exports", help="output directory"),
    output_name: str = typer.Option("extracted_spec.json", help="output file name"),
    use_llm: bool = typer.Option(False, "--use-llm", help="Enable LLM-based extraction"),
    llm_provider: str = typer.Option("dummy", "--llm-provider", help="LLM provider (dummy|openai)"),
):
    """Extract training_asset_spec from source_evidence.json (Phase 2/6)."""
    from video_asset_manualize.source_evidence_validator import SourceEvidenceValidator
    from video_asset_manualize.source_evidence_to_training_asset_builder import (
        SourceEvidenceToTrainingAssetBuilder,
    )
    from video_asset_manualize.llm_training_asset_builder import LLMTrainingAssetBuilder
    from video_asset_manualize.provider_factory import ProviderFactory
    import json
    
    # Validate input file exists
    input_path = Path(input_file)
    if not input_path.exists():
        console.print(f"[red]❌ Error: Input file not found: {input_file}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]📋 Phase 2/6 Extraction Pipeline[/cyan]")
    console.print(f"Input file: {input_path.absolute()}")
    
    try:
        # Step 1: Validate source_evidence
        console.print("[yellow]🔍 Step 1/3: Validating source_evidence schema...[/yellow]")
        validator = SourceEvidenceValidator()
        validator.validate_file(str(input_path))
        console.print("[green]✓ Schema validation passed[/green]")
        
        # Step 2: Build training_asset_spec
        console.print("[yellow]📝 Step 2/3: Building training_asset_spec...[/yellow]")
        
        if use_llm:
            # Use LLM-based extraction
            console.print(f"[cyan]  Using LLM provider: {llm_provider}[/cyan]")
            llm_provider_obj = ProviderFactory.create_llm_provider(provider_type=llm_provider)
            builder = LLMTrainingAssetBuilder(llm_provider=llm_provider_obj)
            spec = builder.build_from_file(str(input_path))
        else:
            # Use standard extraction
            builder = SourceEvidenceToTrainingAssetBuilder()
            spec = builder.build_from_file(str(input_path))
        
        console.print("[green]✓ Spec built successfully[/green]")
        
        # Step 3: Save spec
        console.print("[yellow]💾 Step 3/3: Saving spec...[/yellow]")
        output_path = Path(output_dir) / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
        
        console.print("[green]✓ Spec saved[/green]")
        
        # Display summary
        asset_id = spec.get('asset_meta', {}).get('asset_id', 'unknown')
        title = spec.get('asset_meta', {}).get('title', 'Untitled')
        
        summary_table = Table(title="Extraction Result")
        summary_table.add_column("Field", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_row("Input file", str(input_path.absolute()))
        summary_table.add_row("Output file", str(output_path.absolute()))
        summary_table.add_row("Asset ID", asset_id)
        summary_table.add_row("Title", title)
        summary_table.add_row("Extraction mode", "LLM" if use_llm else "Standard")
        
        console.print(summary_table)
        console.print(f"\n[green]✅ Phase 2/6 extraction completed successfully![/green]")
        console.print(f"[cyan]Next step: python -m video_asset_manualize.build_asset build {output_path}[/cyan]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def video(
    input_file: str = typer.Argument(..., help="video file path"),
    output_dir: str = typer.Option("output/exports", help="output directory"),
    output_name: str = typer.Option("extracted_source_evidence.json", help="output file name"),
    provider: str = typer.Option("dummy", help="transcript provider (dummy|whisper)"),
    whisper_model: str = typer.Option("base", help="Whisper model size"),
    ocr_provider: str = typer.Option("dummy", help="OCR provider (dummy|easyocr)"),
    ocr_gpu: bool = typer.Option(False, help="Enable GPU for OCR"),
):
    """Extract source_evidence from video file (Phase 3/5)."""
    from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
    from video_asset_manualize.settings import settings
    import json
    
    input_path = Path(input_file)
    if not input_path.exists():
        console.print(f"[red]❌ Error: Input video not found: {input_file}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]🎬 Video to Source Evidence Pipeline[/cyan]")
    console.print(f"Input video: {input_path.absolute()}")
    
    try:
        # Temporarily set provider settings
        settings.TRANSCRIPT_PROVIDER_TYPE = provider
        settings.WHISPER_MODEL = whisper_model
        settings.OCR_PROVIDER_TYPE = ocr_provider
        settings.EASYOCR_GPU = ocr_gpu
        
        console.print("[yellow]🔍 Extracting source evidence...[/yellow]")
        builder = VideoSourceEvidenceBuilder()
        source_evidence = builder.build_from_video(str(input_path))
        
        output_path = Path(output_dir) / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(source_evidence, f, ensure_ascii=False, indent=2)
        
        # Summary
        transcript_count = len(source_evidence.get('transcript_segments', []))
        ocr_count = len(source_evidence.get('ocr_segments', []))
        
        summary_table = Table(title="Video Extraction Result")
        summary_table.add_column("Field", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_row("Input file", str(input_path.absolute()))
        summary_table.add_row("Output file", str(output_path.absolute()))
        summary_table.add_row("Transcript segments", str(transcript_count))
        summary_table.add_row("OCR segments", str(ocr_count))
        summary_table.add_row("Transcript provider", provider)
        summary_table.add_row("OCR provider", ocr_provider)
        
        console.print(summary_table)
        console.print(f"[green]✅ Video extraction completed![/green]")
        console.print(f"[cyan]Next step: python -m video_asset_manualize.build_asset extract {output_path}[/cyan]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)




@app.command()
def batch_specs(
    manifest_file: str = typer.Argument(..., help="specs_manifest.json file path"),
    output_dir: str = typer.Option("output/exports", help="output directory"),
):
    """Build HTML/PDF from multiple training_asset_spec files (batch)."""
    from video_asset_manualize.batch_manifest_loader import BatchManifestLoader
    from video_asset_manualize.batch_pipeline import BatchPipeline
    
    console.print("[cyan]📋 Batch Spec Build Pipeline[/cyan]")
    console.print(f"Manifest: {manifest_file}")
    
    try:
        # Load manifest
        console.print("[yellow]📂 Loading specs manifest...[/yellow]")
        project_id, title, specs = BatchManifestLoader.load_specs_manifest(manifest_file)
        
        # Validate
        valid_specs, errors = BatchManifestLoader.validate_items(specs)
        
        if errors:
            console.print(f"[yellow]⚠ {len(errors)} items failed validation[/yellow]")
            for idx, err in errors:
                console.print(f"  [red]- Item {idx}: {err}[/red]")
        
        console.print(f"[green]✓ {len(valid_specs)}/{len(specs)} items valid[/green]")
        
        # Process
        console.print("[yellow]🔨 Building specs...[/yellow]")
        pipeline = BatchPipeline()
        report, outputs = pipeline.process_specs_batch(valid_specs, output_dir)
        
        # Display results
        result_table = Table(title="Batch Spec Build Results")
        result_table.add_column("Status", style="cyan")
        result_table.add_column("Count", style="green")
        result_table.add_row("Total", str(report.total))
        result_table.add_row("Succeeded", str(report.succeeded))
        result_table.add_row("Failed", str(report.failed))
        
        console.print(result_table)
        
        # Save report
        report_file = Path(output_dir) / "batch_report.json"
        report.save(str(report_file))
        console.print(f"[green]✓ Report saved: {report_file}[/green]")
        
        console.print(f"\n[green]✅ Batch build completed![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def booklet_build(
    specs_manifest: str = typer.Argument(..., help="specs_manifest.json file path"),
    output_dir: str = typer.Option("output/exports", help="output directory"),
    project_id: str = typer.Option("booklet-project", help="project ID"),
    project_title: str = typer.Option("Training Booklet", help="project title"),
):
    """Build a compiled booklet from multiple training_asset_spec files."""
    from video_asset_manualize.batch_manifest_loader import BatchManifestLoader
    from video_asset_manualize.compiled_training_asset_builder import CompiledTrainingAssetBuilder
    from video_asset_manualize.booklet_html_renderer import BookletHTMLRenderer
    from video_asset_manualize.booklet_pdf_renderer import BookletPDFRenderer
    import json
    
    console.print("[cyan]📚 Booklet Build Pipeline[/cyan]")
    console.print(f"Manifest: {specs_manifest}")
    
    try:
        # Load manifest
        console.print("[yellow]📂 Loading specs manifest...[/yellow]")
        _, _, specs = BatchManifestLoader.load_specs_manifest(specs_manifest)
        
        # Validate
        valid_specs, errors = BatchManifestLoader.validate_items(specs)
        console.print(f"[green]✓ {len(valid_specs)}/{len(specs)} items valid[/green]")
        
        # Load spec JSONs
        console.print("[yellow]📖 Loading spec files...[/yellow]")
        spec_dicts = []
        for spec_item in valid_specs:
            with open(spec_item.spec_path, 'r', encoding='utf-8') as f:
                spec_dicts.append(json.load(f))
        
        console.print(f"[green]✓ Loaded {len(spec_dicts)} specs[/green]")
        
        # Compile
        console.print("[yellow]🔗 Compiling specs...[/yellow]")
        compiled = CompiledTrainingAssetBuilder.compile_specs(
            spec_dicts,
            project_id=project_id,
            title=project_title,
            description="Compiled Training Manual"
        )
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save compiled
        compiled_file = output_path / f"{project_id}_compiled.json"
        compiled.save(str(compiled_file))
        console.print(f"[green]✓ Compiled spec saved: {compiled_file}[/green]")
        
        # Render HTML
        console.print("[yellow]🎨 Rendering HTML booklet...[/yellow]")
        html_renderer = BookletHTMLRenderer()
        html_file = output_path / f"{project_id}_booklet.html"
        html_renderer.render_to_file(compiled, str(html_file))
        console.print(f"[green]✓ HTML booklet: {html_file}[/green]")
        
        # Render PDF
        console.print("[yellow]📄 Rendering PDF booklet...[/yellow]")
        pdf_renderer = BookletPDFRenderer()
        pdf_file = output_path / f"{project_id}_booklet.pdf"
        pdf_renderer.render_to_file(compiled, str(pdf_file))
        console.print(f"[green]✓ PDF booklet: {pdf_file}[/green]")
        
        # Summary
        result_table = Table(title="Booklet Build Results")
        result_table.add_column("Output", style="cyan")
        result_table.add_column("Path", style="green")
        result_table.add_row("Compiled JSON", str(compiled_file))
        result_table.add_row("HTML Booklet", str(html_file))
        result_table.add_row("PDF Booklet", str(pdf_file))
        
        console.print(result_table)
        console.print(f"\n[green]✅ Booklet build completed![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

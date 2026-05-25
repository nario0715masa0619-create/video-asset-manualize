"""
Phase 7 build_asset.py 拡張スクリプト
"""

from pathlib import Path

build_asset_file = Path("src/video_asset_manualize/build_asset.py")
content = build_asset_file.read_text(encoding='utf-8')

# batch-specs コマンドを追加
batch_specs_command = '''

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
        
        console.print(f"\\n[green]✅ Batch build completed![/green]")
        
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
        console.print(f"\\n[green]✅ Booklet build completed![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)
'''

# if __name__ == "__main__": の前に追加
if 'if __name__ == "__main__":' in content:
    content = content.replace('if __name__ == "__main__":', batch_specs_command + '\n\nif __name__ == "__main__":')
else:
    content += batch_specs_command

build_asset_file.write_text(content, encoding='utf-8')
print("OK: build_asset.py extended with batch-specs and booklet-build commands")

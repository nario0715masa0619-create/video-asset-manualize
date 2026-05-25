"""
Phase 6 build_asset 拡張スクリプト
"""

from pathlib import Path
import re

build_asset_file = Path("src/video_asset_manualize/build_asset.py")
content = build_asset_file.read_text(encoding='utf-8')

# 既存の extract コマンドを確認
if "@app.command()" in content and "def extract(" in content:
    # 古い extract コマンドを探して置き換え
    extract_pattern = r'@app\.command\(\)\s+def extract\([^)]*\):[^}]+?(?=@app\.command\(\)|if __name__)'
    
    new_extract_command = '''@app.command()
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
    
    console = Console()
    
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
        
        from video_asset_manualize.training_asset_spec_builder import TrainingAssetSpecBuilder
        builder_out = TrainingAssetSpecBuilder()
        with open(output_path, 'w', encoding='utf-8') as f:
            import json
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
        console.print(f"\\n[green]✅ Phase 2/6 extraction completed successfully![/green]")
        console.print(f"[cyan]Next step: python -m video_asset_manualize.build_asset build {output_path}[/cyan]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


'''
    
    # 置き換え
    content = re.sub(extract_pattern, new_extract_command, content, flags=re.DOTALL)
    build_asset_file.write_text(content, encoding='utf-8')
    print("✓ Updated: src/video_asset_manualize/build_asset.py (extract command extended with --use-llm)")
else:
    print("⚠ extract command not found")

print("\n✅ build_asset.py の extract コマンドが --use-llm オプションで拡張されました")

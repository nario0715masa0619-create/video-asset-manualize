"""
build_asset.py の構文エラーを修正
"""

from pathlib import Path

build_asset_path = Path("src/video_asset_manualize/build_asset.py")

# ファイルを読み込み
with open(build_asset_path, "r", encoding="utf-8") as f:
    content = f.read()

# 問題のある部分を特定して修正
# line 136 周辺の unterminated string を探す
lines = content.split("\n")

# 簡単な修正：最後の if __name__ 部分を確認
if_name_pos = -1
for i, line in enumerate(lines):
    if "if __name__" in line:
        if_name_pos = i
        break

print(f"if __name__ は line {if_name_pos} にあります")
print(f"エラーは line 136 です")

# build_asset.py をクリーンに再作成する
new_build_asset = '''"""
VideoAsset Manualize CLI - Build and validate training assets
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .settings import settings
from .schema_validator import SchemaValidator
from .build_training_asset_pipeline import BuildTrainingAssetPipeline
from .source_evidence_validator import SourceEvidenceValidator
from .source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder

app = typer.Typer(help="VideoAsset Manualize CLI")
console = Console()


@app.command()
def validate(
    input_file: str = typer.Argument(..., help="JSON ファイルパス"),
):
    """
    training_asset_spec.json をスキーマに対して検証します
    """
    try:
        console.print(f"[cyan]検証中: {input_file}[/]")
        validator = SchemaValidator()
        validator.validate_file(Path(input_file))
        console.print("[green]✓ 検証成功[/]")
    except Exception as e:
        console.print(f"[red]❌ 検証失敗: {str(e)}[/]")
        raise typer.Exit(code=1)


@app.command()
def build(
    input_file: str = typer.Argument(..., help="training_asset_spec.json ファイルパス"),
    output_dir: str = typer.Option("output/exports", help="出力ディレクトリ"),
    skip_validation: bool = typer.Option(False, help="スキーマ検証をスキップ"),
    format: str = typer.Option("all", help="出力形式: all, html, pdf, json"),
):
    """
    training_asset_spec.json から HTML/PDF マニュアルを生成します (Phase 1)
    """
    try:
        console.print("[bold blue]📋 VideoAsset Manualize - ビルドパイプライン[/]")
        console.print(f"[cyan]入力ファイル: {input_file}[/]")

        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]❌ エラー: {input_file} が見つかりません[/]")
            raise FileNotFoundError(f"{input_file} not found")

        # スキーマ検証
        if not skip_validation:
            console.print("[yellow]🔍 ステップ 1/3: スキーマ検証中...[/]")
            validator = SchemaValidator()
            validator.validate_file(input_path)
            console.print("[green]✓ スキーマ検証: 成功[/]")

        # パイプライン実行
        console.print("[yellow]🔍 ステップ 2/3: HTML/PDF 生成中...[/]")
        pipeline = BuildTrainingAssetPipeline()
        outputs = pipeline.generate_outputs(input_path, Path(output_dir), format=format)
        console.print("[green]✓ HTML/PDF 生成: 成功[/]")

        # 結果表示
        console.print("[yellow]🔍 ステップ 3/3: 結果を表示中...[/]")
        console.print("[bold green]✅ ビルド完了！[/]")

        table = Table(title="生成ファイル")
        table.add_column("ファイル", style="cyan")
        table.add_column("パス", style="green")
        for key, path in outputs.items():
            table.add_row(key, str(path))
        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ エラー: {str(e)}[/]")
        raise typer.Exit(code=1)


@app.command()
def extract(
    input_file: str = typer.Argument(..., help="source_evidence.json ファイルパス"),
    output_dir: str = typer.Option("output/exports", help="出力ディレクトリ"),
    output_name: str = typer.Option("extracted_spec.json", help="出力ファイル名"),
):
    """
    source_evidence.json から training_asset_spec を自動抽出します (Phase 2)
    """
    try:
        console.print("[bold blue]📋 Phase 2: Source Evidence 抽出パイプライン[/]")
        console.print(f"[cyan]入力ファイル: {input_file}[/]")

        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]❌ エラー: {input_file} が見つかりません[/]")
            raise FileNotFoundError(f"{input_file} not found")

        # Step 1: source_evidence を検証
        console.print("[yellow]🔍 ステップ 1/4: source_evidence を検証中...[/]")
        validator = SourceEvidenceValidator()
        validator.validate_file(input_path)
        console.print("[green]✓ source_evidence スキーマ検証: 成功[/]")

        # Step 2: source_evidence から training_asset_spec を抽出
        console.print("[yellow]🔍 ステップ 2/4: training_asset_spec を抽出中...[/]")
        builder = SourceEvidenceToTrainingAssetBuilder()
        builder.load_source_evidence(input_path)
        spec = builder.build_training_asset_spec()
        console.print("[green]✓ training_asset_spec 抽出: 成功[/]")

        # Step 3: 出力ディレクトリ作成
        console.print("[yellow]🔍 ステップ 3/4: 出力ディレクトリを作成中...[/]")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        spec_file = output_path / output_name
        console.print(f"[green]✓ 出力ディレクトリ作成: {output_path}[/]")

        # Step 4: 抽出結果を保存
        console.print("[yellow]🔍 ステップ 4/4: 抽出結果を保存中...[/]")
        builder.save_training_asset_spec(spec_file)
        console.print(f"[green]✓ 保存完了: {spec_file}[/]")

        # 結果サマリー
        console.print("[bold green]✅ Phase 2 抽出完了![/]")
        table = Table(title="処理結果")
        table.add_column("項目", style="cyan")
        table.add_column("値", style="green")
        table.add_row("入力ファイル", str(input_path.absolute()))
        table.add_row("出力ファイル", str(spec_file.absolute()))
        table.add_row("Asset ID", spec.get("asset_meta", {}).get("asset_id", "N/A"))
        table.add_row("タイトル", spec.get("asset_meta", {}).get("title", "N/A"))
        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ エラー: {str(e)}[/]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
'''

# ファイルに書き込み
with open(build_asset_path, "w", encoding="utf-8") as f:
    f.write(new_build_asset)

print("✓ build_asset.py を修正しました")

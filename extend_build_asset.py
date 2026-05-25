"""
Phase 2 拡張用スクリプト - build_asset.py に Phase 2 コマンドを追加
"""

import sys
from pathlib import Path

# build_asset.py を読み込み
build_asset_path = Path("src/video_asset_manualize/build_asset.py")
with open(build_asset_path, "r", encoding="utf-8") as f:
    content = f.read()

# Phase 2 コマンドを追加
phase2_commands = '''

@app.command()
def extract(
    input_file: str = typer.Argument(..., help="source_evidence.json ファイルパス"),
    output_dir: str = typer.Option("output/exports", help="出力ディレクトリ"),
    output_name: str = typer.Option("extracted_spec.json", help="出力ファイル名"),
):
    """
    source_evidence.json から training_asset_spec を自動抽出します (Phase 2)
    """
    from video_asset_manualize.source_evidence_validator import SourceEvidenceValidator
    from video_asset_manualize.source_evidence_to_training_asset_builder import (
        SourceEvidenceToTrainingAssetBuilder
    )
    from rich.console import Console
    from rich.table import Table

    console = Console()

    try:
        # Step 1: source_evidence を検証
        console.print("[bold blue]📋 Phase 2: Source Evidence 抽出パイプライン[/]")
        console.print(f"[cyan]入力ファイル: {input_file}[/]")

        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]❌ エラー: {input_file} が見つかりません[/]")
            raise FileNotFoundError(f"{input_file} not found")

        # source_evidence を検証
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
        console.print("\n[bold green]✅ Phase 2 抽出完了![/]")
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
'''

# コマンド追加前に if __name__ 部分を検出
if "if __name__" in content:
    # if __name__ の前に Phase 2 コマンドを挿入
    insert_pos = content.rfind("if __name__")
    new_content = content[:insert_pos] + phase2_commands + "\n\n" + content[insert_pos:]
else:
    # if __name__ がなければ末尾に追加
    new_content = content + phase2_commands

# ファイルに書き込み
with open(build_asset_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✓ build_asset.py に Phase 2 extract コマンドを追加しました")

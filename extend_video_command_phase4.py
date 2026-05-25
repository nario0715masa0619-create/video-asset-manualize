"""
build_asset.py の video コマンドを拡張
Provider 選択オプションを追加
"""

from pathlib import Path

build_asset_file = Path("src/video_asset_manualize/build_asset.py")

# 現在のコンテンツを読み込み
with open(build_asset_file, "r", encoding="utf-8") as f:
    content = f.read()

# 既存の video コマンドを削除して新しいバージョンに置き換え
# @app.command() def video の部分を探して置き換え
old_video_command_start = content.find("@app.command()\ndef video(")
if old_video_command_start > 0:
    # 次の @app.command() または if __name__ までを見つける
    next_decorator_pos = content.find("\n@app.command()", old_video_command_start + 1)
    if_name_pos = content.find("\nif __name__", old_video_command_start + 1)
    
    # どちらが先に来るかで切り取り位置を決める
    if next_decorator_pos > 0 and (if_name_pos < 0 or next_decorator_pos < if_name_pos):
        end_pos = next_decorator_pos
    elif if_name_pos > 0:
        end_pos = if_name_pos
    else:
        end_pos = len(content)
    
    # 古いコマンドを削除
    content = content[:old_video_command_start] + content[end_pos:]

# 新しい video コマンドを追加
new_video_command = '''
@app.command()
def video(
    input_file: str = typer.Argument(..., help="動画ファイルパス"),
    output_dir: str = typer.Option("output/exports", help="出力ディレクトリ"),
    output_name: str = typer.Option("extracted_source_evidence.json", help="出力ファイル名"),
    provider: str = typer.Option("dummy", help="Transcript provider: dummy or whisper"),
    whisper_model: str = typer.Option("base", help="Whisper model: tiny, base, small, medium, large"),
):
    """
    動画ファイルから source_evidence を抽出します (Phase 3/4)
    
    Examples:
      # ダミー provider で実行
      python -m video_asset_manualize.build_asset video input.mp4
      
      # Whisper で実行
      python -m video_asset_manualize.build_asset video input.mp4 --provider whisper --whisper-model base
    """
    from video_asset_manualize.video_source_evidence_builder import (
        VideoSourceEvidenceBuilder
    )

    try:
        console.print("[bold blue]📹 Phase 3/4: 動画 → Source Evidence パイプライン[/]")
        console.print(f"[cyan]入力ファイル: {input_file}[/]")
        console.print(f"[cyan]Transcript Provider: {provider}[/]")

        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]❌ エラー: {input_file} が見つかりません[/]")
            raise FileNotFoundError(f"{input_file} not found")

        # Step 1: source_evidence を生成
        console.print("[yellow]🔍 ステップ 1/3: 動画から source_evidence を抽出中...[/]")
        
        builder = VideoSourceEvidenceBuilder()
        # Provider 設定を反映
        from video_asset_manualize.settings import settings
        original_provider = settings.TRANSCRIPT_PROVIDER_TYPE
        original_model = settings.WHISPER_MODEL
        
        try:
            settings.TRANSCRIPT_PROVIDER_TYPE = provider
            settings.WHISPER_MODEL = whisper_model
            
            source_evidence = builder.build_from_video(input_path)
            console.print("[green]✓ source_evidence 抽出: 成功[/]")
        finally:
            settings.TRANSCRIPT_PROVIDER_TYPE = original_provider
            settings.WHISPER_MODEL = original_model

        # Step 2: 出力ディレクトリ作成
        console.print("[yellow]🔍 ステップ 2/3: 出力ディレクトリを作成中...[/]")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        evidence_file = output_path / output_name
        console.print(f"[green]✓ 出力ディレクトリ作成: {output_path}[/]")

        # Step 3: source_evidence を保存
        console.print("[yellow]🔍 ステップ 3/3: source_evidence を保存中...[/]")
        builder.save_to_file(evidence_file)
        console.print(f"[green]✓ 保存完了: {evidence_file}[/]")

        # 結果サマリー
        console.print("[bold green]✅ 抽出完了![/]")
        table = Table(title="処理結果")
        table.add_column("項目", style="cyan")
        table.add_column("値", style="green")
        table.add_row("入力ファイル", str(input_path.absolute()))
        table.add_row("出力ファイル", str(evidence_file.absolute()))
        table.add_row("Transcript セグメント", str(len(source_evidence.get("transcript_segments", []))))
        table.add_row("OCR セグメント", str(len(source_evidence.get("ocr_segments", []))))
        table.add_row("Source Video Metadata", "ffprobe" if builder.extract_metadata else "ダミー")
        console.print(table)

        console.print("[cyan]💡 次ステップ:[/]")
        console.print(f"   python -m video_asset_manualize.build_asset extract {evidence_file}")

    except Exception as e:
        console.print(f"[red]❌ エラー: {str(e)}[/]")
        raise typer.Exit(code=1)
'''

# if __name__ の前に新しいコマンドを挿入
if_name_pos = content.rfind("if __name__")
if if_name_pos > 0:
    new_content = content[:if_name_pos] + new_video_command + "\n\n" + content[if_name_pos:]
else:
    new_content = content + "\n" + new_video_command

# ファイルに保存
with open(build_asset_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✓ build_asset.py の video コマンドを拡張しました")

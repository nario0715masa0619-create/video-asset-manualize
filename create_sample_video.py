"""
サンプル動画入力メタデータを作成
実際の動画ファイルの代わりにダミーメタデータで E2E テスト
"""

from pathlib import Path
import json

# サンプル動画メタデータを作成
samples_dir = Path("samples")
samples_dir.mkdir(exist_ok=True)

# 実際の動画ファイルを作成するのは重いので、
# メタデータ用に一時的なダミーファイルを作成
dummy_video = samples_dir / "sample_training_video.mp4"

# 存在しない動画を参照する形で進める方法もあるが、
# ここでは 1 バイトのダミーファイルを作成
dummy_video.write_bytes(b'\x00')

print(f"✓ ダミー動画ファイル作成: {dummy_video}")

# Phase 3 用の video コマンドをテスト
print("\n✅ Phase 3 基盤完成。次ステップは以下:")
print(f"   python -m video_asset_manualize.build_asset video {dummy_video}")

import os
import subprocess
from pathlib import Path

def generate_tts(text, output_file):
    # Ensure absolute path for output_file
    output_file = Path(output_file).absolute()
    cmd = f'powershell -ExecutionPolicy Bypass -File generate_tts.ps1 -text "{text}" -output_file "{output_file}"'
    subprocess.run(cmd, shell=True, check=True)

def create_videos():
    base_dir = Path("samples/real_test_videos")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Fonts
    # We need a font file for drawtext on Windows
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/arial.ttf"
        
    font_path_escaped = font_path.replace(":", "\\:").replace("/", "\\\\")

    # 1. Speech Dominant
    print("Generating speech_dominant...")
    speech_text = "音声のみで説明しています。画面上には特に文字はありません。ステップ１、システムにログインします。ステップ２、パスワードを入力します。完了です。"
    tts_speech_file = base_dir / "temp_speech.wav"
    generate_tts(speech_text, tts_speech_file)
    
    # Create video with audio and blank screen
    cmd1 = (
        f'ffmpeg -y -f lavfi -i color=c=blue:s=1280x720:d=10 -i "{tts_speech_file}" '
        f'-c:v libx264 -c:a aac -shortest "{base_dir / "speech.mp4"}"'
    )
    subprocess.run(cmd1, shell=True, check=True)
    
    # 2. Text Dominant
    print("Generating text_dominant...")
    # 10s video, draw text
    text_content = "手順１：システムにログインする。ユーザーIDとパスワードを入力します。手順２：ダッシュボードから対象のプロジェクトを選択して、設定画面を開きます。"
    cmd2 = (
        f'ffmpeg -y -f lavfi -i color=c=darkgreen:s=1280x720:d=10 '
        f'-vf "drawtext=fontfile=\'{font_path_escaped}\':text=\'Step 1 Login. Step 2 Dashboard. Open settings. This is a text dominant manual without speech.\':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2" '
        f'-c:v libx264 -c:a aac "{base_dir / "text.mp4"}"'
    )
    subprocess.run(cmd2, shell=True, check=True)
    
    # 3. Mixed
    print("Generating mixed...")
    mixed_text = "ここではシステムの使い方を説明します。画面の文字も確認してください。まずは設定を開きます。"
    tts_mixed_file = base_dir / "temp_mixed.wav"
    generate_tts(mixed_text, tts_mixed_file)
    cmd3 = (
        f'ffmpeg -y -f lavfi -i color=c=darkred:s=1280x720:d=10 -i "{tts_mixed_file}" '
        f'-vf "drawtext=fontfile=\'{font_path_escaped}\':text=\'System Manual. 1. Open Settings.\':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2" '
        f'-c:v libx264 -c:a aac -shortest "{base_dir / "mixed.mp4"}"'
    )
    subprocess.run(cmd3, shell=True, check=True)
    
    # 4. Weak Evidence
    print("Generating weak_evidence...")
    cmd4 = (
        f'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=2 '
        f'-c:v libx264 -c:a aac "{base_dir / "weak.mp4"}"'
    )
    subprocess.run(cmd4, shell=True, check=True)
    
    # Cleanup temp wavs
    if tts_speech_file.exists(): os.remove(tts_speech_file)
    if tts_mixed_file.exists(): os.remove(tts_mixed_file)
    print("Video generation complete.")

if __name__ == "__main__":
    create_videos()

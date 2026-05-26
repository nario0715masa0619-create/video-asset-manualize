import asyncio
from video_asset_manualize.ui_pipeline_runner import UIPipelineRunner

runner = UIPipelineRunner()
result = runner.run_single_video_pipeline(
    video_path="samples/sample_training_video.mp4",
    use_llm=False,
    llm_provider="dummy",
    transcript_provider="dummy",
    ocr_provider="dummy"
)
print("Success:", result.success)
if not result.success:
    print("Error:", result.error_message)
else:
    print("Files:", result.files)

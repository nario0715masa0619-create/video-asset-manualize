import traceback
from typer.testing import CliRunner
from video_asset_manualize.build_asset import app

runner = CliRunner()
result = runner.invoke(app, ["video", "samples/sample_training_video.mp4"])
if result.exception:
    traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
else:
    print(result.output)

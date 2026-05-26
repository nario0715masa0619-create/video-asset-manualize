from video_asset_manualize.ui_pipeline_runner import UIPipelineRunner
import json

runner = UIPipelineRunner()

print("--- Testing Batch Specs ---")
batch_res = runner.run_batch_specs("samples/specs_manifest_batch_test.json", "output/exports/batch")
print("Success:", batch_res.success)
print("Message:", batch_res.message)
if not batch_res.success:
    print("Error:", batch_res.error_message)

print("\n--- Testing Booklet Build ---")
booklet_res = runner.run_booklet_build("samples/specs_manifest_batch_test.json", "output/exports/booklet", "test-project", "Test Booklet")
print("Success:", booklet_res.success)
print("Message:", booklet_res.message)
if not booklet_res.success:
    print("Error:", booklet_res.error_message)

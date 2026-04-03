from backend.pipeline import FloorPlanPipeline

pipeline = FloorPlanPipeline()

result = pipeline.run(
    input_path="data/samples/sample.png",
    from_drive=True,
    scale_px_to_m=0.02,
    poppler_path="C:/poppler/Library/bin"  # Windows only
)

print("Final JSON:")
print(result["json"])
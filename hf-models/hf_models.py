import os
import json
from datetime import datetime, timedelta, timezone
from huggingface_hub import HfApi


def main():
    api = HfApi(token=os.environ["HF_TOKEN"])

    models = api.list_models(
        expand=["gguf", "likes", "createdAt", "lastModified", "downloads"],
        num_parameters="min:6B,max:10B",
        sort="created_at"
    )

    with open("hf-out.jsonl", "w") as f:
        for model in models:
            if not model.gguf:
                continue

            ago_6mo = datetime.now(timezone.utc) - timedelta(weeks=26)

            if model.created_at < ago_6mo:
                break

            print(
                json.dumps({
                    "modelId": model.id, 
                    "downloads": model.downloads, 
                    "likes": model.likes, 
                    "gguf": model.gguf,
                    "createdAt": str(model.created_at), 
                    "lastModified": str(model.last_modified)
                }),
                file=f
            )


if __name__ == "__main__":
    main()

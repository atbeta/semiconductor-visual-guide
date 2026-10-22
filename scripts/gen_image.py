"""ComfyUI flux1-dev-fp8 text2image helper (GPU host 192.168.5.103:8188).

Usage:
  python3 scripts/gen_image.py "<prompt>" <prefix> [width] [height]
"""
import json, time, urllib.request, urllib.parse, sys, os, random
BASE = "http://192.168.5.103:8188"
prompt_text = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else "smi_demo"
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1216
h = int(sys.argv[4]) if len(sys.argv) > 4 else 832

wf = {
  "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "flux1-dev-fp8.safetensors"}},
  "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt_text, "clip": ["1", 1]}},
  "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["1", 1]}},
  "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
  "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0],
        "latent_image": ["4", 0], "seed": random.randint(1, 10**12), "steps": 20, "cfg": 1.0,
        "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0}},
  "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
  "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
}
data = json.dumps({"prompt": wf, "client_id": "smi-viz"}).encode()
req = urllib.request.Request(f"{BASE}/prompt", data=data, headers={"Content-Type": "application/json"})
pid = json.load(urllib.request.urlopen(req))["prompt_id"]
print("queued", pid, flush=True)
for i in range(240):
    time.sleep(2)
    hist = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}"))
    if pid in hist:
        outs = hist[pid]["outputs"]
        for node in outs.values():
            for img in node.get("images", []):
                q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""), "type": img.get("type", "output")})
                blob = urllib.request.urlopen(f"{BASE}/view?{q}").read()
                out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", prefix + ".png")
                open(out, "wb").write(blob)
                print("saved", out, len(blob), flush=True)
        break
else:
    print("timeout", flush=True)

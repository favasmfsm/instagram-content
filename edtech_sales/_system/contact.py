import sys, os, glob, subprocess
d = os.path.abspath(sys.argv[1]); pngs = sorted(glob.glob(f"{d}/png/*.png"))
cols = 5; w = 270; h = int(w * 1.25); rows = (len(pngs) + cols - 1) // cols
html = "".join(f'<img src="file://{p}" style="width:{w}px;height:{h}px;margin:4px">' for p in pngs)
out = f"{d}/contact.html"; open(out, "w").write(f'<body style="margin:0;background:#888;width:{cols*(w+8)}px">{html}</body>')
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--hide-scrollbars", "--allow-file-access-from-files",
  f"--window-size={cols*(w+8)},{rows*(h+8)+8}", f"--screenshot={d}/contact.png", f"file://{out}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.remove(out); print(f"{d}/contact.png")

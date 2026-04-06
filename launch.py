import subprocess
print("Running inference.py...")
with open("output.txt", "w") as f:
    subprocess.run(["python", "inference.py"], stdout=f, stderr=f)
print("Done.")

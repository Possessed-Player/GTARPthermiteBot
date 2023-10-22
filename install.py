import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
	
if __name__ == "__main__":
	packages = ("pynput", 
			 	"numpy", 
			 	"pyautogui", 
				"opencv-python")

	for p in packages:
		install(p)
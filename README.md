AI model about testing knowledge

To run this project make sure to install all dependencies in requirement.txt. Create virtuar env and run dependencies:

python3 -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt

NOTE: torch installation might fail, in that case you can replace torch package in requirements.txt with this:
pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

NOTE2: Freezing requirement will replace pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu with the installed torch version.


# ai-agno
agno example

# python 命令
```shell
python -V

python -m venv .venv

.\.venv\Scripts\Activate.ps1 # windows
source .venv/bin/activate # mac

pip install -U pip

pip install -r requirements.txt

pip install -U -r requirements.txt
 
pip list --not-required --format=freeze > requirements.txt

pip list --not-required --format=freeze | cut -d '=' -f 1 > requirements.txt

```

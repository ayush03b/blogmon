# Blogmon Project

## Quick Start

To get the application up and running:

```bash
git clone https://github.com/ayusxhhb/blogmon.git
cd blogmon

### run using docker
docker-compose up --build

### run the app by pasting this in the browser 
localhost:5001
```

## if you don't have docker 
```bash
### install virtual env
brew install virtualenv

### go to terminal and paste this
virtualenv .venv -p python3
source .venv/bin/activate 
git clone https://github.com/ayusxhhb/blogmon.git
cd blogmon
pip install -r requirements.txt

### paste this in the browser
http://127.0.0.1:5000/
```

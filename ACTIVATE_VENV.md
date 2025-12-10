# How to Activate Virtual Environment

## Windows (PowerShell)

### Option 1: Direct Activation
```powershell
# Navigate to backend directory (if not already there)
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Option 2: Using Command Prompt
```cmd
# Navigate to backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate.bat
```

## If You Get Execution Policy Error (PowerShell)

If you see: `"execution of scripts is disabled on this system"`

**Solution 1: Run this command first**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:
```powershell
.\venv\Scripts\Activate.ps1
```

**Solution 2: Use Command Prompt instead**
```cmd
# Open Command Prompt (cmd) instead of PowerShell
cd backend
venv\Scripts\activate.bat
```

## Verify Activation

After activation, you should see `(venv)` at the start of your prompt:

```
(venv) PS C:\Users\HP\Desktop\loanifi\backend>
```

## Install Dependencies

Once activated, install requirements:

```powershell
# Make sure you're in the backend directory with venv activated
pip install -r requirements.txt
```

## Deactivate

To exit the virtual environment:

```powershell
deactivate
```

## Quick Reference

```powershell
# 1. Navigate to backend
cd backend

# 2. Activate venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload
```



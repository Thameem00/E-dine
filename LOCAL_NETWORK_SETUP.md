# Local Network Hosting Guide

## What I've Changed
✅ Updated `settings.py` with `ALLOWED_HOSTS = ['*']` to allow all local network connections

## Steps You Need to Follow

### Step 1: Find Your PC's IP Address
1. Open **Command Prompt** or **PowerShell**
2. Run this command:
   ```
   ipconfig
   ```
3. Look for **IPv4 Address** under your network adapter (usually something like `192.168.x.x`)
4. **Example**: `192.168.1.100` or `192.168.0.105`

### Step 2: Update ALLOWED_HOSTS (Optional but Recommended)
For better security, update `canteen_ordering/settings.py`:

Replace:
```python
ALLOWED_HOSTS = ['*']
```

With (replace `192.168.x.x` with your actual IP):
```python
ALLOWED_HOSTS = ['192.168.1.100', 'localhost', '127.0.0.1']
```

### Step 3: Activate Virtual Environment
```powershell
cd "c:\Users\anand\Downloads\Telegram Desktop\naja\canteen_ordering"
.\clg\Scripts\Activate.ps1
```

### Step 4: Run the Django Development Server on All Network Interfaces
Instead of running on localhost only, run on `0.0.0.0`:

```powershell
python manage.py runserver 0.0.0.0:8000
```

**Output should look like:**
```
Starting development server at http://0.0.0.0:8000/
```

### Step 5: Access from Other Devices on Your Network
From **any device on the same network**, open your browser and go to:

```
http://192.168.x.x:8000/
```

Replace `192.168.x.x` with your PC's actual IP address you found in Step 1.

**Example:**
- If your PC IP is `192.168.1.100`, visit: `http://192.168.1.100:8000/`
- If your PC IP is `192.168.0.105`, visit: `http://192.168.0.105:8000/`

## Testing Locally
You can still access it locally with:
- `http://localhost:8000/`
- `http://127.0.0.1:8000/`
- `http://YOUR_PC_IP:8000/`

## Important Notes
⚠️ **Default `0.0.0.0:8000` only works for development!** Don't use this in production.

⚠️ **Make sure your Windows Firewall allows port 8000:**
- Go to **Windows Defender Firewall** → **Allow an app through firewall**
- Find Python and enable it (or port 8000)

⚠️ **All devices must be on the same WiFi network** for this to work.

## Troubleshooting

### Can't connect from other device?
1. Verify both devices are on the **same network**
2. Check your PC's IP address again with `ipconfig`
3. Make sure port 8000 isn't blocked by firewall
4. Try pinging your PC: `ping 192.168.x.x`

### Connection refused?
- Make sure Django server is running (`python manage.py runserver 0.0.0.0:8000`)
- Check that you're using the correct IP and port

### 404 errors on other devices?
- Might need to add your IP to `ALLOWED_HOSTS` in settings.py
- Current setting `['*']` should work, but try adding your specific IP for security

# Docker Troubleshooting Guide

## Error: "unable to get image" or "cannot connect to dockerDesktopLinuxEngine"

This error means **Docker Desktop is not running**.

---

## 🔧 **SOLUTION - Follow These Steps:**

### Step 1: Start Docker Desktop

**Option A: Automated (Easiest)**
```cmd
start-docker-first.bat
```
This script will:
- Check if Docker is installed
- Start Docker Desktop automatically
- Wait for it to be ready
- Start LoaniFi services

**Option B: Manual**

1. **Find Docker Desktop** in your Windows Start Menu
2. **Click to open** Docker Desktop application
3. **Wait** for the whale icon to appear in system tray (bottom-right)
4. **Wait** for the message "Docker Desktop is running"
5. **Then continue** with the steps below

### Step 2: Verify Docker is Running

```cmd
check-docker.bat
```

This will check:
- ✅ Docker is installed
- ✅ Docker Desktop is running
- ✅ Docker is responding to commands

### Step 3: Start LoaniFi

Once Docker is verified running:

```cmd
run-all.bat
```

---

## 🚨 **Common Issues & Solutions**

### Issue 1: Docker Desktop Won't Start

**Solution:**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Look for "Docker Desktop" in processes
3. If found, end the task
4. Restart Docker Desktop from Start Menu
5. Wait 1-2 minutes for full startup

### Issue 2: "Docker is not installed"

**Solution:**
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Install it (requires restart)
3. Start Docker Desktop
4. Run setup script again

### Issue 3: Docker Says "Starting..." Forever

**Solution:**
1. Close Docker Desktop completely
2. Open Task Manager
3. End all Docker processes:
   - Docker Desktop.exe
   - Docker Desktop Service
   - com.docker.backend.exe
4. Restart Docker Desktop
5. Wait 2-3 minutes

### Issue 4: "WSL 2 installation is incomplete"

**Solution:**
1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart computer
4. Start Docker Desktop

### Issue 5: Docker Requires Login

**Solution:**
1. Click "Sign up" or "Skip" in Docker Desktop
2. You can skip the login for local development
3. Docker will work without an account

---

## ✅ **Verify Docker is Working**

Run these commands in PowerShell/CMD:

```cmd
# Should show Docker version
docker --version

# Should show system info (not error)
docker info

# Should show version
docker compose version

# Should show running containers (may be empty)
docker ps
```

If all these work, Docker is ready!

---

## 🎯 **Quick Reference - Error Messages**

| Error Message | Solution |
|--------------|----------|
| "The system cannot find the file specified" | Start Docker Desktop |
| "Cannot connect to Docker daemon" | Start Docker Desktop |
| "docker-compose not found" | Use `docker compose` (no hyphen) |
| "version is obsolete" | Ignore or update docker-compose.yml |
| "port is already allocated" | Run `kill-port-3000.bat` |
| "permission denied" | Run as Administrator |

---

## 🔄 **Complete Reset Process**

If nothing works, try this complete reset:

```cmd
# 1. Stop all Docker services
docker-compose down

# 2. Close Docker Desktop completely

# 3. Open Task Manager and end all Docker processes

# 4. Restart Docker Desktop

# 5. Wait for "Docker Desktop is running"

# 6. Run verification
check-docker.bat

# 7. Start fresh
run-all.bat
```

---

## 📋 **Pre-flight Checklist**

Before running LoaniFi, ensure:

- [ ] Docker Desktop is installed
- [ ] Docker Desktop is running (whale icon in system tray)
- [ ] `docker info` command works without error
- [ ] You have at least 4GB free disk space
- [ ] You have at least 4GB free RAM
- [ ] Ports 3000, 8000, 5432, 27017, 6379 are free
- [ ] .env file exists with OPENAI_API_KEY

---

## 🆘 **Still Having Issues?**

Try these diagnostic commands:

```cmd
# Check Docker version
docker --version

# Check Docker status (detailed)
docker info

# Check Docker Compose
docker compose version

# Check system resources
docker system df

# Check running containers
docker ps -a

# Check Docker logs
docker-compose logs
```

---

## 💡 **Best Practices**

1. **Always start Docker Desktop first** before running any docker commands
2. **Wait for full startup** - Docker takes 30-60 seconds to fully start
3. **Check the whale icon** in system tray - it should be static, not animated
4. **Use the automated scripts** - they handle most issues automatically
5. **Keep Docker Desktop updated** - helps avoid compatibility issues

---

## 🚀 **Recommended Workflow**

```cmd
# 1. First time setup
start-docker-first.bat

# 2. Daily usage
run-all.bat

# 3. If issues arise
check-docker.bat

# 4. Complete reset if needed
docker-compose down -v
start-docker-first.bat
```

---

## 📞 **Getting More Help**

If you're still stuck:

1. Check Docker Desktop logs:
   - Click Docker icon → Troubleshoot → View logs

2. Check LoaniFi logs:
   ```cmd
   docker-compose logs -f
   ```

3. Check specific service logs:
   ```cmd
   docker-compose logs backend
   docker-compose logs frontend
   ```

4. Restart everything:
   ```cmd
   docker-compose down -v
   docker system prune -a
   start-docker-first.bat
   ```

---

**Remember: 90% of Docker errors are solved by simply starting Docker Desktop!** 🐳



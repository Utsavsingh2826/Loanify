# LoaniFi - Setup Instructions

## Quick Fix for Current Issue

### Problem: Port 3000 is Already in Use

**Windows - Quick Fix:**
```cmd
# Run this to kill the process and start everything
run-all.bat
```

**Mac/Linux - Quick Fix:**
```bash
chmod +x run-all.sh
./run-all.sh
```

### Manual Fix

**Windows:**
```cmd
# 1. Kill process on port 3000
kill-port-3000.bat

# 2. Start services
docker-compose up -d
```

**Mac/Linux:**
```bash
# 1. Kill process on port 3000
chmod +x kill-port-3000.sh
./kill-port-3000.sh

# 2. Start services
docker-compose up -d
```

---

## Problem: Module Type Warning

✅ **FIXED!** The package.json has been updated with `"type": "module"`.

If you still see warnings, the fix is already applied. Just restart the services.

---

## Complete Setup Process

### Option 1: Automated Setup (Recommended)

**Windows:**
```cmd
run-all.bat
```

**Mac/Linux:**
```bash
chmod +x run-all.sh
./run-all.sh
```

This script will:
1. ✅ Check for .env file
2. ✅ Kill processes on ports 3000 and 8000
3. ✅ Check Docker status
4. ✅ Stop existing containers
5. ✅ Start all services
6. ✅ Verify health
7. ✅ Open browser automatically

### Option 2: Manual Setup

1. **Setup Environment**
```bash
# Copy env template
copy env.template .env  # Windows
cp env.template .env    # Mac/Linux

# Edit .env and add your OPENAI_API_KEY
```

2. **Kill Port Conflicts**
```cmd
# Windows
kill-port-3000.bat

# Mac/Linux
chmod +x kill-port-3000.sh
./kill-port-3000.sh
```

3. **Start Services**
```bash
docker-compose up -d --build
```

4. **Wait and Access**
```
Wait 30 seconds for services to start, then access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs
```

---

## Troubleshooting

### Issue: "Port 3000 is already allocated"

**Solution:**
```cmd
# Windows
netstat -ano | findstr :3000
taskkill /F /PID <PID_NUMBER>

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

Or use the automated scripts provided above.

### Issue: "Docker is not running"

**Solution:**
1. Start Docker Desktop
2. Wait for Docker to fully start
3. Run the setup script again

### Issue: Frontend not loading

**Solution:**
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend only
docker-compose restart frontend

# Rebuild if needed
docker-compose up -d --build frontend
```

### Issue: Backend errors

**Solution:**
```bash
# Check if OPENAI_API_KEY is set
cat .env | grep OPENAI_API_KEY  # Mac/Linux
type .env | findstr OPENAI_API_KEY  # Windows

# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Issue: Module type warnings

**Solution:**
The warning has been fixed by adding `"type": "module"` to package.json.
If you still see it, restart the frontend:
```bash
docker-compose restart frontend
```

---

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart backend
docker-compose restart frontend
```

### Stop Services
```bash
# Stop all
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### Check Service Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
# Backend
docker exec -it loanifi_backend bash

# Frontend
docker exec -it loanifi_frontend sh
```

---

## Port Configuration

Default ports used:
- **Frontend**: 3000
- **Backend**: 8000
- **PostgreSQL**: 5432
- **MongoDB**: 27017
- **Redis**: 6379

To change ports, edit `docker-compose.yml`:
```yaml
frontend:
  ports:
    - "3001:3000"  # Change first number only
```

---

## Success Checklist

Before starting:
- [ ] Docker Desktop is running
- [ ] .env file exists with OPENAI_API_KEY
- [ ] Ports 3000 and 8000 are free

After starting:
- [ ] `docker-compose ps` shows all services "Up"
- [ ] http://localhost:3000 loads
- [ ] http://localhost:8000/docs shows API docs
- [ ] No errors in `docker-compose logs`

---

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Check service status: `docker-compose ps`
3. Try clean restart: `docker-compose down -v && docker-compose up -d`
4. Check QUICK_START.md for common issues
5. Review README.md for detailed information

---

## Next Steps

Once everything is running:
1. ✅ Open http://localhost:3000
2. ✅ Start chatting with the AI assistant
3. ✅ Check admin dashboard at /admin
4. ✅ Review DEMO_GUIDE.md for presentation tips

---

**Need a complete reset?**
```bash
docker-compose down -v
docker system prune -a
# Then run setup again
```



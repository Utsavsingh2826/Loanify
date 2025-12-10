# LoaniFi - Quick Start Guide

Get up and running with LoaniFi in 3 simple steps!

## Prerequisites

- Docker Desktop installed and running
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Setup Environment

### Windows
```bash
start.bat
```

### Mac/Linux
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

## Step 2: Start Services

### Automatic (Recommended)
```bash
# Windows
start.bat

# Mac/Linux
./start.sh
```

### Manual
```bash
# Start all services
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

## Step 3: Access Application

Open your browser and navigate to:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:3000/admin

## First Time Using?

### Try the Demo Flow

1. **Open** http://localhost:3000
2. **Start chatting** with the AI assistant
3. Say: *"Hi, I need a personal loan"*
4. Follow the conversation to experience the full flow

### Sample Conversation

```
You: Hi, I need a personal loan
Bot: Hello! I'd be happy to help you with a personal loan...

You: I need 5 lakh rupees for home renovation
Bot: Great! Home renovation is a wonderful investment...

You: I am salaried and earn 80,000 per month
Bot: Excellent! Based on your income...

You: I prefer 36 months tenure
Bot: Perfect! Let me show you your options...
```

## Admin Dashboard

Access analytics and management:

1. Go to http://localhost:3000/admin
2. View conversion funnel
3. Check agent performance
4. Monitor applications

## Troubleshooting

### Services not starting?

```bash
# Check Docker is running
docker --version

# View detailed logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

### Port already in use?

Edit `docker-compose.yml` to change ports:
- Frontend: Change `3000:3000` to `3001:3000`
- Backend: Change `8000:8000` to `8001:8000`

### Backend errors?

Check your OpenAI API key:
```bash
# View current config
cat .env | grep OPENAI_API_KEY

# Make sure it starts with 'sk-'
```

## Stop Services

```bash
docker-compose down

# To also remove data volumes
docker-compose down -v
```

## Useful Commands

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart backend
docker-compose restart frontend

# Rebuild and restart
docker-compose up -d --build

# Stop all services
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

## Next Steps

- 📖 Read the [Demo Guide](DEMO_GUIDE.md) for presentation tips
- 🏗️ Check [Architecture](ARCHITECTURE.md) for technical details
- 📚 Explore [API Documentation](http://localhost:8000/docs) when running

## Need Help?

- Check logs: `docker-compose logs -f`
- View README.md for detailed setup
- Check DEMO_GUIDE.md for demo walkthrough
- Review ARCHITECTURE.md for technical details

## Demo Credentials (if using seed data)

```
Customer Users:
- Email: rajesh.kumar@example.com
- Password: demo123

Admin User:
- Email: admin@loanifi.com
- Password: admin123
```

---

**Ready to revolutionize lending with AI!** 🚀



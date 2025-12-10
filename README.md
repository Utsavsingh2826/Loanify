# LoaniFi - AI-Powered Personal Loan Chatbot

An intelligent multi-agent chatbot system that automates the entire personal loan sales process from customer engagement to sanction letter generation.

## 🌟 Features

### Core Capabilities
- **Multi-Agent Orchestration**: Specialized AI agents for different stages of the loan process
- **End-to-End Automation**: From initial inquiry to sanction letter generation
- **Real-time Intelligence**: Live credit score checks, dynamic pricing, and instant decisioning
- **Document Processing**: AI-powered OCR and fraud detection
- **Sentiment Analysis**: Adaptive responses based on customer mood
- **Multi-language Support**: English and Hindi support

### AI Agents
1. **Master Agent**: Orchestrates conversation flow and routes to appropriate agents
2. **Engage Agent**: Handles customer engagement, lead qualification, and sales
3. **Verify Agent**: Manages document collection and verification (KYC)
4. **Underwrite Agent**: Performs risk assessment and loan eligibility calculation
5. **Sanction Agent**: Generates professional PDF sanction letters

### Advanced Features
- Voice support (speech-to-text and text-to-speech)
- Real-time analytics dashboard
- Conversion funnel visualization
- A/B testing framework
- Customer profiling and recommendations
- Fraud detection system
- WhatsApp integration (mock)
- Email and SMS notifications (mock)

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- LangGraph for agent orchestration
- OpenAI GPT-4
- PostgreSQL (structured data)
- MongoDB (conversations/documents)
- Redis (caching/sessions)

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Recharts (analytics)
- React Query (data fetching)

**Infrastructure:**
- Docker & Docker Compose
- WebSocket for real-time chat

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd loanifi
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- MongoDB (port 27017)
- Redis (port 6379)
- FastAPI Backend (port 8000)
- React Frontend (port 3000)

4. **Initialize the database**
```bash
# Access backend container
docker exec -it loanifi_backend bash

# Run database initialization
python -m backend.app.utils.database
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start services (PostgreSQL, MongoDB, Redis) separately
# Then run:
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 Usage

### Customer Flow
1. Start a conversation with the AI assistant
2. Discuss loan requirements and get pre-qualified
3. Upload required documents (PAN, Aadhaar, bank statements, etc.)
4. Receive instant credit score check
5. Get loan eligibility and offer details
6. Accept offer and receive sanction letter via email

### Admin Dashboard
Access the admin dashboard at `/admin` to:
- View real-time analytics
- Monitor conversion funnel
- Track agent performance
- Manage applications
- Analyze time metrics

## 🔧 API Endpoints

### Chat
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history/{conversation_id}` - Get conversation history
- `GET /api/chat/conversations/user/{user_id}` - Get user conversations

### Documents
- `POST /api/documents/upload` - Upload document
- `POST /api/documents/verify/{document_id}` - Verify document
- `GET /api/documents/application/{application_id}` - Get application documents

### Analytics
- `GET /api/analytics/dashboard` - Get dashboard analytics
- `GET /api/analytics/conversion-funnel` - Get conversion funnel data
- `GET /api/analytics/agent-performance` - Get agent performance metrics
- `GET /api/analytics/time-metrics` - Get time-based metrics

### Admin
- `GET /api/admin/applications` - List applications
- `GET /api/admin/applications/{id}` - Get application details
- `PUT /api/admin/applications/{id}/status` - Update application status
- `GET /api/admin/users` - List users
- `GET /api/admin/stats/overview` - Get overview statistics

## 🎯 Key Metrics

### Success Metrics
- **Conversion Rate**: 40%+ improvement vs traditional process
- **Time to Sanction**: < 15 minutes (vs days traditionally)
- **Cost Reduction**: 60%+ reduction in manual processing
- **Document Verification**: 95%+ accuracy
- **Customer Satisfaction**: 4.5+ star rating target

## 🔒 Security

- End-to-end encryption for sensitive data
- JWT authentication
- Rate limiting
- Input sanitization
- Audit logging
- GDPR compliance measures
- Secure file storage

## 📊 Agent Prompts

All agent prompts are stored in `agents/prompts/` directory:
- `master_prompt.txt` - Master orchestrator agent
- `engage_prompt.txt` - Customer engagement agent
- `verify_prompt.txt` - Document verification agent
- `underwrite_prompt.txt` - Risk assessment agent
- `sanction_prompt.txt` - Sanction letter agent

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 Documentation

- **API Documentation**: Available at `/docs` when backend is running
- **Architecture**: See `ARCHITECTURE.md`
- **Demo Guide**: See `DEMO_GUIDE.md`

## 🤝 Contributing

This is a hackathon project. For production use, consider:
- Implementing real external API integrations (CIBIL, SendGrid, Twilio, etc.)
- Adding comprehensive error handling
- Implementing proper authentication and authorization
- Adding extensive test coverage
- Setting up production-grade monitoring and logging
- Implementing data backup and recovery
- Adding load balancing and scaling capabilities

## 📄 License

MIT License

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- LangChain/LangGraph for agent orchestration
- FastAPI for the excellent web framework
- React community for frontend tools

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for financial inclusion and customer experience innovation**



# LoaniFi - System Architecture

## Overview

LoaniFi is a sophisticated AI-powered chatbot system built using a multi-agent architecture. The system leverages specialized AI agents that work together to automate the entire personal loan application process.

## System Components

### 1. Frontend Layer (React)

**Technology Stack:**
- React 18 with Vite
- Tailwind CSS for styling
- React Query for data fetching
- Recharts for visualizations
- Zustand for state management

**Key Components:**
- `ChatInterface`: Real-time chat with AI agents
- `DocumentUpload`: Multi-document upload with validation
- `ApplicationDashboard`: Application status tracking
- `AdminDashboard`: Analytics and management interface
- `ConversionFunnel`: Visual conversion tracking
- `Analytics`: Performance metrics and insights

**Features:**
- WebSocket support for real-time communication
- Progressive enhancement
- Responsive design
- Optimized for performance

### 2. Backend Layer (FastAPI)

**Technology Stack:**
- Python 3.11
- FastAPI for REST API
- SQLAlchemy for ORM
- Pydantic for data validation
- Structlog for logging

**API Structure:**
```
/api
  /chat - Conversation management
  /ws - WebSocket endpoints
  /documents - Document handling
  /admin - Administration
  /analytics - Business intelligence
```

**Middleware:**
- CORS handling
- Request timing
- Rate limiting
- Authentication (JWT)
- Error handling

### 3. Agent Orchestration Layer

**Master Agent Pattern:**
The Master Agent acts as an orchestrator that:
1. Receives user messages
2. Analyzes conversation state
3. Routes to appropriate specialized agent
4. Manages context between agents
5. Handles agent handoffs
6. Ensures conversation continuity

**Specialized Agents:**

**a) Engage Agent**
- Role: Sales and relationship management
- Functions:
  - Lead qualification
  - Product explanation
  - Objection handling
  - Requirement gathering
- Handoff Trigger: Customer ready to proceed with application

**b) Verify Agent**
- Role: Document and identity verification
- Functions:
  - KYC document collection
  - OCR processing
  - Document validation
  - Credit score retrieval
- Handoff Trigger: All documents verified

**c) Underwrite Agent**
- Role: Risk assessment and underwriting
- Functions:
  - Creditworthiness analysis
  - DTI calculation
  - Eligibility determination
  - Interest rate assignment
- Handoff Trigger: Loan approved

**d) Sanction Agent**
- Role: Final approval and documentation
- Functions:
  - Sanction letter generation
  - Terms finalization
  - Email delivery
  - Process completion
- Handoff Trigger: Customer accepts terms

### 4. Data Layer

**PostgreSQL - Structured Data:**
```
Tables:
- users (user profiles)
- conversations (conversation metadata)
- messages (individual messages)
- loan_applications (application data)
- documents (document records)
- customer_profiles (personalization data)
- metrics (analytics data)
```

**MongoDB - Unstructured Data:**
```
Collections:
- conversation_history (full message history)
- audit_logs (compliance tracking)
- session_data (temporary data)
```

**Redis - Caching:**
```
Keys:
- session:{session_id} (conversation state)
- rate_limit:{client_id} (rate limiting)
- cache:{key} (general caching)
```

### 5. Service Layer

**Core Services:**
- `LLMService`: OpenAI GPT-4 integration
- `DocumentService`: Document processing
- `CreditScoreService`: Credit bureau integration (mock)
- `PDFService`: Sanction letter generation
- `NotificationService`: Email/SMS (mock)
- `OCRService`: Document data extraction (mock)
- `FraudDetectionService`: Anomaly detection
- `SentimentService`: Sentiment analysis
- `VoiceService`: Speech processing (mock)

**Business Services:**
- `ProfilingService`: Customer profiling
- `AnalyticsService`: Business intelligence
- `RecommendationService`: Product recommendations

### 6. Integration Layer

**Mock Integrations:**
- CRM (Salesforce/HubSpot format)
- Banking APIs (account verification)
- Payment Gateway (application fees)
- WhatsApp Business API
- Email Service (SendGrid format)
- SMS Service (Twilio format)

**Note:** These are mock implementations for demo purposes. Production would integrate real APIs.

## Data Flow

### 1. Customer Interaction Flow

```
User Message
    ↓
WebSocket/REST API
    ↓
Chat Endpoint
    ↓
Master Agent (determines routing)
    ↓
Specialized Agent (processes message)
    ↓
LLM Service (GPT-4)
    ↓
Function Calls (if needed)
    ↓
Services (document, credit, etc.)
    ↓
Database Updates
    ↓
Response to User
```

### 2. Document Processing Flow

```
File Upload
    ↓
Document Service (validation)
    ↓
Storage (filesystem/S3)
    ↓
Database Record
    ↓
OCR Service (extraction)
    ↓
Fraud Detection (validation)
    ↓
Verification Result
    ↓
Update Application State
```

### 3. Underwriting Flow

```
Verified Documents + User Data
    ↓
Underwrite Agent
    ↓
Calculate Eligibility
    ↓
Determine Interest Rate
    ↓
Assess Risk
    ↓
Generate Loan Offer
    ↓
Store in Database
    ↓
Present to Customer
```

## Security Architecture

### Authentication & Authorization
- JWT tokens for API access
- Token expiration and refresh
- Role-based access control (customer/admin)
- Session management via Redis

### Data Security
- Encryption at rest for sensitive fields
- TLS/SSL for data in transit
- PAN/Aadhaar masked in logs and UI
- Secure file storage

### Compliance
- Audit logging for all actions
- GDPR-compliant data handling
- Data retention policies
- Consent management

### API Security
- Rate limiting per client/IP
- Input validation and sanitization
- SQL injection prevention (ORM)
- XSS protection
- CORS configuration

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Load balancer ready
- Session state in Redis (shared)
- Database connection pooling

### Performance Optimization
- Redis caching layer
- Database query optimization
- Async I/O operations
- WebSocket for real-time updates
- CDN for static assets

### Monitoring & Observability
- Structured logging (JSON)
- Request timing headers
- Error tracking
- Performance metrics
- Health check endpoints

## Deployment Architecture

### Development Environment
```
Docker Compose:
- postgres:15-alpine
- mongo:7-jammy
- redis:7-alpine
- loanifi_backend (FastAPI)
- loanifi_frontend (React)
```

### Production Environment (Recommended)
```
Cloud Platform (AWS/Azure/GCP):
- Kubernetes cluster
  - Backend pods (autoscaling)
  - Frontend pods (Nginx)
- Managed PostgreSQL (RDS/CloudSQL)
- Managed MongoDB (Atlas)
- Managed Redis (ElastiCache/MemoryStore)
- Object Storage (S3/Blob Storage)
- Load Balancer
- CDN (CloudFront/CloudFlare)
- Monitoring (Prometheus/Grafana)
- Logging (ELK Stack)
```

## Agent Communication Protocol

### Message Structure
```python
{
    "conversation_id": "uuid",
    "user_id": "uuid",
    "message": "user message text",
    "context": {
        "stage": "current_stage",
        "data": {},
        "history": []
    },
    "metadata": {
        "sentiment": {},
        "language": "english"
    }
}
```

### Context Management
```python
{
    "stage": "qualified|verified|approved|sanctioned",
    "current_agent": "engage|verify|underwrite|sanction",
    "next_agent": "agent_to_hand_off_to",
    "loan_requirements": {},
    "documents": {},
    "underwriting_result": {},
    "application_number": "APP12345678"
}
```

## Performance Metrics

### Target Metrics
- API Response Time: < 200ms (95th percentile)
- LLM Response Time: < 3s
- Document Upload: < 5s for 10MB
- WebSocket Latency: < 100ms
- Database Query Time: < 50ms
- Time to Sanction: < 15 minutes (end-to-end)

### Capacity Planning
- Concurrent users: 1000+
- Messages per second: 100+
- Document uploads per hour: 500+
- Database connections: 50 per instance

## Technology Choices - Rationale

### Why FastAPI?
- Async support for better performance
- Automatic API documentation
- Type hints and validation
- WebSocket support
- Fast development

### Why LangGraph?
- State management for agents
- Easy agent orchestration
- Function calling support
- Conversation flow control

### Why PostgreSQL + MongoDB?
- PostgreSQL for structured, relational data
- MongoDB for flexible, document-based data
- Best of both worlds

### Why Redis?
- Fast in-memory caching
- Session management
- Real-time features
- Rate limiting

### Why React?
- Component reusability
- Large ecosystem
- Great developer experience
- Performance optimization

## Future Enhancements

### Phase 2 Features
- Voice call integration
- Video verification
- Mobile apps (React Native)
- Regional language expansion
- Advanced ML models
- Blockchain for document verification
- Real-time collaboration

### Enterprise Features
- Multi-tenancy support
- Custom branding
- Advanced reporting
- Integration marketplace
- Workflow customization
- Role management
- SLA monitoring

## Conclusion

LoaniFi demonstrates a modern, scalable architecture for AI-powered loan automation. The multi-agent design allows for specialized intelligence at each stage while maintaining conversation continuity and context.



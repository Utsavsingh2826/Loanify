"""Seed data for demo and testing."""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from app.models.user import User, UserRole
from app.models.conversation import Conversation, Message, ConversationStatus, MessageRole, AgentType
from app.models.loan_application import LoanApplication, ApplicationStatus, LoanPurpose, Document
from app.models.customer_profile import CustomerProfile
from app.utils.database import SessionLocal, init_db
from app.utils.security import get_password_hash
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_demo_users(db: Session) -> list:
    """Create demo users."""
    users = [
        User(
            id=uuid.uuid4(),
            email="rajesh.kumar@example.com",
            phone="+919876543210",
            full_name="Rajesh Kumar Sharma",
            hashed_password=get_password_hash("demo123"),
            role=UserRole.CUSTOMER,
            is_active=True,
            is_verified=True,
            date_of_birth=datetime(1985, 8, 15),
            pan_number="ABCDE1234F",
            employment_type="salaried",
            monthly_income="80000",
            city="Bangalore",
            state="Karnataka",
            preferred_language="english"
        ),
        User(
            id=uuid.uuid4(),
            email="priya.singh@example.com",
            phone="+919876543211",
            full_name="Priya Singh",
            hashed_password=get_password_hash("demo123"),
            role=UserRole.CUSTOMER,
            is_active=True,
            is_verified=True,
            date_of_birth=datetime(1990, 3, 20),
            employment_type="self_employed",
            monthly_income="120000",
            city="Mumbai",
            state="Maharashtra",
            preferred_language="hindi"
        ),
        User(
            id=uuid.uuid4(),
            email="admin@loanifi.com",
            phone="+919876543212",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    logger.info("demo_users_created", count=len(users))
    return users


def create_demo_conversations(db: Session, users: list):
    """Create demo conversations with messages."""
    customer = users[0]
    
    # Completed conversation
    conv1 = Conversation(
        id=uuid.uuid4(),
        user_id=customer.id,
        status=ConversationStatus.COMPLETED,
        current_agent=AgentType.SANCTION,
        started_at=datetime.utcnow() - timedelta(hours=2),
        ended_at=datetime.utcnow() - timedelta(hours=1, minutes=45),
        message_count=15,
        conversation_state={
            "stage": "sanctioned",
            "loan_requirements": {
                "loan_purpose": "home_renovation",
                "loan_amount": 500000,
                "tenure_months": 36
            }
        }
    )
    db.add(conv1)
    
    # Add sample messages
    messages = [
        Message(
            id=uuid.uuid4(),
            conversation_id=conv1.id,
            role=MessageRole.USER,
            content="Hi, I need a personal loan for home renovation",
            agent_type=AgentType.MASTER,
            created_at=datetime.utcnow() - timedelta(hours=2)
        ),
        Message(
            id=uuid.uuid4(),
            conversation_id=conv1.id,
            role=MessageRole.ASSISTANT,
            content="Hello! I'd be happy to help you with a personal loan. How much are you looking to borrow?",
            agent_type=AgentType.ENGAGE,
            created_at=datetime.utcnow() - timedelta(hours=2, minutes=-1)
        ),
        Message(
            id=uuid.uuid4(),
            conversation_id=conv1.id,
            role=MessageRole.USER,
            content="I need 5 lakh rupees",
            agent_type=AgentType.ENGAGE,
            created_at=datetime.utcnow() - timedelta(hours=2, minutes=-2)
        ),
    ]
    
    for msg in messages:
        db.add(msg)
    
    # Active conversation
    conv2 = Conversation(
        id=uuid.uuid4(),
        user_id=customer.id,
        status=ConversationStatus.ACTIVE,
        current_agent=AgentType.VERIFY,
        started_at=datetime.utcnow() - timedelta(minutes=30),
        message_count=8,
        conversation_state={"stage": "qualified"}
    )
    db.add(conv2)
    
    db.commit()
    logger.info("demo_conversations_created")
    return [conv1, conv2]


def create_demo_applications(db: Session, users: list, conversations: list):
    """Create demo loan applications."""
    customer = users[0]
    
    # Sanctioned application
    app1 = LoanApplication(
        id=uuid.uuid4(),
        application_number="APP" + str(uuid.uuid4())[:8].upper(),
        user_id=customer.id,
        conversation_id=conversations[0].id,
        status=ApplicationStatus.SANCTIONED,
        loan_purpose=LoanPurpose.HOME_RENOVATION,
        requested_amount=500000,
        approved_amount=500000,
        tenure_months=36,
        interest_rate=12.5,
        monthly_income=80000,
        credit_score=750,
        risk_score=0.25,
        risk_category="low",
        eligibility_amount=600000,
        created_at=datetime.utcnow() - timedelta(hours=2),
        submitted_at=datetime.utcnow() - timedelta(hours=1, minutes=50),
        approved_at=datetime.utcnow() - timedelta(hours=1, minutes=48),
        sanctioned_at=datetime.utcnow() - timedelta(hours=1, minutes=45)
    )
    db.add(app1)
    
    # Under review application
    app2 = LoanApplication(
        id=uuid.uuid4(),
        application_number="APP" + str(uuid.uuid4())[:8].upper(),
        user_id=users[1].id,
        conversation_id=conversations[1].id if len(conversations) > 1 else conversations[0].id,
        status=ApplicationStatus.UNDER_REVIEW,
        loan_purpose=LoanPurpose.BUSINESS,
        requested_amount=1000000,
        tenure_months=48,
        monthly_income=120000,
        credit_score=720,
        created_at=datetime.utcnow() - timedelta(hours=5),
        submitted_at=datetime.utcnow() - timedelta(hours=4)
    )
    db.add(app2)
    
    db.commit()
    logger.info("demo_applications_created")
    return [app1, app2]


def create_demo_profiles(db: Session, users: list):
    """Create customer profiles."""
    for user in users:
        if user.role == UserRole.CUSTOMER:
            profile = CustomerProfile(
                id=uuid.uuid4(),
                user_id=user.id,
                total_conversations=2,
                total_applications=1,
                successful_applications=1 if user.email == "rajesh.kumar@example.com" else 0,
                preferred_language=user.preferred_language,
                average_sentiment_score=0.75,
                engagement_score=0.85,
                approval_likelihood=0.80,
                created_at=datetime.utcnow() - timedelta(days=30)
            )
            db.add(profile)
    
    db.commit()
    logger.info("demo_profiles_created")


def seed_database():
    """Seed database with demo data."""
    try:
        # Initialize database
        init_db()
        
        # Create session
        db = SessionLocal()
        
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info("database_already_seeded", user_count=existing_users)
            db.close()
            return
        
        logger.info("seeding_database")
        
        # Create demo data
        users = create_demo_users(db)
        conversations = create_demo_conversations(db, users)
        applications = create_demo_applications(db, users, conversations)
        create_demo_profiles(db, users)
        
        db.close()
        
        logger.info("database_seeded_successfully")
        print("\n✅ Database seeded successfully!")
        print("\nDemo Users:")
        print("- Customer: rajesh.kumar@example.com / demo123")
        print("- Customer: priya.singh@example.com / demo123")
        print("- Admin: admin@loanifi.com / admin123")
        
    except Exception as e:
        logger.error("seed_error", error=str(e))
        print(f"\n❌ Error seeding database: {e}")
        raise


if __name__ == "__main__":
    seed_database()



#!/usr/bin/env python3
"""
Setup fresh database with all tables and test data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import engine, SessionLocal
from src.models.user import User, Role
from src.models.base import Base
from datetime import datetime

def main():
    print("🔄 Setting up fresh database...")
    
    # Drop and recreate all tables
    Base.metadata.drop_all(engine)
    print("⚠️  All tables dropped")
    
    Base.metadata.create_all(engine)
    print("✅ All tables recreated with fresh schema")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create roles first
        admin_role = Role(id=1, name="admin", description="Administrator with full access", is_paid=False)
        coach_role = Role(id=2, name="coach", description="Coach who can create and manage plans", is_paid=False)
        client_role = Role(id=3, name="client", description="Client who can follow assigned plans", is_paid=False)
        
        db.add_all([admin_role, coach_role, client_role])
        db.commit()
        print("✅ Roles created")
        
        # Create admin user
        admin_uuid = "916e4281-60e5-4585-b7b7-6ae92e542e15"
        admin = User(
            id=admin_uuid,
            name="Admin User",
            email="admin@fitness.com",
            password_hash="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
            role_id=1,
            is_approved=True
        )
        db.add(admin)
        
        # Create coach user (unapproved)
        coach_uuid = "550e8400-2936-4b0c-b8c8-3b2c3c6a5b2b"
        coach = User(
            id=coach_uuid,
            name="Coach User",
            email="coach@fitness.com",
            password_hash="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
            role_id=2,
            is_approved=False,
            approval_requested_at=datetime.utcnow()
        )
        db.add(coach)
        
        # Create normal user
        client_uuid = "d362bed0-6dbc-420e-8966-d27f64827cb9"
        client = User(
            id=client_uuid,
            name="Normal User",
            email="user@fitness.com",
            password_hash="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
            role_id=3,
            is_approved=True
        )
        db.add(client)
        
        db.commit()
        print("✅ Test users created")
        
        # Test queries
        admin_user = db.query(User).filter(User.email == "admin@fitness.com").first()
        coach_user = db.query(User).filter(User.email == "coach@fitness.com").first()
        client_user = db.query(User).filter(User.email == "user@fitness.com").first()
        
        print(f"✅ Admin: {admin_user.name}, role_id: {admin_user.role_id}, approved: {admin_user.is_approved}")
        print(f"✅ Coach: {coach_user.name}, role_id: {coach_user.role_id}, approved: {coach_user.is_approved}")
        print(f"✅ Client: {client_user.name}, role_id: {client_user.role_id}, approved: {client_user.is_approved}")
        
        # Test approval fields
        print(f"   - Coach approval_requested_at: {coach_user.approval_requested_at}")
        print(f"   - Coach approved_by: {coach_user.approved_by}")
        print(f"   - Coach approved_at: {coach_user.approved_at}")
        
        print("\n🎉 Database setup complete!")
        print("📊 Test credentials:")
        print("   Admin: admin@fitness.com / password123")
        print("   Coach: coach@fitness.com / password123 (pending approval)")
        print("   Client: user@fitness.com / password123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()

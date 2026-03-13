#!/usr/bin/env python3
"""
Check and fix password hashes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.security import get_password_hash, verify_password
from src.models.user import User

def check_and_fix_admin():
    db = SessionLocal()
    try:
        # Check admin user
        admin = db.query(User).filter(User.email == "admin@fitness.com").first()
        
        if admin:
            print(f"Admin user found: {admin.email}")
            print(f"Current hash: {admin.password_hash[:50]}...")
            
            # Try to verify with current password
            try:
                if verify_password("admin123", admin.password_hash):
                    print("✅ Admin password verification successful")
                else:
                    print("❌ Admin password verification failed")
                    
                    # Reset the password
                    new_hash = get_password_hash("admin123")
                    admin.password_hash = new_hash
                    db.commit()
                    print("✅ Admin password reset successfully")
                    
            except Exception as e:
                print(f"❌ Error verifying password: {e}")
                
                # Reset the password
                new_hash = get_password_hash("admin123")
                admin.password_hash = new_hash
                db.commit()
                print("✅ Admin password reset successfully")
        else:
            print("❌ Admin user not found")
            
            # Create admin user
            admin_user = User(
                email="admin@fitness.com",
                name="Administrador",
                password_hash=get_password_hash("admin123"),
                role_id=1,  # Admin role
                is_approved=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created successfully")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_fix_admin()

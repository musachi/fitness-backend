-- Add approval fields to users table
ALTER TABLE users
ADD COLUMN is_approved BOOLEAN DEFAULT TRUE,  -- Default TRUE for existing users
ADD COLUMN approval_requested_at TIMESTAMP,
ADD COLUMN approved_by UUID REFERENCES users(id),
ADD COLUMN approved_at TIMESTAMP;

-- For coach role (role_id=2), set is_approved to FALSE by default
-- This will require manual approval from admin
UPDATE users
SET is_approved = FALSE
WHERE role_id = 2 AND is_approved = TRUE;

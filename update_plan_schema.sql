-- Add description, goal, and level columns to plans table
ALTER TABLE plans
ADD COLUMN description VARCHAR(1000),
ADD COLUMN goal VARCHAR(50) NOT NULL DEFAULT 'general_fitness',
ADD COLUMN level VARCHAR(20) NOT NULL DEFAULT 'beginner';

-- Update existing plans with default values
UPDATE plans
SET goal = 'general_fitness', level = 'beginner'
WHERE goal IS NULL OR level IS NULL;

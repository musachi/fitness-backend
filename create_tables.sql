-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    coach_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create exercises table
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    muscle_groups JSON,
    equipment JSON,
    movement_type VARCHAR(50),
    position VARCHAR(50),
    contraction_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    coach_id UUID REFERENCES users(id)
);

-- Create plans table with description, goal, and level
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    goal VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL,
    coach_id UUID REFERENCES users(id),
    duration_weeks INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workout_sessions table
CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans(id),
    client_id UUID REFERENCES users(id),
    date DATE,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workout_exercises table
CREATE TABLE workout_exercises (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES workout_sessions(id),
    exercise_id INTEGER REFERENCES exercises(id),
    sets_planned INTEGER,
    reps_planned VARCHAR(50),
    weight_planned VARCHAR(50),
    rest_between_sets VARCHAR(50),
    sets_done INTEGER,
    reps_done JSON,
    weight_used VARCHAR(50),
    time_spent VARCHAR(50),
    reps_in_time JSON
);

-- Insert default roles
INSERT INTO roles (name, description, is_paid) VALUES
    ('admin', 'Administrator with full access', FALSE),
    ('coach', 'Coach who can create and manage plans', FALSE),
    ('client', 'Client who can follow assigned plans', FALSE);

-- Создание таблицы Permissions
CREATE TABLE IF NOT EXISTS Permissions (
    prem_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы Roles
CREATE TABLE IF NOT EXISTS Roles (
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы RolePermissions
CREATE TABLE IF NOT EXISTS RolePermissions (
    role_id INT REFERENCES Roles(role_id),
    permission_id INT REFERENCES Permissions(prem_id),
    PRIMARY KEY (role_id, permission_id)
);

-- Создание таблицы Users
CREATE TABLE IF NOT EXISTS Users (
    id_users SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT REFERENCES Roles(role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы TestCases
CREATE TABLE IF NOT EXISTS TestCases (
    id_case SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы TestCaseSteps
CREATE TABLE IF NOT EXISTS TestCaseSteps (
    id_step SERIAL PRIMARY KEY,
    StepNumber INT,
    ActionDescription TEXT,
    ExpectedResult TEXT,
    TestCaseID INT REFERENCES TestCases(id_case)
);

-- Создание таблицы TestRuns
CREATE TABLE IF NOT EXISTS TestRuns (
    id_run SERIAL PRIMARY KEY,
    testcase_id INT REFERENCES TestCases(id_case),
    user_id INT REFERENCES Users(id_users),
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы TestSuites
CREATE TABLE IF NOT EXISTS TestSuites (
    suite_id SERIAL PRIMARY KEY,
    suite_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы TestSuiteCases
CREATE TABLE IF NOT EXISTS TestSuiteCases (
    suite_id INT REFERENCES TestSuites(suite_id),
    case_id INT REFERENCES TestCases(id_case),
    PRIMARY KEY (suite_id, case_id)
);

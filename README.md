# Ghost CMS QA Automation

End-to-end QA automation project for **Ghost CMS**, covering functional testing, cross-browser testing, accessibility testing, visual regression, and exploratory defect reporting.

The application under test is a locally deployed Ghost CMS instance running in Docker.

---

## Project Overview

This project demonstrates a practical QA automation workflow against a real application rather than a demo website.

The test suite focuses on critical user journeys including:

- Ghost login
- Post creation
- Draft persistence
- Post publishing
- Published post persistence
- Post deletion
- Accessibility checks
- Visual regression
- Cross-browser execution

Manual exploratory testing is also used to identify defects that automated happy-path tests may not detect.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Test automation language |
| Pytest | Test framework |
| Playwright | Browser automation |
| pytest-bdd | BDD scenarios |
| axe-playwright-python | Accessibility testing |
| Allure | Test reporting |
| Docker | Application under test |
| Git / GitHub | Version control and portfolio |

---

## Test Architecture

```text
ghost-qa-automation/
│
├── .github/
│   └── workflows/
│
├── pages/
│   ├── __init__.py
│   ├── login_page.py
│   └── posts_page.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_smoke.py
│   ├── test_login.py
│   ├── test_posts.py
│   ├── test_accessibility.py
│   └── test_visual.py
│
├── features/
│   └── publishing.feature
│
├── bug_reports/
│   └── BUG-001.md
│
├── screenshots/
│   └── test evidence
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md

Page Object Model

Application-specific locators and actions are kept inside Page Object classes.

Test
 ↓
Page Object
 ↓
Ghost UI

This keeps the tests readable and makes locator maintenance easier when the application UI changes.

Test Coverage
Authentication
Valid login
Login page smoke validation
Posts
Create post
Add title and content
Publish post
Verify post in the Posts list
Draft persistence
Published post persistence
Deleted post persistence
Cross-Browser

Tests are executed against:

Chromium
Firefox
WebKit

Example:

pytest tests/test_posts.py --browser=chromium
pytest tests/test_posts.py --browser=firefox
pytest tests/test_posts.py --browser=webkit
Accessibility Testing

Accessibility checks use the axe-core engine through axe-playwright-python.

The login page is scanned for accessibility violations.

The current Ghost instance produced findings including:

color-contrast
landmark-unique
meta-viewport
region

These findings are captured as QA observations rather than modifying the application under test.

Visual Regression Testing

A baseline screenshot is captured for the Ghost homepage.

The current page is then captured and compared against the baseline.

Baseline screenshot
        ↓
Current screenshot
        ↓
Image comparison
        ↓
Pass / Fail

This helps identify unintended visual changes.

Exploratory Testing

Manual exploratory testing was performed before expanding automation.

Areas explored included:

Login
Post creation
Drafts
Publishing
Editing
Deletion
Preview
Image/media behavior
Long content
Special characters
Persistence

Exploratory testing was used to identify scenarios that should be automated or documented as defects.

Defects Identified
BUG-001 — Post Preview Fails to Load

Severity: Medium

The Ghost post preview displayed a connection error when running the application locally through Docker.

Evidence and reproduction steps are documented in:

bug_reports/BUG-001.md

Running the Project
1. Start Ghost

The application under test runs locally through Docker.

Verify the container is running:

docker ps

Ghost should be available at:

http://localhost:3001
2. Activate the Python environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Install Playwright browsers
python -m playwright install chromium firefox webkit
5. Run all tests
pytest
6. Run a specific test
pytest tests/test_login.py
7. Run headed
pytest tests/test_posts.py --headed
8. Run a specific browser
pytest tests/test_posts.py --browser=chromium
Test Reporting

Allure reporting is configured through allure-pytest.

Generate test results:

pytest --alluredir=allure-results

The generated report can be opened with Allure tooling.

QA Approach

The testing strategy follows this progression:

Explore
   ↓
Identify risks
   ↓
Design test scenarios
   ↓
Automate critical flows
   ↓
Cross-browser validation
   ↓
Accessibility validation
   ↓
Visual validation
   ↓
Defect reporting

The goal is not maximum test count.

The goal is meaningful coverage of critical user journeys and clear defect documentation.

Skills Demonstrated
UI automation
Playwright
Pytest
Page Object Model
BDD
Cross-browser testing
Accessibility testing
Visual regression testing
Exploratory testing
Defect reporting
Docker-based test environments
Git/GitHub
Test reporting






# SQLiScanner

## Description

SQLiScanner is a Python-based automated vulnerability assessment tool designed to detect potential error-based SQL Injection (SQLi) vulnerabilities in web application forms. It is developed for educational security testing in authorised lab environments, such as DVWA.

The tool parses HTML forms, identifies testable input parameters, establishes baseline responses, injects SQL testing payloads, and detects database error signatures.

## Intended Users

SQLiScanner is intended for:
- Cybersecurity students and ethical hacking learners who want to understand basic SQL injection detection.
- Educators demonstrating web application security testing in controlled laboratory environments.
- Junior penetration testers conducting authorised security assessments.
- Web developers interested in identifying potential SQL injection vulnerabilities in their applications.

## Team Members

This project was collaboratively developed by four students from UniKL MIIT as part of the IKB31603 Ethical Hacking Assignment 1.

GROUP 1 L01-B05
| No. | Name | Student ID | Contribution |
|---|---|---|---|
| 1 | Muhammad Hafeez bin Mohd Radzi | 52215226085 | Scanner testing, validation, documentation and report preparation. |
| 2 | Nur Najihah Farhanah binti Hashim | 52215125111 | Core scanner development, SQL injection detection logic, payload implementation, integration and overall testing. |
| 3 | Izzat 'Irfan bin Azman | 52215124710 | HTML form discovery, input parameter identification, testing and documentation. |
| 4 | Shahril Iskandar bin Sharizan | 52215125627 | Response analysis, vulnerability verification, testing and report preparation. |

All team members contributed to the development, testing, documentation and evaluation of SQLiScanner.

## Attack Category

- **Vulnerability Class:** SQL Injection (CWE-89: Improper Neutralization of Special Elements used in an SQL Command)
- **OWASP Top 10 Mapping:** A03:2021 – Injection

## Attack Lifecycle Mapping

1. **Reconnaissance & Enumeration:** Connects to the target URL, parses HTML forms using BeautifulSoup, and identifies testable input parameters, such as text and search fields.

2. **Baseline Establishment:** Submits normal form data to establish the application's baseline response behaviour and help reduce false positives.

3. **Vulnerability Probing:** Injects syntax-breaking characters (`'`, `"`, `')`, `")`) into discovered parameters to identify potential SQL injection vulnerabilities.

4. **Analysis & Detection:** Analyses HTTP responses for database error signatures associated with MySQL, MSSQL, and Oracle.

5. **Reporting & Safe Termination:** Displays potential findings in the console and saves timestamped reports locally in the `output/` directory. The scan can also be interrupted using the keyboard interrupt (`Ctrl+C`).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/njhhfrhnh/SQLiScanner.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SQLiScanner
   ```

3. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   **Windows PowerShell:**

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**

   ```bash
   source .venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

### 1. Standard Interactive Scan

Run the scanner and follow the interactive prompts:

```bash
python main.py
```

### 2. Dry Run

Validates the target URL and scope without sending HTTP requests:

```bash
python main.py --dry-run
```

## Demonstration

### 1. Legal Disclaimer and Authorization

SQLiScanner displays a legal disclaimer referencing the Computer Crimes Act 1997 (Act 563), Malaysia, and requires users to confirm their authorization before proceeding.

![Legal Disclaimer](01-legal-disclaimer.png)

### 2. SQL Injection Detection

The following screenshot demonstrates SQLiScanner detecting a potential error-based SQL injection vulnerability in the DVWA testing environment.

![DVWA SQLi Detection](02-dvwa-sqli-detection.png)

### 3. Authenticated Scan

Passes session cookies to access pages that require authentication, such as DVWA:

```bash
python main.py --cookie "PHPSESSID=your_session_id; security=low"
```

**Note:** Replace the placeholder with your own valid session cookie. Never share or commit session cookies because they contain authentication credentials.

## Rules of Engagement (RoE)

### Authorised Scope

- Testing is permitted only on localhost, isolated lab environments, or systems with explicit written authorisation.
- The target hostname must be confirmed before testing begins.
- Testing outside the authorised scope is strictly prohibited.

### Testing Time Windows

- Testing must be conducted within the time window approved by the system owner.
- Testing must stop immediately if the authorised testing period expires.

### Permitted Techniques

- HTML form discovery and input parameter identification.
- Basic SQL injection payload testing.
- Detection of database error messages.
- Local report generation for vulnerability assessment.

### Prohibited Actions

- Testing systems without permission.
- Accessing, extracting, or modifying sensitive information.
- Denial-of-service attacks or destructive testing.
- Testing targets outside the approved scope.

### Emergency Stop Procedures

- Press `Ctrl+C` to activate the keyboard interrupt kill switch.
- The scanner will stop execution safely.
- Partial scan results will be saved locally when available.

## Ethical Considerations & Responsible Disclosure

SQLiScanner is developed strictly for academic learning and defensive vulnerability assessment. Several safeguards are implemented to encourage responsible usage:

- **User Authorization:** Requires users to explicitly confirm that they have permission to test the target system before proceeding.
- **Target Scope Validation:** Helps prevent testing outside the intended and authorised scope.
- **Safe Default Target:** Uses localhost as the default target to reduce accidental testing of external systems.
- **Limited Payloads:** Uses basic SQL syntax-breaking characters to identify potential database error responses without attempting data extraction or destructive exploitation.
- **Emergency Stop:** Provides a Ctrl+C mechanism to interrupt scanning and preserve partial results when available.
- **Local Report Storage:** Saves scan results locally in the designated output directory.

If a potential vulnerability is discovered during authorised testing, it should be reported privately to the affected system owner or their designated security contact. The report should include the affected URL, input parameter, detected error evidence and recommended remediation, such as implementing parameterised queries or prepared statements.

Users should avoid accessing, extracting or publicly disclosing sensitive information. Public disclosure should be avoided until the system owner has had a reasonable opportunity to address the vulnerability.

## Legal Disclaimer

**LEGAL NOTICE:** This tool is intended for educational purposes and authorised security testing only. Unauthorised testing of systems without explicit permission is strictly prohibited and may constitute an offence under the Computer Crimes Act 1997 (Act 563) Malaysia. The developers assume no responsibility or liability for any misuse or damage caused by this software.

By using this tool, users acknowledge that they are responsible for obtaining proper authorisation before conducting security testing.

## Limitations

- **Error-Based Detection Only:** SQLiScanner focuses on detecting visible database error signatures. It does not currently support Boolean-based, Time-based or UNION-based SQL injection detection.
- **Limited Input Coverage:** The scanner focuses on supported HTML form input parameters and does not comprehensively test JSON payloads, HTTP headers or standalone URL query parameters.
- **Authentication Dependency:** Authenticated pages require a valid session cookie. An expired or missing cookie may cause the scanner to access a login page instead of the intended application page.
- **No Rate Limiting:** The current implementation does not provide a configurable request rate-limiting mechanism.
- **Authorization Verification:** The scanner requires user confirmation but cannot independently verify whether the user has legitimate permission to test the target.
- **Manual Verification Required:** Detected findings represent potential vulnerabilities and require manual verification to confirm their validity.

## Future Improvements

- Implement Boolean-based and Time-based SQL injection detection.
- Expand support for additional HTML input types, JSON payloads and standalone URL parameters.
- Improve detection accuracy and reduce false positives.
- Introduce configurable request rate limiting.
- Enhance authentication handling for different web application environments.

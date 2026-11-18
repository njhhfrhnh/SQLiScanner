# SQLiScanner

## Description

SQLiScanner is a Python-based automated vulnerability assessment tool designed to detect potential error-based SQL Injection (SQLi) vulnerabilities in web application forms. It is developed for educational security testing in authorised lab environments, such as DVWA.

The tool parses HTML forms, identifies testable input parameters, establishes baseline responses, injects SQL testing payloads, and detects database error signatures.

## Team Members

This project was collaboratively developed by four students from UniKL MIIT as part of the IKB31603 Ethical Hacking Assignment 1.

| No. | Name | Student ID | Contribution |
|---|---|---|---|
| 1 | Muhammad Hafeez bin Mohd Radzi | 52215226085 | Scanner testing, validation, documentation and report preparation. |
| 2 | Nur Najihah Farhanah binti Hashim | 52215125111 | Core scanner development, SQL injection detection logic, payload implementation, integration and overall testing. |
| 3 | Izzat Ir'fan bin Azman | 52215124710 | HTML form discovery, input parameter identification, testing and documentation. |
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

This tool is developed strictly for academic learning and defensive vulnerability assessment. Testing must only be performed on systems where explicit authorisation has been granted.

If a vulnerability is discovered during authorised testing, it must be reported privately and responsibly to the system owner with clear remediation advice, such as implementing parameterised queries or prepared statements, rather than exploiting or exfiltrating data.

## Legal Disclaimer

**LEGAL NOTICE:** This tool is intended for educational purposes and authorised security testing only. Unauthorised testing of systems without explicit permission is strictly prohibited and may constitute an offence under the Computer Crimes Act 1997 (Act 563) Malaysia. The developers assume no responsibility or liability for any misuse or damage caused by this software.

By using this tool, users acknowledge that they are responsible for obtaining proper authorisation before conducting security testing.

## Limitations

- **Error-Based Detection Only:** Currently detects SQL injection through visible database error messages. It does not support Blind SQL Injection techniques, such as Boolean-based or Time-based detection.

- **Limited Input Coverage:** Targets text and search fields discovered in HTML forms. It does not test HTTP headers, JSON payloads, or standalone URL query parameters.

- **Manual Verification Required:** All flagged findings represent potential vulnerabilities and require manual review to confirm exploitability and reduce false positives.

## Future Improvements

- Implement Boolean-based and Time-based SQL

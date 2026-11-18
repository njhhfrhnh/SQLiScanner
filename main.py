import pyfiglet
import requests
import argparse
import time
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urljoin
from pathlib import Path
from datetime import datetime

safe_hosts = {
    "localhost",
    "127.0.0.1"
}

default_target = "http://127.0.0.1"

test_types = ["text", "search", "textarea", "email", "password", "url", "tel"]

sql_error = {
    "MySQL": ["you have an error in your sql syntax", "warning: mysql"],
    "MSSQL": ["unclosed quotation mark after the character string"],
    "Oracle": ["quoted string not properly terminated"],
}

def display_banner():
    print(pyfiglet.figlet_format("SQLi Scanner", font="small"))
    print("       WELCOME TO SQL INJECTION SCANNER")
    print("\n" + "-" * 75)

def display_completion_banner():
    print(pyfiglet.figlet_format(" SQLi Scan Completed", font="small"))


def legal_disclaimer():
    disclaimer = """
    [!] LEGAL DISCLAIMER:
    This tool is intended for educational purposes and authorized security
    testing only. 

    Unauthorized testing is strictly prohibited and may constitute an offence 
    under the Computer Crimes Act 1997 (Act 563) Malaysia.
    
    The developers are not responsible for any misuse or damage resulting from
    unauthorized use of this tool.

    By proceeding, you confirm that you have permission from the system owner to
    test the target.
    """
    print(disclaimer)


def user_authorization():
      while True:
          print("-" * 55)
          print("             AUTHORIZATION CONFIRMATION")
          print("-" * 55)
          
          print("\nDo you have explicit authorization to test the target system?")
          print("\n[1] Yes")
          print("\n[2] No ")

          choice = input("\nEnter your choice: ").strip()

          if choice == '1':
            print("\n[+] Authorization confirmed. Proceeding with SQLiScanner...")
            return True
            
          elif choice == '2':
            print("\n[!] You do not have authorization to use this tool. [-] Exiting SQLiScanner...")
            return False
            
          else:
            print("\n[!] Invalid selection. Please enter 1 or 2.")


def get_target_url():
    while True:
        # prompt user for target and fall back to default if blank
        target_url = input(
            f"\nEnter the target URL [default: {default_target}]: "
            ).strip()

        if not target_url:
            target_url = default_target

        # ensure scheme is included so urlsplit parses correctly
        if "://" not in target_url:
            target_url = "http://" + target_url

        
        parsed_url = urlsplit(target_url)

        valid_hostname = (
            parsed_url.hostname == "localhost"
            or (
                parsed_url.hostname is not None
                and "." in parsed_url.hostname
            )
        )
        
        if (
            parsed_url.scheme in ["http", "https"]
            and valid_hostname
            and not parsed_url.username
            and not parsed_url.password
            and parsed_url.port !=0
        ):
            return target_url
        
        print("\n[!] Invalid URL format. Please enter a valid HTTP/HTTPS URL.")
   

def confirm_scope(target_url):
    parsed_url = urlsplit(target_url)
    target_host = parsed_url.hostname.lower()

    print(f"\n[+] Target identified: {target_host}")

    if target_host in safe_hosts:
        print("[+] Predefined safe host detected.")
        return target_host

    print("\n[!] Custom target detected.")
    print("[!] Only proceed if you have permission to test this system.")

    confirmation = input(
        f"\nType '{target_host}' to confirm the target scope: "
    ).strip()

    if confirmation.lower() == target_host:
        print("\n[+] Target scope confirmed.")
        return target_host

    print("\n[!] Target scope confirmation failed.")
    print("[!] Access denied.")
    return None


def url_in_scope(url, confirmed_scope):
    parsed_url = urlsplit(url)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.hostname:
        print("\n[!] Invalid URL.")
        return False

    target_host = parsed_url.hostname.lower()

    if target_host == confirmed_scope:
        return True

    print(f"\n[!] Out-of-scope URL detected: {url}")
    print("[!] Request blocked.")
    return False


def safe_request(session, method, url, confirmed_scope, **kwargs):
    current_url = url
    method = method.upper()

    # follow redirects manually to enforce scope checks on every hop
    for redirect_count in range(6):

        if not url_in_scope(current_url, confirmed_scope):
            raise requests.exceptions.RequestException(
                "Request blocked: URL is outside the authorized scope."
            )

        response = session.request(
            method,
            current_url,
            timeout=5,
            allow_redirects=False,
            **kwargs
        )

        if response.status_code not in [301, 302, 303, 307, 308]:
            return response

        redirect_url = response.headers.get("Location")

        if not redirect_url:
            return response

        current_url = urljoin(current_url, redirect_url)
        # rest of redirect handling 

        if response.status_code == 303 and method != "HEAD":
            method = "GET"
            kwargs.pop("data", None)
            kwargs.pop("json", None)

        elif response.status_code in [301, 302] and method == "POST":
            method = "GET"
            kwargs.pop("data", None)
            kwargs.pop("json", None)

        response.close()

    raise requests.exceptions.RequestException(
        "Maximum redirect limit exceeded."
    )


def check_target_connection(session, target_url, confirmed_scope):
    try:
        response = safe_request(
            session,
            "GET",
            target_url,
            confirmed_scope
        )

        if response.status_code < 400:
            print(f"\n[+] Successfully connected to the target URL: {target_url}")
            print(f"[+] HTTP Status Code: {response.status_code}")
            response.close()
            return True
        
        print(f"\n[!] Target returned an HTTP error: {response.status_code}")
        response.close()
        return False
        
    except requests.exceptions.RequestException as error:
        print(f"\n[!] Unable to connect to the target: {target_url}")
        print(f"[!] Error: {error}")
        return False


def get_forms(session, target_url, confirmed_scope):
    try:
        response = safe_request(
            session,
            "GET",
            target_url,
            confirmed_scope
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')

        print(f"\n[+] Found {len(forms)} form(s) on the target webpage.")
        response.close()
        return forms
    
    except requests.exceptions.RequestException as error:
        print(f"\n[!] Error fetching the target URL: {error}")
        return []


def forms_details(session, target_url, confirmed_scope):
    forms = get_forms(session, target_url, confirmed_scope)
    all_forms = []

    for form in forms:
        form_details = {
            "action": urljoin(target_url, form.get("action") or ""),
            "method": (form.get("method") or "get").lower(),
            "inputs": []
        }

        for tag in form.find_all(["input", "textarea", "select"]):
            if tag.name == "input":
                field_type = tag.get("type", "text")
                field_value = tag.get("value", "")

            elif tag.name == "textarea":
                field_type = "textarea"
                field_value = tag.text

            else:
                field_type = "select"
                option = tag.find("option", selected=True) or tag.find("option")
                field_value = option.get("value", option.text) if option else ""

            form_details["inputs"].append({
                "name": tag.get("name"),
                "type": field_type,
                "value": field_value
            })

        all_forms.append(form_details)

    return all_forms


def display_form_details(details):
    if not details:
        print("\n[!] No HTML forms found on the target webpage.")
        return
    
    print(f"\n[+] Found {len(details)} HTML form(s).")

    for index, form in enumerate(details, start=1):
        print("\n" + "-" * 50)
        print(f"Form {index}:")
        print("-" * 50)

        print(f"  Action: {form['action']}")
        print(f"  Method: {form['method'].upper()}")
        
        print(" \n Input Fields:")

        for input_index, input_field in enumerate(form["inputs"], start=1):
            print(f"  {input_index}. Name: {input_field['name']}")
            print(f"     Type: {input_field['type']}")

    print("-" * 50)


def generate_payloads():
    payloads = [
        "'",
        "\"",
        "')",
        "\")"
    ]
    return payloads


def build_form_data(form, target_param=None, payload=None):
    data = {}
    for field in form["inputs"]:
        name = field["name"]
        if name:
            data[name] = payload if name == target_param else field["value"]
    return data


def inject_payload(session, form_details, payload, confirmed_scope, parameter_name):
    target_url = form_details["action"]
    method = form_details["method"].upper()

    if not url_in_scope(target_url, confirmed_scope):
        return None

    data = build_form_data(form_details, parameter_name, payload)

    try:
        if method == "GET":
            response = safe_request(
                session, method, target_url, confirmed_scope, params=data
                )
            
        elif method == "POST":
            response = safe_request(
                session, method, target_url, confirmed_scope, data=data
                )
            
        else:
            print(f"\n[!] Unsupported HTTP method: {method}")
            return None

        return response
    
    except requests.exceptions.RequestException as error:
        print(f"\n[!] Payload submission failed: {error}")
        return None


def analyze_response(response):
    if response is None:
        return None

    response_text = response.text.lower()

    for dbms, signatures in sql_error.items():
        for signature in signatures:
            if signature in response_text:
                return dbms, signature

    return None


def baseline_response(session, form_details, confirmed_scope):
    target_url = form_details["action"]
    method = form_details["method"].upper()

    data = build_form_data(form_details)

    try:
        if method == "GET":
            response = safe_request(
                session, method, target_url, confirmed_scope, params=data
            )

        elif method == "POST":
            response = safe_request(
                session, method, target_url, confirmed_scope, data=data
            )

        else:
            return None

        return response

    except requests.exceptions.RequestException as error:
        print(f"\n[!] Baseline request failed: {error}")
        return None


def sqli_scan(session, forms_details, confirmed_scope):
    payloads = generate_payloads()
    results = []
    interrupted = False

    try:
        for form_index, form in enumerate(forms_details, start=1):
            print(f"\n[*] Scanning Form {form_index}...")

            # only target text or search input fields for injection
            parameters = [
                field["name"]
                for field in form["inputs"]
                if field["name"] and field["type"] in ["text", "search"]
            ]

            # get baseline response to compare against error signatures
            baseline = baseline_response(session, form, confirmed_scope)

            if baseline is None:
                continue

            baseline_finding = analyze_response(baseline)
            baseline.close()

            for parameter_name in parameters:
                print(f"\n[*] Testing parameter: {parameter_name}")

                for payload in payloads:
                    print(f"[*] Testing payload: {payload}")

                    response = inject_payload(
                        session, form, payload, confirmed_scope, parameter_name
                    )

                    if response is None:
                        continue

                    finding = analyze_response(response)
                    response.close()

                    # flag vulnerability if sql error appears and wasn't in baseline
                    if finding and not baseline_finding:
                        dbms, evidence = finding

                        print(f"[!] Possible SQL Injection detected! (DBMS: {dbms})")
                        
                        results.append({
                            "form": form_index,
                            "action": form["action"],
                            "method": form["method"],
                            "parameter": parameter_name,
                            "payload": payload,
                            "dbms": dbms,
                            "evidence": evidence
                        })
                        break
  
                    else:
                        print("[+] No new SQL error detected.")

    except KeyboardInterrupt:
        interrupted = True
        print("\n[!] Kill switch activated!")
        print("[!] Stopping the scan and preserving collected findings...")

    return results, interrupted


def sqli_results(results, interrupted=False):
    print("\n" + "=" * 55)
    print("                SQLi SCAN RESULTS")
    print("=" * 55)

    if not results:
        if interrupted:
            print("\n[!] Scan interrupted. No findings were collected.")

        else:
            print("\n[+] No potential SQL injection vulnerabilities detected.")

    else:
        print(f"\n[!] Found {len(results)} potential finding(s).")

        for index, result in enumerate(results, start=1):
            print("\n" + "-" * 55)
            print(f"Finding {index}")
            print("-" * 55)

            print(f"Form: {result['form']}")
            print(f"URL: {result['action']}")
            print(f"Method: {result['method'].upper()}")
            print(f"Parameter: {result['parameter']}")
            print(f"Payload: {result['payload']}")
            print(f"Database: {result['dbms']}")
            print(f"Evidence: {result['evidence']}")
            print("Status: Potential SQL Injection")

    if not interrupted:
        display_completion_banner()


def save_report(target_url, forms, results, status="Completed"):
    # ensure output directory exists locally before writing report
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"scan_report_{timestamp}.txt"

    # write structured scan summary and findings to text file
    with open(report_path, "w", encoding="utf-8") as report:
        report.write("=" * 60 + "\n")
        report.write("              SQLi SCANNER REPORT\n")
        report.write("=" * 60 + "\n\n")

        report.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Target URL: {target_url}\n")
        report.write(f"Scan Status: {status}\n\n")

        report.write("-" * 60 + "\n")
        report.write("SCAN SUMMARY\n")
        report.write("-" * 60 + "\n")

        report.write(f"Forms Discovered: {len(forms)}\n")

        parameters = [
            field["name"]
            for form in forms
            for field in form["inputs"]
            if field["name"] and field["type"] in ["text", "search"]
        ]

        report.write(f"Parameters Tested: {len(parameters)}\n")
        report.write(f"Potential Findings: {len(results)}\n\n")

        report.write("-" * 60 + "\n")
        report.write("SCAN FINDINGS\n")
        report.write("-" * 60 + "\n")

        if not results:
            report.write("No potential SQL injection vulnerabilities detected.\n")

        else:
            for index, result in enumerate(results, start=1):
                report.write(f"\nFinding {index}\n")
                report.write(f"Form: {result['form']}\n")
                report.write(f"URL: {result['action']}\n")
                report.write(f"Method: {result['method'].upper()}\n")
                report.write(f"Parameter: {result['parameter']}\n")
                report.write(f"Payload: {result['payload']}\n")
                report.write(f"Database: {result['dbms']}\n")
                report.write(f"Evidence: {result['evidence']}\n")
                report.write("Status: Potential SQL Injection\n")

        report.write("\n" + "=" * 60 + "\n")
        report.write("NOTE: Findings are potential vulnerabilities and require manual verification.\n")

    print(f"\n[+] Scan report saved successfully: {report_path}")


def parse_arguments():

    examples = """
Examples:
  python main.py --dry-run
  python main.py --cookie "PHPSESSID=your_session_id; security=low"
"""

    parser = argparse.ArgumentParser(
        description="SQL Injection Scanner for authorized security testing",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate target and scope without sending HTTP requests"
    )

    parser.add_argument(
        "--cookie",
        help="Session cookie for pages behind a login"
    )

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        session = requests.Session()

        if args.cookie:
            session.headers.update({"Cookie": args.cookie})

        display_banner()
        legal_disclaimer()

        input("Press Enter to continue...")
   
        authorized = user_authorization()
        if not authorized:
            return

        target_url = get_target_url()

        confirmed_scope = confirm_scope(target_url)
        if confirmed_scope is None:
            return

        in_scope = url_in_scope(target_url, confirmed_scope)
        if not in_scope:
            return

        if args.dry_run:
            print("\n[+] Dry run mode enabled. No HTTP requests will be sent.")
            return
    
        reachable = check_target_connection(session, target_url, confirmed_scope)
        if not reachable:
            return

        details = forms_details(session,target_url, confirmed_scope)
        display_form_details(details)
        if not details:
            return
        
        results, interrupted = sqli_scan(session, details, confirmed_scope)
        sqli_results(results, interrupted)

        if interrupted:
            save_report(target_url, details, results, "Interrupted")
            print("\n[+] Partial scan report saved successfully.")

        else:
            save_report(target_url, details, results, "Completed")

    except KeyboardInterrupt:
        print("\n[!] Kill switch activated!")
        print("[!] SQLiScanner has been stopped safely.")



if __name__ == "__main__":
    main()

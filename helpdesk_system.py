
import json
import os
import platform
import re
import subprocess
from datetime import datetime

tickets = {}
ticket_counter = 100
audit_trail = []

ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def validate_urgency(urgency="3"):
    """Validate and return a ticket urgency between 1 and 5."""
    try:
        priority = int(urgency)
    except (TypeError, ValueError) as exc:
        raise ValueError("Urgency must be an integer from 1 to 5.") from exc

    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    return priority


def raise_ticket(user, issue_type, urgency="3", audit_log=None):
    """Create a ticket and record its creation in the audit log."""
    global ticket_counter

    if not isinstance(user, str) or not user.strip():
        raise ValueError("User name cannot be empty.")
    if not isinstance(issue_type, str) or not issue_type.strip():
        raise ValueError("Issue type cannot be empty.")

    priority = validate_urgency(urgency)
    ticket_counter += 1

    tickets[ticket_counter] = {
        "user": user.strip(),
        "issue": issue_type.strip(),
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    log = audit_trail if audit_log is None else audit_log
    log.append(
        f"{user.strip()} raised #{ticket_counter} "
        f"at {datetime.now().isoformat(timespec='seconds')}"
    )
    return ticket_counter


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in tickets:
        return False
    if not isinstance(technician, str) or not technician.strip():
        return False

    tickets[ticket_id]["tech"] = technician.strip()
    return True


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in tickets:
        return False
    if not isinstance(note, str) or not note.strip():
        return False

    tickets[ticket_id]["notes"].append(note.strip())
    return True


def close_ticket(ticket_id, password):
    """Close a ticket using the configured administrator password."""
    if not ADMIN_PASSWORD or password != ADMIN_PASSWORD:
        return False
    if ticket_id not in tickets:
        return False

    del tickets[ticket_id]
    return True


def unresolved_high_priority():
    """Return unassigned tickets with urgency of at least four."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a validated hostname without invoking a shell."""
    if not isinstance(hostname, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9.-]*", hostname
    ):
        raise ValueError("Enter a valid hostname or IP address.")

    if platform.system() == "Windows":
        command = ["ping", "-n", "1", hostname]
    else:
        command = ["ping", "-c", "1", hostname]

    try:
        result = subprocess.run(
            command,
            check=False,
            timeout=10,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return 1

    return result.returncode


def save_tickets(file="tickets.json"):
    """Save tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as ticket_file:
        json.dump(tickets, ticket_file, indent=4)


def main():
    """Demonstrate the helpdesk ticket workflow."""
    first_ticket = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    third_ticket = raise_ticket("joe", "vpn", "2")

    assign_ticket(first_ticket, "Tech-Kiran")
    add_note(first_ticket, "Printer troubleshooting started.")

    print("Unassigned high priority:", unresolved_high_priority())

    level = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ).strip() or "3"

    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as error:
        print(f"Invalid urgency: {error}")
        print("Creating the laptop ticket with default urgency 3.")
        raise_ticket("sana", "laptop", "3")

    if ADMIN_PASSWORD:
        if close_ticket(third_ticket, ADMIN_PASSWORD):
            print(f"Ticket #{third_ticket} closed.")
    else:
        print(
            "Ticket closure is disabled: set "
            "HELPDESK_ADMIN_PASSWORD to enable it."
        )

    save_tickets()
    print("Open tickets:", list(tickets))
    print("Tickets saved to tickets.json")


if __name__ == "__main__":
    main()

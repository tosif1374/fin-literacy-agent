# scripts/01_build_manifest.py
import csv

SOURCES = [
    {"file": "npci_upi_faq.pdf", "topic": "upi", "source": "NPCI", "url": "https://www.npci.org.in/what-we-do/upi/faqs"},
    {"file": "rbi_beaware_scams.pdf", "topic": "scam", "source": "RBI", "url": "https://rbikehtahai.rbi.org.in/"},
    {"file": "rbi_interest_rate_master_direction.pdf", "topic": "interest_rate", "source": "RBI", "url": "https://www.rbi.org.in/"},
    {"file": "sebi_investor_basics.pdf", "topic": "budgeting", "source": "SEBI", "url": "https://investor.sebi.gov.in/"},
]

with open("data/manifest.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "topic", "source", "url"])
    writer.writeheader()
    writer.writerows(SOURCES)
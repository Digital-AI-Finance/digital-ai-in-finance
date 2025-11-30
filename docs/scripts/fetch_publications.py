"""
Fetch joint publications from OpenAlex API
Authors: Joerg Osterrieder AND Stephen Chan
"""

import requests
import json
from pathlib import Path

# OpenAlex API endpoints
OPENALEX_WORKS = "https://api.openalex.org/works"
OPENALEX_AUTHORS = "https://api.openalex.org/authors"

# Joerg Osterrieder's OpenAlex author ID (136 works)
OSTERRIEDER_ID = "A5032430973"

def search_publications():
    """Search OpenAlex for joint publications"""

    print("Fetching publications by Joerg Osterrieder...")

    # Search by author ID
    params = {
        "filter": f"author.id:{OSTERRIEDER_ID}",
        "per_page": 200,
        "sort": "publication_year:desc"
    }

    response = requests.get(OPENALEX_WORKS, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return []

    data = response.json()
    all_works = data.get("results", [])

    print(f"Found {len(all_works)} total works")

    # Filter for works that also have Stephen Chan as co-author
    joint_publications = []
    seen_titles = set()  # To avoid duplicates

    print("\nFiltering for joint publications with Stephen Chan...")

    for work in all_works:
        authors = work.get("authorships", [])
        author_names = [a.get("author", {}).get("display_name", "") for a in authors]

        # Check if Stephen Chan is a co-author
        has_chan = any(
            "chan" in name.lower() and ("stephen" in name.lower() or "s." in name.lower())
            for name in author_names
        )

        if has_chan:
            title = work.get("title", "")
            # Skip duplicates (same title)
            title_key = title.lower().replace(" ", "")[:50]
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            pub = extract_publication_data(work)
            joint_publications.append(pub)
            print(f"  [{pub['year']}] {pub['title'][:60]}...")

    print(f"\nTotal joint publications: {len(joint_publications)}")

    return joint_publications

def extract_publication_data(work):
    """Extract relevant fields from OpenAlex work object"""

    # Get DOI
    doi = work.get("doi", "")
    if doi:
        doi = doi.replace("https://doi.org/", "")

    # Get journal/venue
    venue = work.get("primary_location", {})
    source = venue.get("source", {}) if venue else {}
    journal = source.get("display_name", "Unknown") if source else "Unknown"

    # Get authors list
    authors = []
    for authorship in work.get("authorships", []):
        author = authorship.get("author", {})
        authors.append(author.get("display_name", "Unknown"))

    # Get concepts/topics
    concepts = [c.get("display_name") for c in work.get("concepts", [])[:5]]

    return {
        "title": work.get("title", "Unknown"),
        "year": work.get("publication_year"),
        "journal": journal,
        "doi": doi,
        "doi_url": f"https://doi.org/{doi}" if doi else None,
        "citations": work.get("cited_by_count", 0),
        "authors": authors,
        "concepts": concepts,
        "open_access": work.get("open_access", {}).get("is_oa", False),
        "openalex_id": work.get("id", "")
    }

def save_publications(publications, output_path):
    """Save publications to JSON file"""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(publications)} publications to {output_path}")

def generate_markdown_table(publications):
    """Generate markdown table for Research.md"""

    if not publications:
        return "No joint publications found."

    lines = []
    lines.append("| Year | Title | Journal | Citations | DOI |")
    lines.append("|------|-------|---------|-----------|-----|")

    for pub in sorted(publications, key=lambda x: x['year'] or 0, reverse=True):
        title = pub['title'][:80] + "..." if len(pub['title']) > 80 else pub['title']
        doi_link = f"[Link]({pub['doi_url']})" if pub['doi_url'] else "-"

        lines.append(f"| {pub['year'] or 'N/A'} | {title} | {pub['journal']} | {pub['citations']} | {doi_link} |")

    return "\n".join(lines)

def main():
    # Output paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"

    # Fetch publications
    publications = search_publications()

    # Save to JSON
    json_path = data_dir / "publications.json"
    save_publications(publications, json_path)

    # Generate markdown table
    print("\n" + "="*60)
    print("MARKDOWN TABLE FOR RESEARCH.MD:")
    print("="*60 + "\n")
    print(generate_markdown_table(publications))

    # Summary stats
    if publications:
        total_citations = sum(p['citations'] for p in publications)
        print(f"\n\nSummary:")
        print(f"  Total publications: {len(publications)}")
        print(f"  Total citations: {total_citations}")
        print(f"  Year range: {min(p['year'] for p in publications if p['year'])} - {max(p['year'] for p in publications if p['year'])}")

if __name__ == "__main__":
    main()

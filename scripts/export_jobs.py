#!/usr/bin/env python3
"""
Export job data from the scraper database for Fractional Pulse website.

Reads from the SQLite database or CSV files and exports to JSON format
suitable for static site generation.
"""

import json
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scraper project to path (for database exports)
SCRAPER_PATH = "/Users/rome/Documents/projects/scrapers/fractional"


def get_session(db_path: str = None):
    """Create database session."""
    sys.path.insert(0, SCRAPER_PATH)
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_path = db_path or os.path.join(SCRAPER_PATH, "fractional_jobs.db")
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    return Session()


def generate_job_slug(company: str, title: str, job_id: str) -> str:
    """Generate URL-friendly slug for job page."""
    def slugify(text: str) -> str:
        if not text:
            return ""
        # Lowercase, replace spaces and special chars
        slug = text.lower().strip()
        slug = slug.replace("&", "and")
        slug = "".join(c if c.isalnum() or c == " " else "" for c in slug)
        slug = "-".join(slug.split())
        return slug[:50]  # Limit length

    company_slug = slugify(company) or "company"
    title_slug = slugify(title) or "role"

    # Add short hash for uniqueness
    hash_input = f"{company}-{title}-{job_id}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:6]

    return f"{company_slug}-{title_slug}-{short_hash}"


def format_compensation(job) -> dict:
    """Format compensation data for display."""
    comp_data = {
        "type": job.compensation_type or "not_disclosed",
        "display": "Not disclosed",
        "min": None,
        "max": None,
        "hourly_min": job.hourly_rate_min,
        "hourly_max": job.hourly_rate_max,
    }

    if job.compensation_type == "hourly" and job.compensation_min:
        if job.compensation_min == job.compensation_max:
            comp_data["display"] = f"${job.compensation_min:.0f}/hr"
        else:
            comp_data["display"] = f"${job.compensation_min:.0f}-${job.compensation_max:.0f}/hr"
        comp_data["min"] = job.compensation_min
        comp_data["max"] = job.compensation_max
    elif job.compensation_type == "monthly" and job.compensation_min:
        if job.compensation_min == job.compensation_max:
            comp_data["display"] = f"${job.compensation_min:,.0f}/mo"
        else:
            comp_data["display"] = f"${job.compensation_min:,.0f}-${job.compensation_max:,.0f}/mo"
        comp_data["min"] = job.compensation_min
        comp_data["max"] = job.compensation_max
    elif job.compensation_type == "annual" and job.compensation_min:
        if job.compensation_min == job.compensation_max:
            comp_data["display"] = f"${job.compensation_min:,.0f}/yr"
        else:
            comp_data["display"] = f"${job.compensation_min:,.0f}-${job.compensation_max:,.0f}/yr"
        comp_data["min"] = job.compensation_min
        comp_data["max"] = job.compensation_max

    return comp_data


def format_hours(job) -> dict:
    """Format hours commitment data."""
    hours_data = {
        "min": job.hours_per_week_min,
        "max": job.hours_per_week_max,
        "display": "Not specified",
        "bucket": None,
    }

    if job.hours_per_week_min:
        if job.hours_per_week_min == job.hours_per_week_max:
            hours_data["display"] = f"{job.hours_per_week_min:.0f} hrs/week"
        elif job.hours_per_week_max:
            hours_data["display"] = f"{job.hours_per_week_min:.0f}-{job.hours_per_week_max:.0f} hrs/week"
        else:
            hours_data["display"] = f"{job.hours_per_week_min:.0f}+ hrs/week"

        # Calculate bucket
        avg_hours = (job.hours_per_week_min + (job.hours_per_week_max or job.hours_per_week_min)) / 2
        if avg_hours < 10:
            hours_data["bucket"] = "under_10"
        elif avg_hours < 20:
            hours_data["bucket"] = "10_20"
        elif avg_hours < 30:
            hours_data["bucket"] = "20_30"
        else:
            hours_data["bucket"] = "30_plus"

    return hours_data


def categorize_role(title: str, function_category: str) -> dict:
    """Categorize role by executive function and seniority."""
    title_lower = (title or "").lower()

    # Determine primary role category
    role_type = None
    if "cfo" in title_lower or "chief financial" in title_lower:
        role_type = "cfo"
    elif "cmo" in title_lower or "chief marketing" in title_lower:
        role_type = "cmo"
    elif "cto" in title_lower or "chief technology" in title_lower or "chief technical" in title_lower:
        role_type = "cto"
    elif "coo" in title_lower or "chief operating" in title_lower:
        role_type = "coo"
    elif "chro" in title_lower or "chief human" in title_lower or "chief people" in title_lower:
        role_type = "chro"
    elif "cpo" in title_lower or "chief product" in title_lower:
        role_type = "cpo"
    elif "cro" in title_lower or "chief revenue" in title_lower:
        role_type = "cro"
    elif "ciso" in title_lower or "chief information security" in title_lower:
        role_type = "ciso"
    elif "cio" in title_lower or "chief information" in title_lower:
        role_type = "cio"
    elif "vp" in title_lower or "vice president" in title_lower:
        role_type = "vp"
    elif "director" in title_lower:
        role_type = "director"
    elif "head of" in title_lower:
        role_type = "head_of"

    return {
        "role_type": role_type,
        "function": function_category or "other",
        "is_c_level": role_type in ["cfo", "cmo", "cto", "coo", "chro", "cpo", "cro", "ciso", "cio"],
        "is_vp_level": role_type in ["vp", "director", "head_of"],
    }


def job_to_dict(job) -> dict:
    """Convert FractionalJob model to export dictionary."""
    slug = generate_job_slug(job.company_name, job.title, job.source_id)
    compensation = format_compensation(job)
    hours = format_hours(job)
    role_category = categorize_role(job.title, job.function_category)

    return {
        "job_id": f"{job.source[:2]}-{job.source_id[:10]}",
        "slug": slug,
        "title": job.title,
        "company": job.company_name or "Confidential",
        "company_url": job.company_url,

        # Location
        "location": job.location_raw or "Remote",
        "location_type": job.location_type or "remote",
        "location_restriction": job.location_restriction,
        "is_remote": job.location_type in ["remote", None],

        # Compensation
        "compensation": compensation,
        "has_salary": compensation["min"] is not None,

        # Hours
        "hours": hours,

        # Classification
        "role_type": role_category["role_type"],
        "function_category": role_category["function"],
        "is_c_level": role_category["is_c_level"],
        "is_vp_level": role_category["is_vp_level"],
        "seniority": job.seniority_tier,

        # Dates
        "date_posted": job.date_posted.isoformat() if job.date_posted else None,
        "date_scraped": job.date_scraped.isoformat() if job.date_scraped else None,
        "last_seen": job.last_seen.isoformat() if job.last_seen else None,

        # Content
        "description": job.description_raw,
        "description_snippet": (job.description_snippet or job.description_raw or "")[:500],

        # Source
        "source": job.source,
        "source_url": job.source_url,
    }


def export_jobs(output_dir: str = None, db_path: str = None) -> dict:
    """
    Export all active jobs to JSON format.

    Args:
        output_dir: Output directory path
        db_path: Database file path

    Returns:
        Export statistics
    """
    output_dir = output_dir or "/Users/rome/Documents/Fractional/data"
    os.makedirs(output_dir, exist_ok=True)

    session = get_session(db_path)

    # Import model after adding to path
    from models.database import FractionalJob

    # Query active jobs
    jobs = session.query(FractionalJob).filter(
        FractionalJob.is_active == True
    ).order_by(FractionalJob.date_posted.desc()).all()

    # Convert to export format
    jobs_data = [job_to_dict(job) for job in jobs]

    # Calculate statistics
    stats = {
        "total_jobs": len(jobs_data),
        "by_role_type": {},
        "by_function": {},
        "by_location_type": {},
        "with_salary": 0,
        "c_level": 0,
        "vp_level": 0,
    }

    for job in jobs_data:
        # Count by role type
        role = job["role_type"] or "other"
        stats["by_role_type"][role] = stats["by_role_type"].get(role, 0) + 1

        # Count by function
        func = job["function_category"] or "other"
        stats["by_function"][func] = stats["by_function"].get(func, 0) + 1

        # Count by location type
        loc = job["location_type"] or "remote"
        stats["by_location_type"][loc] = stats["by_location_type"].get(loc, 0) + 1

        # Other stats
        if job["has_salary"]:
            stats["with_salary"] += 1
        if job["is_c_level"]:
            stats["c_level"] += 1
        if job["is_vp_level"]:
            stats["vp_level"] += 1

    # Write jobs.json
    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_jobs": len(jobs_data),
        "stats": stats,
        "jobs": jobs_data,
    }

    jobs_file = os.path.join(output_dir, "jobs.json")
    with open(jobs_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(jobs_data)} jobs to {jobs_file}")
    print(f"  C-Level roles: {stats['c_level']}")
    print(f"  VP-Level roles: {stats['vp_level']}")
    print(f"  With salary disclosed: {stats['with_salary']}")
    print(f"  By role type: {stats['by_role_type']}")

    session.close()

    return stats


def export_market_stats(output_dir: str = None, db_path: str = None) -> dict:
    """
    Export market statistics for homepage and insights pages.

    Args:
        output_dir: Output directory path
        db_path: Database file path

    Returns:
        Market statistics dictionary
    """
    output_dir = output_dir or "/Users/rome/Documents/Fractional/data"
    os.makedirs(output_dir, exist_ok=True)

    session = get_session(db_path)

    from models.database import FractionalJob, ListingSnapshot

    # Get active job counts
    active_count = session.query(FractionalJob).filter(
        FractionalJob.is_active == True
    ).count()

    # Get compensation stats for jobs with hourly rates
    jobs_with_comp = session.query(FractionalJob).filter(
        FractionalJob.is_active == True,
        FractionalJob.hourly_rate_min.isnot(None)
    ).all()

    hourly_rates = [j.hourly_rate_min for j in jobs_with_comp if j.hourly_rate_min]
    avg_hourly = sum(hourly_rates) / len(hourly_rates) if hourly_rates else 0
    median_hourly = sorted(hourly_rates)[len(hourly_rates) // 2] if hourly_rates else 0

    # Get recent snapshot for trends
    latest_snapshot = session.query(ListingSnapshot).filter(
        ListingSnapshot.source == 'all'
    ).order_by(ListingSnapshot.snapshot_date.desc()).first()

    market_stats = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_active_listings": active_count,
        "compensation": {
            "sample_size": len(hourly_rates),
            "avg_hourly_rate": round(avg_hourly, 0) if avg_hourly else None,
            "median_hourly_rate": round(median_hourly, 0) if median_hourly else None,
            "disclosure_rate": round(len(hourly_rates) / active_count * 100, 1) if active_count else 0,
        },
        "trends": {},
    }

    if latest_snapshot:
        market_stats["trends"] = {
            "new_today": latest_snapshot.new_today,
            "removed_today": latest_snapshot.removed_today,
        }

    # Write market_stats.json
    stats_file = os.path.join(output_dir, "market_stats.json")
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(market_stats, f, indent=2)

    print(f"Exported market stats to {stats_file}")

    session.close()

    return market_stats


def import_from_csv(csv_path: str, output_dir: str = None) -> dict:
    """
    Import jobs from CSV file (from JobSpy/Indeed scraper).

    Args:
        csv_path: Path to CSV file
        output_dir: Output directory path

    Returns:
        Export statistics
    """
    import csv

    output_dir = output_dir or "/Users/rome/Documents/Fractional/data"
    os.makedirs(output_dir, exist_ok=True)

    jobs_data = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip non-fractional jobs
            title_lower = (row.get("title") or "").lower()
            if not any(term in title_lower for term in [
                "fractional", "cfo", "cmo", "cto", "coo", "chro", "cpo", "cro",
                "chief", "vp ", "vice president", "head of"
            ]):
                continue

            # Parse compensation
            comp_min = None
            comp_max = None
            comp_type = "not_disclosed"
            interval = (row.get("interval") or "").lower()

            if row.get("min_amount"):
                try:
                    comp_min = float(row["min_amount"])
                except (ValueError, TypeError):
                    pass

            if row.get("max_amount"):
                try:
                    comp_max = float(row["max_amount"])
                except (ValueError, TypeError):
                    pass

            if comp_min or comp_max:
                if interval == "hourly":
                    comp_type = "hourly"
                elif interval == "monthly":
                    comp_type = "monthly"
                elif interval in ["yearly", "annual"]:
                    comp_type = "annual"

            # Format compensation display
            comp_display = "Not disclosed"
            hourly_min = None
            hourly_max = None

            if comp_type == "hourly" and comp_min:
                comp_display = f"${comp_min:.0f}/hr" if comp_min == comp_max else f"${comp_min:.0f}-${comp_max or comp_min:.0f}/hr"
                hourly_min = comp_min
                hourly_max = comp_max or comp_min
            elif comp_type == "annual" and comp_min:
                comp_display = f"${comp_min:,.0f}/yr" if comp_min == comp_max else f"${comp_min:,.0f}-${comp_max or comp_min:,.0f}/yr"
                # Estimate hourly from annual (assuming 1000 hrs/year for fractional)
                hourly_min = comp_min / 1000
                hourly_max = (comp_max or comp_min) / 1000
            elif comp_type == "monthly" and comp_min:
                comp_display = f"${comp_min:,.0f}/mo" if comp_min == comp_max else f"${comp_min:,.0f}-${comp_max or comp_min:,.0f}/mo"
                # Estimate hourly from monthly (assuming ~80 hrs/month for fractional)
                hourly_min = comp_min / 80
                hourly_max = (comp_max or comp_min) / 80

            # Categorize role
            role_category = categorize_role(row.get("title"), row.get("job_function"))

            # Generate slug
            source_id = row.get("id") or row.get("job_url", "")[-20:]
            slug = generate_job_slug(row.get("company"), row.get("title"), source_id)

            # Determine location type
            location = row.get("location") or ""
            is_remote = str(row.get("is_remote", "")).lower() == "true" or "remote" in location.lower()
            location_type = "remote" if is_remote else "onsite"

            job_data = {
                "job_id": source_id[:15],
                "slug": slug,
                "title": row.get("title"),
                "company": row.get("company") or "Confidential",
                "company_url": row.get("company_url"),

                "location": location,
                "location_type": location_type,
                "location_restriction": None,
                "is_remote": is_remote,

                "compensation": {
                    "type": comp_type,
                    "display": comp_display,
                    "min": comp_min,
                    "max": comp_max,
                    "hourly_min": hourly_min,
                    "hourly_max": hourly_max,
                },
                "has_salary": comp_min is not None,

                "hours": {
                    "min": None,
                    "max": None,
                    "display": "Not specified",
                    "bucket": None,
                },

                "role_type": role_category["role_type"],
                "function_category": role_category["function"],
                "is_c_level": role_category["is_c_level"],
                "is_vp_level": role_category["is_vp_level"],
                "seniority": row.get("job_level"),

                "date_posted": row.get("date_posted"),
                "date_scraped": datetime.now().strftime("%Y-%m-%d"),
                "last_seen": datetime.now().strftime("%Y-%m-%d"),

                "description": row.get("description"),
                "description_snippet": (row.get("description") or "")[:500],

                "source": row.get("site") or "indeed",
                "source_url": row.get("job_url"),
            }

            jobs_data.append(job_data)

    # Calculate statistics
    stats = {
        "total_jobs": len(jobs_data),
        "by_role_type": {},
        "by_function": {},
        "by_location_type": {},
        "with_salary": 0,
        "c_level": 0,
        "vp_level": 0,
    }

    for job in jobs_data:
        role = job["role_type"] or "other"
        stats["by_role_type"][role] = stats["by_role_type"].get(role, 0) + 1

        func = job["function_category"] or "other"
        stats["by_function"][func] = stats["by_function"].get(func, 0) + 1

        loc = job["location_type"] or "remote"
        stats["by_location_type"][loc] = stats["by_location_type"].get(loc, 0) + 1

        if job["has_salary"]:
            stats["with_salary"] += 1
        if job["is_c_level"]:
            stats["c_level"] += 1
        if job["is_vp_level"]:
            stats["vp_level"] += 1

    # Write jobs.json
    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_jobs": len(jobs_data),
        "stats": stats,
        "jobs": jobs_data,
    }

    jobs_file = os.path.join(output_dir, "jobs.json")
    with open(jobs_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Imported {len(jobs_data)} jobs from CSV to {jobs_file}")
    print(f"  C-Level roles: {stats['c_level']}")
    print(f"  VP-Level roles: {stats['vp_level']}")
    print(f"  With salary disclosed: {stats['with_salary']}")
    print(f"  By role type: {stats['by_role_type']}")

    # Write market stats
    hourly_rates = [j["compensation"]["hourly_min"] for j in jobs_data if j["compensation"]["hourly_min"]]
    avg_hourly = sum(hourly_rates) / len(hourly_rates) if hourly_rates else 0
    median_hourly = sorted(hourly_rates)[len(hourly_rates) // 2] if hourly_rates else 0

    market_stats = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_active_listings": len(jobs_data),
        "compensation": {
            "sample_size": len(hourly_rates),
            "avg_hourly_rate": round(avg_hourly, 0) if avg_hourly else None,
            "median_hourly_rate": round(median_hourly, 0) if median_hourly else None,
            "disclosure_rate": round(len(hourly_rates) / len(jobs_data) * 100, 1) if jobs_data else 0,
        },
        "trends": {},
    }

    stats_file = os.path.join(output_dir, "market_stats.json")
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(market_stats, f, indent=2)

    print(f"Exported market stats to {stats_file}")

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export jobs for Fractional Pulse")
    parser.add_argument("--output", "-o", default="/Users/rome/Documents/Fractional/data",
                        help="Output directory")
    parser.add_argument("--db", help="Database path")
    parser.add_argument("--csv", help="Import from CSV file instead of database")

    args = parser.parse_args()

    print("Exporting job data for Fractional Pulse...")
    print("=" * 50)

    if args.csv:
        # Import from CSV
        import_from_csv(args.csv, args.output)
    else:
        # Export from database
        export_jobs(args.output, args.db)
        print()
        export_market_stats(args.output, args.db)

    print()
    print("Export complete!")

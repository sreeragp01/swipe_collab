#!/usr/bin/env python3
"""
==============================================================================
SwipeCollab - AWS S3 Automated Database & Media Backup Script
==============================================================================
This script backs up the SwipeCollab database (PostgreSQL, MySQL, or SQLite)
and user media uploads, compresses the data into Gzip archives, and uploads
them securely to an AWS S3 Backup Bucket.

Usage:
    python scripts/aws_backup.py [--dry-run] [--keep-local]
==============================================================================
"""

import os
import sys
import argparse
import datetime
import subprocess
import tarfile
import shutil
from pathlib import Path

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Try loading environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def dump_database(backup_dir, timestamp):
    """
    Creates a database dump file based on environment variables or DATABASE_URL.
    """
    db_url = os.environ.get('DATABASE_URL', '')
    db_engine = os.environ.get('DB_ENGINE', '')
    db_host = os.environ.get('DB_HOST', '')
    db_name = os.environ.get('DB_NAME', 'swipecollab')
    db_user = os.environ.get('DB_USER', '')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_port = os.environ.get('DB_PORT', '')

    dump_file = backup_dir / f"swipecollab_db_{timestamp}.sql"

    # PostgreSQL dump
    if 'postgresql' in db_engine.lower() or db_url.startswith('postgres'):
        print(f"[*] Dumping PostgreSQL database: {db_name}...")
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password

        cmd = ["pg_dump"]
        if db_host:
            cmd.extend(["-h", db_host])
        if db_port:
            cmd.extend(["-p", str(db_port)])
        if db_user:
            cmd.extend(["-U", db_user])
        cmd.extend(["-f", str(dump_file), db_name])

        try:
            subprocess.run(cmd, env=env, check=True)
            print(f"[+] PostgreSQL dump created: {dump_file}")
            return dump_file
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"[!] pg_dump command failed or not installed ({e}). Checking fallback...")

    # MySQL dump
    elif 'mysql' in db_engine.lower() or db_url.startswith('mysql'):
        print(f"[*] Dumping MySQL database: {db_name}...")
        cmd = ["mysqldump"]
        if db_host:
            cmd.extend(["-h", db_host])
        if db_port:
            cmd.extend(["-P", str(db_port)])
        if db_user:
            cmd.extend(["-u", db_user])
        if db_password:
            cmd.append(f"-p{db_password}")
        cmd.extend([db_name, "--result-file=" + str(dump_file)])

        try:
            subprocess.run(cmd, check=True)
            print(f"[+] MySQL dump created: {dump_file}")
            return dump_file
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"[!] mysqldump failed or not installed ({e}).")

    # SQLite dump fallback
    sqlite_file = BASE_DIR / 'db.sqlite3'
    if sqlite_file.exists():
        print(f"[*] Copying SQLite database file...")
        sqlite_backup = backup_dir / f"swipecollab_db_{timestamp}.sqlite3"
        shutil.copy2(sqlite_file, sqlite_backup)
        print(f"[+] SQLite database backed up to: {sqlite_backup}")
        return sqlite_backup

    print("[!] Warning: No supported active database found to dump.")
    return None


def compress_directory(source_dir, output_file):
    """
    Compresses a directory into a tar.gz archive.
    """
    if not source_dir.exists() or not any(source_dir.iterdir()):
        print(f"[*] Directory {source_dir} is empty or does not exist. Skipping compression.")
        return None

    print(f"[*] Archiving media directory: {source_dir}...")
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=source_dir.name)
    print(f"[+] Media archive created: {output_file}")
    return output_file


def compress_file(input_file):
    """
    Compresses a single file into a gzip archive.
    """
    gz_file = Path(str(input_file) + ".gz")
    print(f"[*] Gzipping database dump: {input_file}...")
    import gzip
    with open(input_file, 'rb') as f_in:
        with gzip.open(gz_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(input_file)
    print(f"[+] Database compressed to: {gz_file}")
    return gz_file


def upload_to_s3(file_path, bucket_name, s3_key, access_key=None, secret_key=None, region=None):
    """
    Uploads a file to an AWS S3 bucket.
    """
    print(f"[*] Uploading {file_path.name} to s3://{bucket_name}/{s3_key}...")
    session_kwargs = {}
    if access_key and secret_key:
        session_kwargs['aws_access_key_id'] = access_key
        session_kwargs['aws_secret_access_key'] = secret_key
    if region:
        session_kwargs['region_name'] = region

    s3_client = boto3.client('s3', **session_kwargs)

    try:
        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=bucket_name,
            Key=s3_key,
            ExtraArgs={'ServerSideEncryption': 'AES256'}
        )
        print(f"[✔] Successfully uploaded to S3: s3://{bucket_name}/{s3_key}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"[✘] S3 Upload failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="SwipeCollab Automated AWS S3 Backup Tool")
    parser.add_argument("--dry-run", action="store_true", help="Perform backup creation without uploading to S3")
    parser.add_argument("--keep-local", action="store_true", help="Keep local backup archives after uploading")
    args = parser.parse_args()

    timestamp = get_timestamp()
    backup_dir = BASE_DIR / "backups_temp"
    backup_dir.mkdir(exist_ok=True)

    print("==========================================================")
    print(f"  SwipeCollab AWS Data Backup - {timestamp}")
    print("==========================================================")

    # 1. Dump Database
    db_dump = dump_database(backup_dir, timestamp)
    compressed_db = None
    if db_dump and db_dump.exists():
        compressed_db = compress_file(db_dump)

    # 2. Archive Media Directory
    media_dir = BASE_DIR / "media"
    media_archive_file = backup_dir / f"swipecollab_media_{timestamp}.tar.gz"
    media_archive = compress_directory(media_dir, media_archive_file)

    # 3. AWS S3 Credentials and Bucket check
    bucket_name = os.environ.get('AWS_BACKUP_BUCKET_NAME') or os.environ.get('AWS_STORAGE_BUCKET_NAME')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

    if args.dry_run:
        print("\n[!] Dry Run complete. Backup files generated locally in 'backups_temp':")
        if compressed_db:
            print(f"    - {compressed_db}")
        if media_archive:
            print(f"    - {media_archive}")
        return

    if not bucket_name:
        print("\n[!] Warning: AWS_BACKUP_BUCKET_NAME or AWS_STORAGE_BUCKET_NAME is not set.")
        print("    Backup files will remain saved locally in 'backups_temp/'.")
        return

    # 4. Upload to S3
    uploaded_files = []
    if compressed_db and compressed_db.exists():
        s3_key = f"backups/database/{compressed_db.name}"
        if upload_to_s3(compressed_db, bucket_name, s3_key, access_key, secret_key, region):
            uploaded_files.append(compressed_db)

    if media_archive and media_archive.exists():
        s3_key = f"backups/media/{media_archive.name}"
        if upload_to_s3(media_archive, bucket_name, s3_key, access_key, secret_key, region):
            uploaded_files.append(media_archive)

    # 5. Clean up temporary local files
    if not args.keep_local:

        print("[*] Cleaning up temporary local backup archives...")
        for f in [compressed_db, media_archive]:
            if f and f.exists():
                os.remove(f)
        if backup_dir.exists() and not any(backup_dir.iterdir()):
            os.rmdir(backup_dir)

    print("\n[✔] AWS Data Backup completed successfully!")


if __name__ == "__main__":
    main()

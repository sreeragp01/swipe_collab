# SwipeCollab - AWS Free Tier Migration & Data Security Guide

This guide provides step-by-step instructions to migrate **SwipeCollab** from Render to **Amazon Web Services (AWS)** using **100% AWS Free Tier eligible resources**, along with configuring automated database backups and billing safeguards.

---

## 🛡️ Step 0: Set Up AWS Billing Protection ($0 Budget Alarm)

Before creating any AWS resources, set up a zero-cost alert to ensure you never incur unexpected charges.

1. Log into your **AWS Management Console**.
2. Search for **AWS Budgets** in the top search bar.
3. Click **Create budget** -> Select **Cost budget** (Simplified).
4. Set the budget parameters:
   - **Period**: Monthly
   - **Target amount**: `$0.01` (or `$1.00`)
5. Under **Alert thresholds**, set an alert for **100% of budgeted amount** (`$0.01`).
6. Enter your **Email address** to receive immediate alerts if any service exceeds $0.
7. Click **Create budget**.

---

## 🗄️ Step 1: Provision AWS RDS Database (Free Tier Eligible)

AWS offers 750 free monthly hours of single-AZ `db.t3.micro` or `db.t4g.micro` database instances, plus 20 GB of SSD storage and 20 GB of automated backup storage.

1. Go to the **AWS RDS Console** -> Click **Create database**.
2. Select **Standard create**:
   - **Engine type**: **PostgreSQL** (or MySQL)
   - **Templates**: Select **Free tier**
3. **Settings**:
   - **DB instance identifier**: `swipecollab-db`
   - **Master username**: `swipeadmin`
   - **Master password**: *[Choose a strong password]*
4. **Instance configuration**:
   - Select `db.t3.micro` or `db.t4g.micro` (1 vCPU, 1 GB RAM)
5. **Storage**:
   - **Storage type**: General Purpose SSD (gp2 or gp3)
   - **Allocated storage**: `20` GB (maximum free tier limit)
   - **Storage autoscaling**: *Uncheck Enable storage autoscaling* (prevents billing increases)
6. **Connectivity**:
   - **Virtual Private Cloud (VPC)**: Default VPC
   - **Public access**: *No* (Recommended for security; connect via EC2)
   - **VPC security group**: Create new `swipecollab-rds-sg`
7. **Additional configuration**:
   - **Initial database name**: `swipecollab`
   - **Enable automated backups**: Checked (Retention period: `7` days - free of charge)
8. Click **Create database**. Copy the **Endpoint** address once creation completes.

---

## 🪣 Step 2: Create AWS S3 Media & Backup Buckets (Free Tier)

AWS S3 gives you **5 GB of Standard Storage** free for 12 months.

1. Go to the **AWS S3 Console** -> Click **Create bucket**.
2. **Bucket name**: `swipecollab-media-storage` (Must be globally unique)
3. **Region**: `us-east-1` (or your preferred AWS region)
4. **Object Ownership**: ACLs disabled (recommended)
5. **Block Public Access**: *Uncheck Block all public access* if serving media uploads directly from S3 (or keep checked if using CloudFront).
6. Click **Create bucket**.
7. *(Optional)* Create a secondary bucket `swipecollab-database-backups` for database backups with **Block all public access** set to **True**.

### Configure S3 Bucket Policy for Media Access
Navigate to `swipecollab-media-storage` -> **Permissions** -> **Bucket Policy** -> Paste:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::swipecollab-media-storage/media/*"
    }
  ]
}
```

---

## 🚚 Step 3: Export Existing Database & Media from Render

1. Log into your Render Dashboard.
2. Under your PostgreSQL database, copy the **Internal / External Connection String**.
3. Run the export command on your local machine:
   ```bash
   pg_dump "postgres://user:password@render-host.render.com/dbname" -F p -f render_dump.sql
   ```
4. If using local SQLite / Render media, compress your `media/` folder:
   ```bash
   tar -czvf render_media.tar.gz media/
   ```

---

## 💻 Step 4: Launch AWS EC2 Instance (Free Tier Compute)

AWS provides **750 hours/month** for `t2.micro` or `t3.micro` instances.

1. Go to **AWS EC2 Console** -> Click **Launch Instance**.
2. **Name**: `SwipeCollab-Server`
3. **OS Image**: **Ubuntu 24.04 LTS** (Free Tier eligible)
4. **Instance Type**: `t3.micro` or `t2.micro` (1 vCPU, 1 GB RAM)
5. **Key Pair**: Create or select an existing SSH Key pair (`swipecollab-key.pem`).
6. **Network Settings (Security Group)**:
   - Allow **SSH (Port 22)** from your IP
   - Allow **HTTP (Port 80)** from Anywhere (`0.0.0.0/0`)
   - Allow **HTTPS (Port 443)** from Anywhere (`0.0.0.0/0`)
7. **Storage**: `30` GB gp3 SSD (Free Tier allows up to 30 GB total EBS storage)
8. Click **Launch Instance**.

---

## ⚙️ Step 5: Server Configuration & RAM Optimization

1. SSH into your EC2 Instance:
   ```bash
   ssh -i swipecollab-key.pem ubuntu@<YOUR-EC2-PUBLIC-IP>
   ```

2. **Add 2 GB Virtual Swap Memory** (Crucial to prevent OOM errors on 1 GB RAM):
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

3. **Install Docker & Git**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y docker.io docker-compose git postgresql-client
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

4. **Clone Codebase & Environment Variables**:
   ```bash
   git clone <YOUR-GIT-REPOSITORY-URL> swipe_collab
   cd swipe_collab
   cp .env.aws.example .env
   nano .env
   ```
   *Fill in your RDS host, database user, password, S3 bucket name, and AWS API keys in `.env`.*

5. **Import Render Database into AWS RDS**:
   ```bash
   psql -h <YOUR-RDS-ENDPOINT> -U swipeadmin -d swipecollab -f render_dump.sql
   ```

6. **Start SwipeCollab with Docker Compose**:
   ```bash
   docker-compose -f deploy/docker-compose.prod.yml up -d --build
   ```

7. **Run Database Migrations & Static Collection inside container**:
   ```bash
   docker-compose -f deploy/docker-compose.prod.yml exec web python manage.py migrate
   docker-compose -f deploy/docker-compose.prod.yml exec web python manage.py collectstatic --no-input
   ```

---

## 🔐 Step 6: SSL Certificate Setup (Let's Encrypt / Certbot)

To secure traffic with free HTTPS:
1. Install Certbot on EC2:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   ```
2. Point your domain (e.g. `swipecollab.com`) A-Record to `<YOUR-EC2-PUBLIC-IP>` in your domain DNS control panel.
3. Run Certbot to generate and auto-install free SSL certificate:
   ```bash
   sudo certbot --nginx -d swipecollab.com -d www.swipecollab.com
   ```

---

## 🔒 Step 7: Automated S3 Database & Media Backups

We have included `scripts/aws_backup.py` which compresses database dumps and media files, encrypting them and uploading directly to your S3 bucket.

1. Test the backup script on EC2:
   ```bash
   python3 scripts/aws_backup.py
   ```

2. **Schedule Daily Automated Cron Job** (Every night at 2:00 AM):
   ```bash
   crontab -e
   ```
   Add the following line:
   ```cron
   0 2 * * * cd /home/ubuntu/swipe_collab && /usr/bin/python3 scripts/aws_backup.py >> /home/ubuntu/backup.log 2>&1
   ```

3. **Verify S3 Lifecycle Policy**:
   In your AWS S3 Console for `swipecollab-database-backups`:
   - Go to **Management** -> **Create lifecycle rule**
   - **Rule Name**: `AutoDeleteOldBackups`
   - **Prefix**: `backups/`
   - **Expiration**: Expire objects after **30 days**
   *(This ensures backup files are auto-cleaned so you stay under the 5 GB S3 free storage threshold).*

---

## 🚀 Migration Verification Checklist

- [ ] AWS Billing Alarm set to $0.01
- [ ] AWS RDS Database running on `db.t3.micro` with 20 GB storage
- [ ] AWS S3 Bucket configured and tested for media uploads
- [ ] 2 GB Swap file configured on EC2
- [ ] Website accessible via HTTPS with valid SSL certificate
- [ ] WebSockets (Chat & Real-time Notifications) operating smoothly over WSS
- [ ] Daily backup cron job scheduled and verified in S3

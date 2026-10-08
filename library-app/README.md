# Library Management System (Python Console App)

Console app using Python + SQLite. Deployed to AWS EC2 with Docker and GitHub Actions.

## Run locally
    python -m app.main

## Run tests
    pip install -r requirements.txt
    python -m pytest -v

## Run with Docker
    docker build -t library-app .
    docker run -it --rm -v library_data:/data library-app

## Deploy on AWS EC2 (one-time setup)
1. Launch EC2 (Amazon Linux 2023, t2.micro / t3.micro). Security Group: SSH (22) from My IP.
2. SSH in:  ssh -i key.pem ec2-user@<EC2_PUBLIC_IP>
3. Install tools:
       sudo dnf install -y docker git
       sudo systemctl enable --now docker
       sudo usermod -aG docker ec2-user      # then logout and login again
4. Clone the repo:  git clone https://github.com/<you>/library-app.git ~/library-app
5. In GitHub repo -> Settings -> Secrets -> Actions, add:
   EC2_HOST (public IP), EC2_USER (ec2-user), EC2_SSH_KEY (full contents of the .pem file)
6. Push to main -> tests run -> EC2 pulls code and rebuilds image.
7. Use the app on EC2:
       docker run -it --rm -v library_data:/data library-app

## Pipeline
push to main -> pytest -> SSH into EC2 -> git pull -> docker build

# Docker Firewall 🛡️

✨ **__Features__**

🔍 Real-time port scan detection<br>
🚫 Automatic IP blocking for 30 minutes<br>
🐳 Docker-based deployment for easy setup and management<br>

📦 **Prerequisites**

· Linux-based operating system<br>
· sudo privileges<br>

🚀 **Installation**
1. Install Required Dependencies
The following command will install Docker.io and necessary dependencies:

```bash
sudo apt update && \
sudo apt install -y docker.io curl jq && \
sudo curl -L "https://github.com/docker/compose/releases/download/v2.19.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose
```

💡 Usage
Once running, the firewall will automatically:

· Monitor incoming connections<br>
· Detect port scanning attempts<br>
· Block suspicious IP addresses for 30 minutes<br>

👥 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create.<br> Any contributions you make are greatly appreciated.

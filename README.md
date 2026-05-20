# PS4 PKG Sender Docker Container

A lightweight Docker container for sending PS4 PKG files over your network.

## 📋 Setup

- **Server IP**: 10.10.10.57
- **Server Port**: 58880
- **PS4 IP**: 10.10.10.120
- **Network**: 10.10.10.0/24

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Network connectivity between server and PS4

### Build & Deploy

```bash
# Clone the repository
git clone https://github.com/mccarthyah/ps4-pkg-sender.git
cd ps4-pkg-sender

# Create pkgs directory
mkdir -p pkgs

# Build and start the container
docker-compose up -d

# Verify it's running
curl http://10.10.10.57:58880/health
```

## 📁 Adding PKG Files

Place your PS4 PKG files in the `pkgs/` directory:

```bash
cp your_game.pkg pkgs/
```

## 🔌 API Endpoints

### Health Check
```bash
curl http://10.10.10.57:58880/health
```

### List Available PKGs
```bash
curl http://10.10.10.57:58880/list
```

### Download PKG
```bash
curl -O http://10.10.10.57:58880/pkgs/filename.pkg
```

### Upload PKG
```bash
curl -F "file=@your_game.pkg" http://10.10.10.57:58880/upload
```

### Server Info
```bash
curl http://10.10.10.57:58880/info
```

## 🛠️ Docker Commands

```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker-compose logs -f

# Rebuild container
docker-compose build --no-cache
docker-compose up -d
```

## 📦 Project Structure

```
ps4-pkg-sender/
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Docker Compose configuration
├── server.py           # Flask application
├── requirements.txt    # Python dependencies
├── pkgs/               # PKG files directory (created at runtime)
└── README.md           # This file
```

## 🐛 Troubleshooting

### Container won't start
```bash
docker-compose logs -f ps4-pkg-sender
```

### Can't reach server from PS4
- Verify network connectivity: `ping 10.10.10.57`
- Check firewall settings
- Ensure port 58880 is not blocked

### Permission denied on pkgs directory
```bash
sudo chown $USER:$USER pkgs/
chmod 755 pkgs/
```

## 📝 License

MIT

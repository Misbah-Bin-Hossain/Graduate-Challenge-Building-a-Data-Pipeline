# Star Wars Data Pipeline Project

This project demonstrates how to build a data pipeline that extracts data from the Star Wars API (SWAPI) and stores it in a PostgreSQL database.

## Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.7 or higher
- Required Python packages (see requirements.txt)

## Step 2: Set Up PostgreSQL Using Docker

### What is Docker Compose?

Docker Compose is a tool that allows you to define and run multi-container Docker applications. In our case, we'll use it to run a PostgreSQL database container.

### Starting the Database

1. **Open your terminal/command prompt** in the project directory
2. **Start the PostgreSQL container** by running:
   ```bash
   docker-compose up -d
   ```
   The `-d` flag runs the container in the background (detached mode)

3. **Verify the container is running**:
   ```bash
   docker ps
   ```
   You should see a container named `starwars_postgres` running

4. **Check the logs** (optional):
   ```bash
   docker-compose logs postgres
   ```

### Database Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: starwars_db
- **Username**: starwars_user
- **Password**: starwars_password

### Stopping the Database

When you're done working:
```bash
docker-compose down
```

To also remove the data volume (this will delete all data):
```bash
docker-compose down -v
```

### Troubleshooting

**If you get a port conflict error:**
- Another PostgreSQL instance might be running on port 5432
- Change the port in `docker-compose.yml` from `"5432:5432"` to `"5433:5432"`

**If the container won't start:**
- Check if Docker is running
- Ensure no other containers are using the same name
- Check the logs: `docker-compose logs postgres`

## Project Structure

```
├── docker-compose.yml          # Docker configuration for PostgreSQL
├── discover_api_fixed.py       # Script to explore SWAPI
├── Get Data.py                 # Script to get Star Wars data
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Next Steps

After setting up the database, you can:
1. Create database tables for Star Wars data
2. Modify the Python scripts to save data to PostgreSQL
3. Build a complete ETL pipeline

## Useful Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View running containers
docker ps

# View logs
docker-compose logs

# Restart services
docker-compose restart

# Remove everything including volumes
docker-compose down -v
```
## To create a service that runs a FastAPI application within a virtual environment (venv) on Ubuntu boot, you can follow these steps:

## Prerequisites:

```bash
sudo apt install -y libcups2-dev
```

## [Add Printers on Cups](http://localhost:631/admin)

## Useful Links

- [RaspberryPi Printer Server](https://www.tomshardware.com/how-to/raspberry-pi-print-server)
- [Create A Ubuntu Automated Service](https://www.makeuseof.com/use-autokey-to-automate-repetitive-tasks-on-linux/)
- [Deploy FastAPI on Server](https://dev.to/ndrohith/deploy-fastapi-application-on-digital-ocean-with-nginx-and-gunicorn-2lnk)

## 1. Create a Systemd Service Unit File:

Create a systemd service unit file to manage your FastAPI application as a service. Create a file named, for example, `myapp.service` in the `/etc/systemd/system/` directory with the following content:

   ```bash
   [Unit]
   Description=FastPrinterHost Service
   After=network.target

   [Service]
   User=mazhar
   Group=www-data
   WorkingDirectory=/home/mazhar/PycharmProjects/FastAPI-Practice/server
   Environment="PATH=/home/mazhar/PycharmProjects/FastAPI-Practice/venv/bin"
   ExecStart=/home/mazhar/PycharmProjects/FastAPI-Practice/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 2. Enable and Start the Service:

Run the following commands to enable and start the systemd service:

   ```bash
   sudo systemctl enable myapp.service
   sudo systemctl start myapp.service
   ```

This will start your FastAPI application as a service and configure it to start on boot.

## 3. Check the Status:

You can check the status of the service using:

   ```bash
   sudo systemctl status myapp.service
   ```

Make sure your FastAPI application is running as expected.

Your FastAPI application should now run as a service on Ubuntu boot. Make sure to replace the placeholder values in the systemd unit file with your actual values.
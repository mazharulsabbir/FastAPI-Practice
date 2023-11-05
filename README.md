sudo apt install -y libcups2-dev

[Unit]
Description=Gunicorn instance to serve FastPrinterHost
After=network.target

[Service]
User=<username>
Group=www-data
WorkingDirectory=/root/fast-api-ocean
Environment="PATH=/root/fast-api-ocean/venv/bin"
ExecStart=/root/fast-api-ocean/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app

[Install]
WantedBy=multi-user.target

import os
import sys
import cups  # pip install pycups
import tempfile

from fastapi import FastAPI
from pydantic import BaseSettings
from pydantic import BaseModel
from httpx import AsyncClient


class PrintPdfDetails(BaseModel):
    printer_name: str
    pdf_link: str


class Settings(BaseSettings):
    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


# Initialize the FastAPI app for a simple web server
app = FastAPI(title='FastAPI-Practice')
client = AsyncClient()

if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)


@app.get("/")
async def root():
    return {"success": True, "message": "Link working!!"}


@app.get("/my/printers")
async def get_client_printers():
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_list = []
    for printer in printers:
        printer_list.append({
            'name': printer,
            'device_uri': printers[printer]['device-uri']
        })

    return {"success": True, "message": "%s printer(s) found" % (len(printer_list)), "printers": printer_list}


@app.post("/print-pdf")
async def print_pdf(details: PrintPdfDetails):
    try:
        response = await client.get(details.pdf_link)
        if response.status_code == 200:
            file_content = response.content
        else:
            raise Exception("Failed to download the file.")

        # Save the file to a temporary location on the disk
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_content)
        temp_file.close()

        # Connect to the CUPS server
        conn = cups.Connection()

        printers = conn.getPrinters()
        if details.printer_name not in printers:
            return {"success": False, "message": "Printer not found"}

        # Print the file
        job_id = conn.printFile(details.printer_name, temp_file.name, "Print job", {})

        # Remove the temporary file
        os.remove(temp_file.name)

        # Check the print job status
        print_status = conn.getJobAttributes(job_id, ['job-state'])
        job_state = print_status['job-state']
        return {"success": True, "message": "Print job submitted successfully", "job_state": job_state}
    except Exception as e:
        return {"success": False, "message": str(e)}

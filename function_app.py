import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import uuid
import logging
from azure.eventhub import EventHubProducerClient, EventData

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="eh1",
                               connection="EventHubConnection") 
def eventhub_trigger1(azeventhub: func.EventHubEvent):
    event_dec = azeventhub.get_body().decode('utf-8')
    logging.info('Gtms new Python EventHub trigger %s processed an event: %s',
                'eh1', event_dec)
    publish_to_blob(event_dec, os.environ["BlobName1"])


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="mh2",
                               connection="EventHubConnection") 
def eventhub_trigger2(azeventhub: func.EventHubEvent):
    event_dec = azeventhub.get_body().decode('utf-8')
    logging.info('Gtms new Python EventHub trigger %s processed an event: %s',
                'mh2', event_dec)
    publish_to_blob(event_dec, os.environ["BlobName2"])
    

def publish_to_blob(data,blobname):
    localDemoContainer = str(uuid.uuid4())
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ["BlobConnectionString"])
        container_client = blob_service_client.get_container_client(localDemoContainer)

        # Create a container if not exists
        if not container_client.exists():
            container_client.create_container()

        blob_client = blob_service_client.get_blob_client(container=localDemoContainer, blob=blobname)

        # Upload data to the blob
        blob_client.upload_blob(data, overwrite=True)
        logging.info(f"Blob {blobname} created with data: {data}")
    except Exception as ex:
        logging.error(f"Failed to upload blob: {ex}")


@app.function_name(name="HttpTriggerToEventHub")
@app.route(route="send-to-eventhub", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def send_to_eventhub(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')

    # Read data from the HTTP request
    data = req.get_json()
    headers = req.headers

    # Event Hub connection string and name
    connection_str = os.environ["EventHubConnection"]
    eventhub_name = headers.get('eventhub_name')

    # Create an Event Hub producer client
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, eventhub_name=eventhub_name
    )

    # Send data to Event Hub
    with producer:
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(str(data)))
        producer.send_batch(event_data_batch)

    return func.HttpResponse("Data sent to Event Hub successfully!")
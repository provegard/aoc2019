# [START functions_calc_fuel]
def calc_fuel(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64
    import math
    import json
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("per-aoc-2019", "aoc_2019_1_agg")

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        massStr = base64.b64decode(event['data']).decode('utf-8')
        mass = int(massStr)
        fuel = math.floor(mass / 3) - 2

        fuelObj = {"fuel":fuel}
        data = json.dumps(fuelObj)

        print("Publishing FUEL '%s' on topic %s" % (data, topic_path))
        future = publisher.publish(
            topic_path, data=data.encode('utf-8')  # data must be a bytestring.
        )
        print(future.result())

    else:
        print("Missing data in event :(")
# [END functions_calc_fuel]

# [START functions_parse_input]
def parse_input(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64
    import json
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("per-aoc-2019", "aoc_2019_1_mass")
    topic_path_agg = publisher.topic_path("per-aoc-2019", "aoc_2019_1_agg")

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        inputStr = base64.b64decode(event['data']).decode('utf-8')
        masses = inputStr.split(";")
        print("Got %d input masses" % (len(masses),))

        countObj = {"count":len(masses)}
        data = json.dumps(countObj)
        print("Publishing '%s' on topic %s" % (data, topic_path_agg))
        future = publisher.publish(
            topic_path_agg, data=data.encode('utf-8')  # data must be a bytestring.
        )
        print("future = %s" % (future.result(),))

        for mass in masses:
            data = mass
            print("Publishing '%s' on topic %s" % (data, topic_path))
            future = publisher.publish(
                topic_path, data=data.encode('utf-8')  # data must be a bytestring.
            )
            print("future = %s" % (future.result(),))
        print("Done publishing masses")

    else:
        print("Missing data in event :(")
# [END functions_parse_input]

# [START functions_aggregate]
def aggregate(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64
    from google.cloud import storage
    import json

    storage_client = storage.Client()

    bucket_name = "provegard_aoc_2019"

    bucket = storage_client.get_bucket(bucket_name)
    print("Bucket versioning enabled = %s" % (bucket.versioning_enabled,))

    origMultipartUrl = storage.blob._MULTIPART_URL_TEMPLATE
    origResumableUrl = storage.blob._RESUMABLE_URL_TEMPLATE

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        success = False
        attempt = 1
        while not success:
            print("Attempt %d" % (attempt,))
            attempt += 1

            blob = bucket.get_blob("day1", client=storage_client)

            generation = None
            try:
                print("Loading the model")
                contents = blob.download_as_string(client=storage_client).decode("utf-8")
                generation = blob.generation
            except:
                print("No day1 blob found, starting from empty")
                blob = bucket.blob("day1")
                contents = '{"count":0,"fuels":[]}'

            print("Blob generation = %s" % (generation,))

            expectGen = 0
            if not generation is None:
                expectGen = generation

            # https://github.com/googleapis/google-cloud-python/issues/4490
            print("Patching storage with: &ifGenerationMatch=%s" % (expectGen,))
            storage.blob._MULTIPART_URL_TEMPLATE = (
                f'{origMultipartUrl}&ifGenerationMatch={expectGen}'
            )
            storage.blob._RESUMABLE_URL_TEMPLATE = (
                f'{origResumableUrl}&ifGenerationMatch={expectGen}'
            )

            model = json.loads(contents)

            inputStr = base64.b64decode(event['data']).decode('utf-8')
            print("Got aggregate input: %s" % (inputStr,))
            msgObj = json.loads(inputStr)
            if "fuel" in msgObj:
                model["fuels"].append(msgObj["fuel"])
            elif "count" in msgObj:
                model["count"] = msgObj["count"]

            expectedCount = model["count"]
            currentCount  = len(model["fuels"])
            if expectedCount > 0 and expectedCount == currentCount:
                result = sum(model["fuels"])
                print("THE RESULT IS IN: %d" % (result,))
            else:
                print("need more data (%d/%d)" % (currentCount, expectedCount))

            print("Storing the model")
            modelJson = json.dumps(model)
            try:
                blob.upload_from_string(modelJson, client=storage_client)
                success = True
            except Exception as e:
                print("Error %s" % (e,))
    else:
        print("Missing data in event :(")
# [END functions_aggregate]
import requests
from havenondemand.hodclient import *
import time

hodClient = HODClient('1105ea86-e3b9-440c-8a25-9595073dd137', 'v1')

def asyncRequestCompleted(jobID, error, **context):
  if error is not None:
    for err in error.errors:
      print "Error code: %d \nReason: %s \nDetails: %s\n" % (err.error, err.reason, err.detail)
  elif jobID is not None:
    hodClient.get_job_status(jobID, requestCompleted, **context)

def requestCompleted(response, error, **kwargs):
  if error != None:
    for err in error.errors:
      if err.error == ErrorCode.QUEUED:
        # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
        print 'queued'
        time.sleep(2)
        s = time.time()
        hodClient.get_job_status(err.jobID, requestCompleted)
          print 'job retrieval time ' + str(time.time() - s)
      elif err.error == ErrorCode.IN_PROGRESS:
        # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
        print "task is in progress. Retry in 20 secs. jobID: " + err.jobID
        time.sleep(1)
        hodClient.get_job_status(err.jobID, requestCompleted)
      else:
        resp += "Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail)
  elif response != None:
    return response['result']['document'][0]['content']

def get_text(filename):
  params = {'file': 'sample.mp3'}
  start = time.time()
  response = hodClient.post_request(params, HODApps.RECOGNIZE_SPEECH, async=True, callback=asyncRequestCompleted)
  print 'total time: ' + str(time.time() - start)
  return response
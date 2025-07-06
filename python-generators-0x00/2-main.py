import sys
processing = __import__('1-batch_processing')

#### print processed users in a Batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
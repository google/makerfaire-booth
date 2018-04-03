~/.local/bin/tensorflowjs_converter     --input_format=tf_saved_model     --output_node_names='final_result'     --saved_model_tags=serve     /tmp/retrain_arch_mobilenet_1.0_128/saved_models/1 /tmp/mob
gsutil mb gs://konerding-burgernet
gsutil cp /tmp/mob/* gs://konerding-burgernet
gsutil iam ch allUsers:objectViewer gs://konerding-burgernet

gsutil cors set cors.json gs://konerding-burgernet
[
  {
    "origin": ["http://localhost:1234"],
    "responseHeader": ["Content-Type"],
    "method": ["GET"],
    "maxAgeSeconds": 3600
  }
]

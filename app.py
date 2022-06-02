from flask import Flask, jsonify, request
from flask_cors import CORS
from pipeline_status_watcher import PipelineStatusWatcher
# from post_a_message import PostAMessage

# instantiate the app
app = Flask(__name__, static_url_path='/')
app.config.from_object(__name__)

pipeline_status_watcher = PipelineStatusWatcher()
pipeline_status_watcher.start()


# enable COR
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api/gitlab-pipeline', methods=['GET'])
def gitlab_pipeline():
    with pipeline_status_watcher.data_lock:
        response = {}
        response['stages'] = pipeline_status_watcher.stages_jobs_map
        response['repository_name'] = pipeline_status_watcher.repository_name
        response['branch_name'] = pipeline_status_watcher.branch_name
        response['update_counter'] = pipeline_status_watcher.update_counter
    return jsonify(response)

# @app.route('/api/post-a-message', methods=['POST'])
# def post_a_message():
#     response_object = {'status': 'success'}
#     post_data = request.get_json()
#     print(post_data)
#     post_a_message.data = post_data
#     response_object['message'] = 'Message sent'
#     return jsonify(response_object)

@app.route('/api/get-posted-message', methods=['get'])
def post_a_message():
    response = post_a_message.data
    return jsonify(response)

if __name__ == '__main__':
    app.run()
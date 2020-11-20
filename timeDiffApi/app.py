from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
import datetime
import dateutil.parser
from datetime import timedelta


app = Flask(__name__)
api = Api(app)


class timeDifference(Resource):
    def get(self, time):
        # Time Now
        timeNow = datetime.datetime.now()
        #External time
        timePublished = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        #Time Difference
        diff = timeNow - timePublished

        body = {
            # "time": timeNow,
            "timePublished": time,
            "difference": {
                "seconds": diff.seconds ,
                "mins": diff.seconds/60,
                "hours": diff.seconds/3600,
                "days": diff.days,
                }
        }
        return body
api.add_resource(timeDifference, '/timeDiff/<time>')

if __name__ == '__main__':
    app.run(port=8000)
